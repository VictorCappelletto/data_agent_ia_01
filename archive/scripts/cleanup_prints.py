#!/usr/bin/env python3
"""
Script to replace print() statements with proper logging calls.

Usage:
    python scripts/cleanup_prints.py [--dry-run]
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

def find_print_statements(file_path: Path) -> List[Tuple[int, str]]:
    """Find all print statements in a file."""
    prints = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if 'print(' in line and not line.strip().startswith('#'):
                prints.append((line_num, line.rstrip()))
    return prints

def replace_print_with_logger(line: str) -> str:
    """Replace print() with appropriate logger call."""
    # Preserve indentation
    indent = len(line) - len(line.lstrip())
    indent_str = line[:indent]
    
    # Check if it's an f-string
    if 'print(f"' in line or "print(f'" in line:
        # Extract the message
        match = re.search(r'print\(f["\'](.+?)["\']', line)
        if match:
            message = match.group(1)
            
            # Determine log level based on keywords
            if any(keyword in message.lower() for keyword in ['error', 'failed', 'exception']):
                return f'{indent_str}logger.error(f"{message}")'
            elif any(keyword in message.lower() for keyword in ['warning', 'warn']):
                return f'{indent_str}logger.warning(f"{message}")'
            elif any(keyword in message.lower() for keyword in ['debug', 'processing']):
                return f'{indent_str}logger.debug(f"{message}")'
            else:
                return f'{indent_str}logger.info(f"{message}")'
    
    # Check if it's a regular string
    elif 'print("' in line or "print('" in line:
        match = re.search(r'print\(["\'](.+?)["\']', line)
        if match:
            message = match.group(1)
            
            # Determine log level
            if any(keyword in message.lower() for keyword in ['error', 'failed', 'exception']):
                return f'{indent_str}logger.error("{message}")'
            elif any(keyword in message.lower() for keyword in ['warning', 'warn']):
                return f'{indent_str}logger.warning("{message}")'
            elif any(keyword in message.lower() for keyword in ['debug', 'processing']):
                return f'{indent_str}logger.debug("{message}")'
            else:
                return f'{indent_str}logger.info("{message}")'
    
    # Return original line if pattern not matched
    return line

def process_file(file_path: Path, dry_run: bool = False) -> int:
    """Process a single file and replace print statements."""
    prints = find_print_statements(file_path)
    
    if not prints:
        return 0
    
    print(f"\n📝 Processing: {file_path}")
    print(f"   Found {len(prints)} print() statements")
    
    if dry_run:
        for line_num, line in prints:
            new_line = replace_print_with_logger(line)
            print(f"   Line {line_num}:")
            print(f"     - {line.strip()}")
            print(f"     + {new_line.strip()}")
        return len(prints)
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Replace print statements
    replacements = 0
    for line_num, original_line in prints:
        idx = line_num - 1
        new_line = replace_print_with_logger(lines[idx].rstrip())
        if new_line != lines[idx].rstrip():
            lines[idx] = new_line + '\n'
            replacements += 1
            print(f"   ✅ Line {line_num}: {original_line.strip()[:50]}...")
    
    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"   Replaced {replacements} print() statements")
    return replacements

def main():
    """Main function."""
    dry_run = '--dry-run' in sys.argv
    
    print("=" * 60)
    print("DPL Agent - Print Statement Cleanup")
    print("=" * 60)
    
    if dry_run:
        print("\n🔍 DRY RUN MODE (no files will be modified)")
    
    # Find all Python files in data_pipeline_agent_lib
    root_path = Path(__file__).parent.parent / "data_pipeline_agent_lib"
    py_files = list(root_path.rglob("*.py"))
    
    print(f"\nScanning {len(py_files)} Python files...")
    
    total_replacements = 0
    files_modified = 0
    
    for py_file in sorted(py_files):
        replacements = process_file(py_file, dry_run)
        if replacements > 0:
            total_replacements += replacements
            files_modified += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Cleanup {'simulation' if dry_run else 'complete'}!")
    print(f"   Files scanned: {len(py_files)}")
    print(f"   Files modified: {files_modified}")
    print(f"   Total replacements: {total_replacements}")
    print("=" * 60)
    
    if dry_run:
        print("\n💡 Run without --dry-run to apply changes")

if __name__ == "__main__":
    main()

