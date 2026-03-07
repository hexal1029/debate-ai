"""
Import legacy debate markdown files from outputs/ directory into the job manager.

This allows viewing historical debates generated via CLI in the web interface.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from models import DebateMessage, CreateDebateRequest, DebateStatus
from services.job_manager import DebateJob, job_manager


def parse_markdown_file(filepath: Path) -> Optional[dict]:
    """
    Parse a markdown debate file and extract debate information.

    Returns dict with:
    - parameters: CreateDebateRequest-like dict
    - messages: List of DebateMessage
    - created_at: datetime
    - completed_at: datetime
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title (first line after #)
        title_match = re.search(r'^# (.+?)：(.+?)$', content, re.MULTILINE)
        if not title_match:
            return None

        # Parse title: "Person1 vs Person2：Topic"
        title = title_match.group(0)
        participants_topic = title.replace('# ', '')

        # Try to extract participants and topic
        # Format: "Person1 vs Person2：Topic"
        match = re.search(r'(.+?)\s+vs\s+(.+?)[:：](.+)', participants_topic)
        if not match:
            return None

        p1 = match.group(1).strip()
        p2 = match.group(2).strip()
        topic = match.group(3).strip()

        # Extract metadata from "辩论信息" section
        rounds = 5  # default
        style = "academic"  # default
        language = "zh"

        rounds_match = re.search(r'辩论轮数[：:]\s*(\d+)', content)
        if rounds_match:
            rounds = int(rounds_match.group(1))

        style_match = re.search(r'辩论风格[：:]\s*(\S+)', content)
        if style_match:
            style_text = style_match.group(1)
            if 'casual' in style_text or '轻松' in style_text:
                style = "casual-chat"
            elif 'heated' in style_text or '激烈' in style_text:
                style = "heated-debate"
            elif 'comedy' in style_text or '相声' in style_text:
                style = "comedy-duo"

        # Extract timestamp from filename or metadata
        filename = filepath.stem
        timestamp_match = re.search(r'(\d{8})_(\d{6})', filename)
        if timestamp_match:
            date_str = timestamp_match.group(1)
            time_str = timestamp_match.group(2)
            created_at = datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
        else:
            created_at = datetime.fromtimestamp(filepath.stat().st_mtime)

        # Extract messages from markdown
        messages = []

        # Find all message sections (### emoji Speaker)
        message_pattern = r'###\s+([🎤🔵🟡🎭])\s+(.+?)\n\n(.+?)(?=\n---|\n###|\Z)'

        for match in re.finditer(message_pattern, content, re.DOTALL):
            emoji = match.group(1)
            speaker = match.group(2).strip()
            message_content = match.group(3).strip()

            # Determine role based on speaker and emoji
            if emoji == '🎤' or '主持人' in speaker or 'Moderator' in speaker:
                role = "moderator"
            elif speaker == p1:
                role = "character1"
            elif speaker == p2:
                role = "character2"
            else:
                # Try to determine by position
                if len(messages) == 0 or any('主持' in m.speaker for m in messages if len(messages) > 0):
                    role = "moderator"
                else:
                    # Alternate between character1 and character2
                    last_char_msgs = [m for m in messages if m.role in ['character1', 'character2']]
                    if last_char_msgs and last_char_msgs[-1].role == 'character1':
                        role = "character2"
                    else:
                        role = "character1"

            messages.append(DebateMessage(
                speaker=speaker,
                role=role,
                content=message_content
            ))

        return {
            'parameters': {
                'p1': p1,
                'p2': p2,
                'topic': topic,
                'rounds': rounds,
                'style': style,
                'language': language,
                'language_style': '现代口语'
            },
            'messages': messages,
            'created_at': created_at,
            'completed_at': created_at,  # Assume completed immediately
        }

    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None


async def import_legacy_debates(outputs_dir: str, exclude_files: List[str] = None):
    """
    Import all markdown files from outputs directory into job_manager.

    Args:
        outputs_dir: Path to outputs directory
        exclude_files: List of filenames to exclude (e.g., old debates)
    """
    if exclude_files is None:
        exclude_files = []

    outputs_path = Path(outputs_dir)
    if not outputs_path.exists():
        print(f"Outputs directory not found: {outputs_dir}")
        return

    # Find all markdown files
    md_files = list(outputs_path.glob("*.md"))

    imported_count = 0

    for md_file in sorted(md_files, key=lambda f: f.stat().st_mtime):
        # Skip excluded files
        if md_file.name in exclude_files:
            print(f"Skipping excluded file: {md_file.name}")
            continue

        print(f"Importing: {md_file.name}")

        # Parse the markdown file
        debate_data = parse_markdown_file(md_file)

        if not debate_data:
            print(f"  ✗ Failed to parse")
            continue

        # Create a job in the job_manager
        # Use the original filename timestamp as the ID
        timestamp_match = re.search(r'(\d{8})_(\d{6})', md_file.stem)
        if timestamp_match:
            job_id = f"deb_{timestamp_match.group(1)}{timestamp_match.group(2)}"
        else:
            # Use file modification time
            mtime = int(md_file.stat().st_mtime * 1000)
            job_id = f"deb_{mtime}"

        # Create DebateJob
        job = DebateJob(
            id=job_id,
            status=DebateStatus.COMPLETED,
            parameters=CreateDebateRequest(**debate_data['parameters']),
            messages=debate_data['messages'],
            created_at=debate_data['created_at'],
            completed_at=debate_data['completed_at']
        )

        # Add to job_manager
        job_manager.jobs[job_id] = job

        imported_count += 1
        print(f"  ✓ Imported as {job_id} ({len(debate_data['messages'])} messages)")

    print(f"\n✓ Imported {imported_count} legacy debates")


# Function to be called on startup
async def load_legacy_debates_on_startup():
    """
    Load legacy debates from outputs/ directory on server startup.

    Excludes the oldest "什么是好诗" debate as requested.
    """
    import sys
    from pathlib import Path

    # Get project root (parent of backend/)
    project_root = Path(__file__).parent.parent.parent
    outputs_dir = project_root / "outputs"

    # Exclude the oldest debate about "什么是好诗"
    exclude_files = [
        "李白_vs_杜甫_什么是好诗_20260131_235748.md"
    ]

    await import_legacy_debates(str(outputs_dir), exclude_files)
