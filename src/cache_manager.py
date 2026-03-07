"""
Character Profile Cache Manager

Manages local caching of character profiles to avoid redundant API calls
and speed up repeated debates with the same characters.

Design Decisions:
-----------------
1. **Cache Invalidation Strategy**: Manual invalidation (Option B)
   - Cache persists forever unless manually deleted
   - Simple, predictable behavior
   - Users can delete specific cache files or entire cache directory
   - Future: Can add time-based expiration later

2. **Cache Key Normalization**:
   - Strip leading/trailing whitespace
   - Convert ASCII to lowercase (for English names)
   - Keep Chinese/Unicode characters as-is (no case conversion)
   - Remove internal whitespace to handle "孔 子" vs "孔子"
   - Filename: {normalized_name}_{language}.json

3. **Atomic Writes**: Use temp file + rename to prevent corruption
   - Write to .tmp file first
   - Rename to final filename (atomic operation)
   - Prevents partial writes from corrupting cache

4. **Storage Format**: JSON files, one per character-language pair
   - Easy to inspect and debug
   - Human-readable
   - Simple to manually edit or delete
"""

import os
import json
import re
import tempfile
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime


class CharacterCacheManager:
    """
    Manages local caching of character profiles.

    Cache Directory Structure:
    --------------------------
    cache/
    └── characters/
        ├── 孔子_zh.json
        ├── newton_en.json
        ├── 老子_zh.json
        └── socrates_en.json

    Cache File Schema:
    -----------------
    {
        "character_name": "孔子",           # Original input (user's spelling)
        "language": "zh",                  # zh or en
        "profile": "孔子（前551年...",      # Full research result
        "cached_at": "2026-03-06T08:30:00Z", # ISO timestamp
        "cache_version": "v1",             # Schema version
        "api_model": "claude-sonnet-4-5-20250929"  # Model used
    }
    """

    CACHE_VERSION = "v1"

    def __init__(self, cache_dir: str = "cache/characters"):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory for cache storage (default: cache/characters)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, character_name: str, language: str) -> Optional[str]:
        """
        Get cached character profile if it exists.

        Args:
            character_name: Character name (e.g., "孔子", "Newton")
            language: Language code ("zh" or "en")

        Returns:
            Cached profile text if found, None otherwise
        """
        cache_file = self._get_cache_filepath(character_name, language)

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)

            # Validate cache version
            if cache_data.get("cache_version") != self.CACHE_VERSION:
                # Cache version mismatch, treat as cache miss
                print(f"⚠ Cache version mismatch for {character_name}, ignoring cache")
                return None

            # Return the profile
            return cache_data.get("profile")

        except (json.JSONDecodeError, IOError, KeyError) as e:
            # Corrupted cache file - log warning and treat as cache miss
            print(f"⚠ Corrupted cache file for {character_name}: {e}")
            print(f"  Deleting corrupted cache: {cache_file}")
            try:
                cache_file.unlink()
            except:
                pass
            return None

    def set(
        self,
        character_name: str,
        language: str,
        profile: str,
        api_model: str = "claude-sonnet-4-5-20250929"
    ):
        """
        Save character profile to cache.

        Uses atomic write (temp file + rename) to prevent corruption.

        Args:
            character_name: Character name
            language: Language code ("zh" or "en")
            profile: Character profile text to cache
            api_model: API model used to generate profile
        """
        cache_data = {
            "character_name": character_name,
            "language": language,
            "profile": profile,
            "cached_at": datetime.utcnow().isoformat() + "Z",
            "cache_version": self.CACHE_VERSION,
            "api_model": api_model
        }

        cache_file = self._get_cache_filepath(character_name, language)

        try:
            # Atomic write: write to temp file first, then rename
            with tempfile.NamedTemporaryFile(
                mode='w',
                encoding='utf-8',
                dir=self.cache_dir,
                delete=False,
                suffix='.tmp'
            ) as tmp_file:
                json.dump(cache_data, tmp_file, ensure_ascii=False, indent=2)
                tmp_path = tmp_file.name

            # Atomic rename (overwrites existing file if present)
            Path(tmp_path).replace(cache_file)

        except Exception as e:
            print(f"⚠ Failed to write cache for {character_name}: {e}")
            # Clean up temp file if it exists
            try:
                if 'tmp_path' in locals():
                    Path(tmp_path).unlink()
            except:
                pass

    def invalidate(self, character_name: str, language: str) -> bool:
        """
        Remove specific cache entry.

        Args:
            character_name: Character name
            language: Language code

        Returns:
            True if cache was deleted, False if not found
        """
        cache_file = self._get_cache_filepath(character_name, language)

        if cache_file.exists():
            try:
                cache_file.unlink()
                return True
            except Exception as e:
                print(f"⚠ Failed to delete cache for {character_name}: {e}")
                return False
        else:
            return False

    def clear_all(self) -> int:
        """
        Clear entire cache directory.

        Use with caution!

        Returns:
            Number of cache files deleted
        """
        count = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    cache_file.unlink()
                    count += 1
                except:
                    pass
        except Exception as e:
            print(f"⚠ Error clearing cache: {e}")

        return count

    def get_stats(self) -> Dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats:
            {
                "total_characters": 15,
                "total_size_bytes": 234567,
                "total_size_mb": 0.22,
                "characters": [
                    {"name": "孔子", "language": "zh", "cached_at": "2026-03-05T10:00:00Z"},
                    ...
                ]
            }
        """
        characters = []
        total_size = 0

        try:
            for cache_file in sorted(self.cache_dir.glob("*.json")):
                try:
                    # Get file size
                    file_size = cache_file.stat().st_size
                    total_size += file_size

                    # Read cache metadata
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)

                    characters.append({
                        "name": cache_data.get("character_name", "unknown"),
                        "language": cache_data.get("language", "unknown"),
                        "cached_at": cache_data.get("cached_at", "unknown"),
                        "api_model": cache_data.get("api_model", "unknown"),
                        "size_bytes": file_size
                    })
                except:
                    # Skip corrupted files
                    pass

        except Exception as e:
            print(f"⚠ Error getting cache stats: {e}")

        return {
            "total_characters": len(characters),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "characters": characters
        }

    def list_cached_characters(self) -> List[str]:
        """
        List all cached character names.

        Returns:
            List of character names (format: "name (language)")
        """
        stats = self.get_stats()
        return [
            f"{char['name']} ({char['language']})"
            for char in stats['characters']
        ]

    def normalize_name(self, name: str) -> str:
        """
        Normalize character name for cache key generation.

        Normalization rules:
        1. Strip leading/trailing whitespace
        2. Remove internal whitespace (handles "孔 子" vs "孔子")
        3. Convert ASCII letters to lowercase
        4. Keep Chinese/Unicode characters as-is

        Examples:
            "Newton"        -> "newton"
            "  Newton  "    -> "newton"
            "New ton"       -> "newton"
            "孔子"          -> "孔子"
            "孔 子"         -> "孔子"
            "孔　子"        -> "孔子" (full-width space removed)

        Args:
            name: Character name to normalize

        Returns:
            Normalized name for cache key
        """
        # Strip leading/trailing whitespace
        name = name.strip()

        # Remove all whitespace (including full-width spaces)
        name = re.sub(r'\s+', '', name)

        # Convert ASCII to lowercase, keep Unicode as-is
        # This handles "Newton" vs "newton" but keeps "孔子" unchanged
        result = []
        for char in name:
            if char.isascii() and char.isalpha():
                result.append(char.lower())
            else:
                result.append(char)

        return ''.join(result)

    def _get_cache_filepath(self, character_name: str, language: str) -> Path:
        """
        Get cache file path for a character.

        Args:
            character_name: Character name
            language: Language code

        Returns:
            Path to cache file
        """
        normalized = self.normalize_name(character_name)
        filename = f"{normalized}_{language}.json"
        return self.cache_dir / filename
