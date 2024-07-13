from pathlib import Path

test_root = Path(__file__).resolve(strict=True).parent

test_file = test_root / "ressources" / "hamlet.sids.txt"  # long version
# test_file = test_root / "ressources" / "test.sids.txt"

with test_file.open() as f:
    test_strings = f.read().splitlines()

if __name__ == "__main__":
    print(test_strings)

