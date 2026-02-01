import sys
from pathlib import Path
from authorship import guess_author

# --- Configuration ---
# Assuming the test is run from the 'song-lyrics' directory
BASE_DIR = Path(".")
LABELED_DIR = BASE_DIR / "labeled-lyrics"
UNLABELED_DIR = BASE_DIR / "unlabeled-lyrics"

def test_unknown1_is_pusha_t():
    """Verifies that unknown1.txt is identified as Pusha-T"""
    unknown_file = UNLABELED_DIR / "unknown1.txt"
    if not unknown_file.exists():
        print(f"⚠️ Skipped: Could not find {unknown_file}")
        return
        
    prediction = guess_author(unknown_file, LABELED_DIR)
    expected = "Pusha-T"
    
    assert prediction == expected, f"Expected {expected}, but got {prediction}"
    print(f"✅ PASS: unknown1.txt correctly identified as {prediction}")

def test_unknown2_is_biggie():
    """Verifies that unknown2.txt is identified as The-Notorious-B.I.G."""
    unknown_file = UNLABELED_DIR / "unknown2.txt"
    if not unknown_file.exists():
        print(f"⚠️ Skipped: Could not find {unknown_file}")
        return

    prediction = guess_author(unknown_file, LABELED_DIR)
    expected = "The-Notorious-B.I.G."
    
    assert prediction == expected, f"Expected {expected}, but got {prediction}"
    print(f"✅ PASS: unknown2.txt correctly identified as {prediction}")

def test_unknown3_is_j_cole():
    """Verifies that unknown3.txt is identified as J-Cole"""
    unknown_file = UNLABELED_DIR / "unknown3.txt"
    if not unknown_file.exists():
        print(f"⚠️ Skipped: Could not find {unknown_file}")
        return

    prediction = guess_author(unknown_file, LABELED_DIR)
    expected = "J-Cole"
    
    assert prediction == expected, f"Expected {expected}, but got {prediction}"
    print(f"✅ PASS: unknown3.txt correctly identified as {prediction}")

def test_unknown4_is_mf_doom():
    """Verifies that unknown4.txt is identified as MF-DOOM"""
    unknown_file = UNLABELED_DIR / "unknown4.txt"
    if not unknown_file.exists():
        print(f"⚠️ Skipped: Could not find {unknown_file}")
        return

    prediction = guess_author(unknown_file, LABELED_DIR)
    expected = "MF-DOOM"
    
    assert prediction == expected, f"Expected {expected}, but got {prediction}"
    print(f"✅ PASS: unknown4.txt correctly identified as {prediction}")

def run_all_tests():
    print("="*40)
    print("RUNNING AUTHORSHIP ACCURACY TESTS")
    print("="*40)
    
    # Check if directories exist first
    if not LABELED_DIR.exists() or not UNLABELED_DIR.exists():
        print("❌ Error: Could not find data directories.")
        print("Make sure you are inside the 'song-lyrics' folder.")
        sys.exit(1)

    tests = [
        test_unknown1_is_pusha_t,
        test_unknown2_is_biggie,
        test_unknown3_is_j_cole,
        test_unknown4_is_mf_doom
    ]

    failed = False
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"❌ FAIL: {test.__name__}")
            print(f"   Error: {e}")
            failed = True
        except Exception as e:
            print(f"❌ ERROR: {test.__name__} crashed")
            print(f"   Reason: {e}")
            failed = True
            
    print("="*40)
    if failed:
        print("RESULT: ⚠️ SOME TESTS FAILED")
        sys.exit(1)
    else:
        print("RESULT: 🏆 ALL TESTS PASSED")
        sys.exit(0)

if __name__ == "__main__":
    run_all_tests()
