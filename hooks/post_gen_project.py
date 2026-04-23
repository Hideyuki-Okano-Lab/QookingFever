import os
import shutil
import subprocess

try:
    subprocess.run(["git", "init", "-b", "main"], check=True, capture_output=True)
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", ":tada: Initial commit from QookingFever Cookiecutter"],
        check=True,
        capture_output=True,
    )
except Exception:
    pass

print("\n" + "=" * 50)
print("QookFast Project Successfully Created!")
print("=" * 50)

has_apptainer = shutil.which("apptainer") is not None

if not has_apptainer:
    print("\n  [WARNING] Apptainer is not installed or not in PATH.")
    print("    QookFast requires Apptainer to ensure reproducibility.")
    print("    Please install it before running `make setup`.")
    print("    (e.g., Run: sudo apt update && sudo apt install -y apptainer)")
    print("-" * 55)

print("\nNext steps:")
print(f"  1. cd {os.path.basename(os.getcwd())}")
print("  2. make setup   <-- This will take some time (downloading & indexing)")
print("  3. Move your .fastq.gz files into the ./raw_data/ directory")
print("  4. make run")
print("\nHappy Qooking with QookFast!")
print("=" * 55 + "\n")
