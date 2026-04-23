import os
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
print("QookingFever Project Successfully Created!")
print("=" * 50)
print("\nNext steps:")
print(f"  1. cd {os.path.basename(os.getcwd())}")
print("  2. make setup   <-- This will take some time (downloading genomes & indexing)")
print("  3. Move your .fastq.gz files into the raw_data/ directory")
print("  4. make run")
print("\nHappy Qooking!")
print("=" * 50 + "\n")
