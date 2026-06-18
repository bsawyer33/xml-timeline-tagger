import xml.etree.ElementTree as ET
import urllib.parse
import subprocess
import shutil
import os
import sys

print("\n=========================================")
print("🎬  XML TAGGER - UNUSED MEDIA ORGANIZER 🎬")
print("=========================================\n")

raw_xml_input = input("👉 Drag and drop your XML file here, then press Enter: ").strip()
xml_path = raw_xml_input[1:-1] if raw_xml_input.startswith(('"', "'")) and raw_xml_input.endswith(('"', "'")) else raw_xml_input
xml_path = xml_path.replace("\\ ", " ")

if not os.path.exists(xml_path):
    print(f"\n❌ Error: XML file not found at '{xml_path}'.")
    sys.exit(1)

raw_media_input = input("📁 Drag and drop the master folder (e.g., 01_FOOTAGE), then press Enter: ").strip()
root_media_dir = raw_media_input[1:-1] if raw_media_input.startswith(('"', "'")) and raw_media_input.endswith(('"', "'")) else raw_media_input
root_media_dir = root_media_dir.replace("\\ ", " ")

if not os.path.exists(root_media_dir) or not os.path.isdir(root_media_dir):
    print(f"\n❌ Error: Target folder directory not found at '{root_media_dir}'.")
    sys.exit(1)

try:
    tree = ET.parse(xml_path)
    root = tree.getroot()
except Exception as e:
    print(f"\n❌ Error reading XML file: {e}")
    sys.exit(1)

used_paths = set()
for sequence in root.iter('sequence'):
    for pathurl in sequence.iter('pathurl'):
        url = pathurl.text
        if url and url.startswith('file://'):
            clean_url = url.replace("file://localhost", "").replace("file://", "")
            decoded_path = os.path.abspath(urllib.parse.unquote(clean_url))
            used_paths.add(decoded_path)

print("\n🔍 Scanning master media tree for asset files...")
all_files = []
for dirpath, _, filenames in os.walk(root_media_dir):
    for filename in filenames:
        if not filename.startswith('.'):
            all_files.append(os.path.abspath(os.path.join(dirpath, filename)))

unused_files = [f for f in all_files if f not in used_paths]

print(f"   • Total assets found inside folder: {len(all_files)}")
print(f"   • Assets actively used on timeline: {len(all_files) - len(unused_files)}")
print(f"   • Unused assets identified: {len(unused_files)}")

if not unused_files:
    print("\n🎉 Layout is fully optimal! No unused media files found to organize.")
    sys.exit(0)

parent_dir = os.path.dirname(os.path.abspath(root_media_dir))
root_folder_name = os.path.basename(os.path.abspath(root_media_dir))
unused_master_dir = os.path.join(parent_dir, f"Unused Media ({root_folder_name})")

print(f"\n📦 Extrapolating unused assets to clone path:\n   {unused_master_dir}\n")

moved_paths = []
for source_file in unused_files:
    rel_path = os.path.relpath(source_file, root_media_dir)
    target_file_path = os.path.join(unused_master_dir, rel_path)
    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
    try:
        shutil.move(source_file, target_file_path)
        moved_paths.append(target_file_path)
    except Exception as e:
        print(f"   ⚠️ Skipping {os.path.basename(source_file)}: {e}")

print("🏷️  Applying Red tag natively via metadata to moved UNUSED clips...")
finder_info_hex = "0000000000000000000C00000000000000000000000000000000000000000000"
for path in moved_paths:
    if os.path.exists(path):
        subprocess.run(["xattr", "-wx", "com.apple.FinderInfo", finder_info_hex, path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["xattr", "-w", "com.apple.metadata:_kMDItemUserTags", "Red\n6", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("\n✅ Congratulations, you’ve been programmed. Timeline clips labeled in Finder.")
print("=========================================\n")
