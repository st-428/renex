#!/home/tree/src/renex/.venv/bin/python3

import argparse
from pathlib import Path
from detector import detect_file_extention

def get_unique_path(target_path: Path) -> Path:
    if not target_path.exists():
        return target_path

    counter = 1
    stem = target_path.stem
    ext = target_path.suffix
    parent = target_path.parent

    while True:
        new_path = parent / f"{stem}_{counter}{ext}"
        if not new_path.exists():
            return new_path
        counter += 1

def process_file(file_list: list[Path], confirm: bool = False):
    changed_files = []
    error_files = []

    for file_path in file_list:
        ext = detect_file_extention(file_path)
        if file_path.suffix == ext:
            continue

        if ext != None:
            new_path = get_unique_path(file_path.with_suffix(ext))
            changed_files.append([file_path, new_path])

        else:
            if file_path.suffix:
                new_path = get_unique_path(file_path.with_suffix(""))
                changed_files.append([file_path, new_path])
            error_files.append(file_path)

    print("Modified files:")
    for old_file, new_file in changed_files:
        print(f"{old_file.name} -> {new_file.name}")
        
    print("\nUnable to confirm file's extension:")
    for file in error_files:
        print(f"{file.name}")

    if not changed_files:
        return

    if confirm == False:
        Apply = input("\nApply changes? (y/n): ").strip().lower()
        if Apply not in ("y", "yes"):
            print("Cancelled.")
            return

    for old_file, new_file in changed_files:
        old_file.rename(new_file)
    print("Done.")

def main():
    parser = argparse.ArgumentParser(
        description="Auto detect the extension of the file and rename the filename"
    )

    parser.add_argument("target", type=Path, help="the target path")
    parser.add_argument("-y", "--yes", action="store_true", help="rename the file name without confirm")
    parser.add_argument("-r", "--recursive", action="store_true", help="recursively scan all files within subfolders.")

    args = parser.parse_args()
    target_path: Path = args.target

    if not target_path.exists():
        print(f"Path doesn't exists '{target_path}'")
        return

    if target_path.is_file():
        file_list = [target_path]

    else:
        pattern = "**/*" if args.recursive else "*"
        file_list = [p for p in target_path.glob(pattern) if p.is_file()]

    if not file_list:
        print("No processable files were found.")
        return

    process_file(file_list, confirm=args.yes)

if __name__ == "__main__":
    main()
