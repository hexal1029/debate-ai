#!/usr/bin/env python3
"""
Test script for character caching functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cache_manager import CharacterCacheManager

def test_cache_manager():
    """Test cache manager basic functionality"""
    print("=" * 70)
    print("Testing Character Cache Manager")
    print("=" * 70)

    # Initialize cache manager
    cache_manager = CharacterCacheManager()
    print(f"\n✓ Cache manager initialized")
    print(f"  Cache directory: {cache_manager.cache_dir}")

    # Test name normalization
    print("\n--- Testing Name Normalization ---")
    test_cases = [
        ("Newton", "newton"),
        ("  Newton  ", "newton"),
        ("New ton", "newton"),
        ("孔子", "孔子"),
        ("孔 子", "孔子"),
        ("孔　子", "孔子"),  # Full-width space
    ]

    for input_name, expected in test_cases:
        normalized = cache_manager.normalize_name(input_name)
        status = "✓" if normalized == expected else "✗"
        print(f"  {status} '{input_name}' → '{normalized}' (expected: '{expected}')")

    # Test cache set/get
    print("\n--- Testing Cache Set/Get ---")

    # Set cache for 孔子
    test_profile = "孔子（前551年-前479年），名丘，字仲尼，春秋时期鲁国人..."
    cache_manager.set("孔子", "zh", test_profile)
    print("  ✓ Set cache for 孔子")

    # Get cache
    cached = cache_manager.get("孔子", "zh")
    if cached == test_profile:
        print("  ✓ Retrieved cache successfully")
    else:
        print("  ✗ Cache retrieval failed")

    # Test cache hit with variations
    print("\n--- Testing Cache Hit with Name Variations ---")
    variations = ["孔子", "孔 子", "孔　子"]
    for name in variations:
        cached = cache_manager.get(name, "zh")
        status = "✓" if cached == test_profile else "✗"
        print(f"  {status} Cache hit for '{name}'")

    # Test cache stats
    print("\n--- Testing Cache Stats ---")
    stats = cache_manager.get_stats()
    print(f"  Total characters: {stats['total_characters']}")
    print(f"  Total size: {stats['total_size_mb']} MB")
    print(f"  Characters: {[c['name'] for c in stats['characters']]}")

    # Test cache invalidation
    print("\n--- Testing Cache Invalidation ---")
    result = cache_manager.invalidate("孔子", "zh")
    if result:
        print("  ✓ Cache invalidated successfully")
    else:
        print("  ✗ Cache invalidation failed")

    # Verify it's gone
    cached = cache_manager.get("孔子", "zh")
    if cached is None:
        print("  ✓ Cache entry removed")
    else:
        print("  ✗ Cache entry still exists")

    print("\n" + "=" * 70)
    print("✓ All cache tests completed!")
    print("=" * 70)

if __name__ == "__main__":
    test_cache_manager()
