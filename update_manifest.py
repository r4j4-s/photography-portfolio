#!/usr/bin/env python3
"""
Script to automatically update images/manifest.json based on actual folder structure.
"""
import json
import os
from pathlib import Path

# Image file extensions to include
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

def is_image_file(filename):
    """Check if a file is an image based on extension."""
    return Path(filename).suffix.lower() in IMAGE_EXTENSIONS

def scan_images_directory(images_dir):
    """Scan the images directory and build the manifest structure."""
    manifest = {}

    # Iterate through category folders
    for category in sorted(os.listdir(images_dir)):
        category_path = os.path.join(images_dir, category)

        # Skip non-directories and manifest.json
        if not os.path.isdir(category_path) or category == 'manifest.json':
            continue

        # Get all items in the category folder
        items = sorted(os.listdir(category_path))
        subdirs = [item for item in items if os.path.isdir(os.path.join(category_path, item))]
        files = [item for item in items if is_image_file(item)]

        # If there are subdirectories, use nested structure
        if subdirs:
            manifest[category] = {}
            for subdir in subdirs:
                subdir_path = os.path.join(category_path, subdir)
                subdir_files = sorted([
                    f for f in os.listdir(subdir_path)
                    if is_image_file(f)
                ])
                if subdir_files:
                    manifest[category][subdir] = subdir_files
        # Otherwise, use flat list
        elif files:
            manifest[category] = files

    return manifest

def main():
    """Main function to update the manifest."""
    script_dir = Path(__file__).parent
    images_dir = script_dir / 'images'
    manifest_path = images_dir / 'manifest.json'

    print(f"Scanning directory: {images_dir}")

    # Scan and build manifest
    manifest = scan_images_directory(images_dir)

    # Write to manifest.json
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"✓ Updated {manifest_path}")
    print(f"  Found {len(manifest)} categories")
    for category, content in manifest.items():
        if isinstance(content, dict):
            total = sum(len(files) for files in content.values())
            print(f"    - {category}: {len(content)} subcategories, {total} images")
        else:
            print(f"    - {category}: {len(content)} images")

if __name__ == '__main__':
    main()
