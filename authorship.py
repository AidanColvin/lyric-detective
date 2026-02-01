The primary reason your program is failing to predict the correct artists is likely **inconsistent punctuation** in the lyrics files, which skews the `average_sentence_length` metric.

* **The Problem:** The labeled Pusha-T file has almost no periods (`.`), causing the program to think the entire song is one giant sentence of **132 words**. If your unknown file has even a few periods (or is shorter), the "Sentence Length" difference becomes huge, incorrectly penalizing the match.
* **The Fix:** Update the code to treat **Newlines** (`\n`) as sentence breaks. This standardizes "sentences" into "lines/bars," which is a much more accurate stylistic measure for lyrics.

Here is the fixed `authorship.py`. I have also adjusted the **Weights** slightly to account for the new, smaller sentence lengths (since "lines" are shorter than "paragraphs," we increase the weight to make sure this feature still matters).

### **Steps to Fix:**

1. **Delete your old cache:** You **MUST** delete `song-lyrics/labeled-lyrics/signatures_cache.json` before running this. The old signatures are wrong.
```bash
rm song-lyrics/labeled-lyrics/signatures_cache.json

```


2. **Paste this code:** Replace your `authorship.py` with the code below.
3. **Run:** `python authorship.py song-lyrics --test-all`

### Updated `authorship.py`

```python
import sys
import re
import string
import json
import math
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from concurrent.futures import ProcessPoolExecutor

# --- Configuration ---
# Updated weights to balance the new "Line Length" metric
WEIGHTS = {
    "average_word_length": 11,
    "different_to_total": 33,
    "exactly_once_to_total": 50,
    "average_sentence_length": 1.5,  # Increased from 0.4 because line lengths are smaller
    "average_sentence_complexity": 4
}

CACHE_FILE_NAME = "signatures_cache.json"

# --- Text Processing Utilities ---

def split_string(text: str, delimiters: str) -> List[str]:
    """Splits a string into a list of substrings based on given delimiters.

    The function splits the input text at any of the characters found in the
    delimiters string. Whitespace is stripped from the resulting parts, and
    empty strings are excluded.

    Args:
        text (str): The input string to be split.
        delimiters (str): A string containing all delimiter characters.

    Returns:
        List[str]: A list of non-empty, trimmed substrings.
    """
    parts = re.split(f"[{re.escape(delimiters)}]", text)
    return [p.strip() for p in parts if p.strip()]

def split_into_sentences(text: str) -> List[str]:
    """Splits text into sentences based on newlines and standard punctuation.
    
    For lyrics, treating each line (newline) as a sentence allows for 
    better stylistic comparison than relying solely on punctuation.

    Args:
        text (str): The full text to process.

    Returns:
        List[str]: A list of sentences/lines.
    """
    # Treat newlines as sentence terminators by replacing them with a period
    normalized_text = text.replace('\n', '.')
    return split_string(normalized_text, ".!?")

def split_into_phrases(sentence: str) -> List[str]:
    """Splits a sentence into phrases based on intermediate punctuation.

    Args:
        sentence (str): The sentence string to process.

    Returns:
        List[str]: A list of phrases split by ',', ';', or ':'.
    """
    return split_string(sentence, ",;:")

def clean_word(word: str) -> str:
    """Normalizes a single word by removing punctuation and converting to lowercase.

    Args:
        word (str): The raw word token.

    Returns:
        str: The cleaned, lowercase word, or an empty string if the input
        was only punctuation.
    """
    return word.strip(string.punctuation).lower()

# --- Core Analyzer Class ---

class TextStats:
    """Analyzes text to calculate linguistic statistics for authorship attribution.

    This class ingests a text string once and pre-calculates expensive
    operations (like tokenization and sentence splitting) during initialization.
    This optimization prevents redundant processing when calculating multiple
    features.

    Attributes:
        text (str): The original input text.
        sentences (List[str]): A list of sentences derived from the text.
        clean_words (List[str]): A list of normalized, lowercase words.
    """

    def __init__(self, text: str):
        """Inits TextStats with the provided text and runs pre-processing.

        Args:
            text (str): The full text content to analyze.
        """
        self.text = text
        self.sentences = split_into_sentences(text)
        self.clean_words = self._get_clean_words()
        
    def _get_clean_words(self) -> List[str]:
        """Generates a list of cleaned words from the internal text.

        Returns:
            List[str]: A list of lowercase words with punctuation removed.
        """
        words = self.text.split()
        return [clean_word(w) for w in words if clean_word(w)]

    def average_word_length(self) -> float:
        """Calculates the mean length of all words in the text.

        Returns:
            float: The average character count per word. Returns 0.0 if the
            text contains no valid words.
        """
        if not self.clean_words:
            return 0.0
        total_length = sum(len(word) for word in self.clean_words)
        return total_length / len(self.clean_words)

    def different_to_total(self) -> float:
        """Calculates the vocabulary diversity (Type-Token Ratio).

        Returns:
            float: The ratio of unique words to total words. Returns 0.0 if
            the text contains no valid words.
        """
        total_words = len(self.clean_words)
        if total_words == 0:
            return 0.0
        different_words = len(set(self.clean_words))
        return different_words / total_words

    def exactly_once_to_total(self) -> float:
        """Calculates the ratio of Hapax Legomena (words appearing once).

        Returns:
            float: The ratio of words occurring exactly once to the total
            word count. Returns 0.0 if the text contains no valid words.
        """
        total_words = len(self.clean_words)
        if total_words == 0:
            return 0.0
        word_counts = {}
        for word in self.clean_words:
            word_counts[word] = word_counts.get(word, 0) + 1
        exactly_once = sum(1 for count in word_counts.values() if count == 1)
        return exactly_once / total_words

    def average_sentence_length(self) -> float:
        """Calculates the mean number of words per sentence.

        Returns:
            float: The average word count per sentence. Returns 0.0 if no
            sentences are detected.
        """
        if not self.sentences:
            return 0.0
        total_words = 0.0
        for sentence in self.sentences:
            words = sentence.split()
            total_words += len(words)
        return total_words / len(self.sentences)

    def average_sentence_complexity(self) -> float:
        """Calculates the mean number of phrases per sentence.

        Returns:
            float: The average phrase count per sentence. Returns 0.0 if no
            sentences are detected.
        """
        if not self.sentences:
            return 0.0
        total_phrases = sum(
            len(split_into_phrases(sentence)) for sentence in self.sentences
        )
        return total_phrases / len(self.sentences)

    def get_signature(self) -> Dict[str, float]:
        """Compiles all statistical features into a signature dictionary.

        Returns:
            Dict[str, float]: A dictionary mapping feature names to their
            calculated floating-point values.
        """
        return {
            "average_word_length": self.average_word_length(),
            "different_to_total": self.different_to_total(),
            "exactly_once_to_total": self.exactly_once_to_total(),
            "average_sentence_length": self.average_sentence_length(),
            "average_sentence_complexity": self.average_sentence_complexity(),
        }

# --- Parallel Processing Helper ---

def _process_single_file(file_path: Path) -> Tuple[str, Dict[str, float]]:
    """Processes a single file to generate its signature.

    This function is designed to be used by a ProcessPoolExecutor.

    Args:
        file_path (Path): The path to the text file to process.

    Returns:
        Tuple[str, Dict[str, float]]: A tuple containing the author's name
        (derived from the filename) and their statistical signature.
        Returns the author name and an empty dict if processing fails.
    """
    try:
        text = file_path.read_text(encoding="utf-8")
        analyzer = TextStats(text)
        return file_path.stem, analyzer.get_signature()
    except Exception as e:
        print(f"Warning: Could not process {file_path.name}: {e}", file=sys.stderr)
        return file_path.stem, {}

# --- Main Logic ---

def make_known_signatures(
    labeled_texts_dir: Path, 
    force_rebuild: bool = False
) -> Dict[str, Dict[str, float]]:
    """Generates or loads signatures for all known authors.

    This function attempts to load a cached JSON file first. If the cache is
    missing or invalid, it calculates signatures for all .txt files in the
    directory using parallel processing, and then saves the result to a new
    JSON cache file.

    Args:
        labeled_texts_dir (Path): Directory containing known author text files.
        force_rebuild (bool, optional): If True, ignores the cache and forces
            recalculation. Defaults to False.

    Returns:
        Dict[str, Dict[str, float]]: A dictionary mapping author names to their
        linguistic signatures.
    """
    cache_path = labeled_texts_dir / CACHE_FILE_NAME

    if cache_path.exists() and not force_rebuild:
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                print(f"Loading cached signatures from {cache_path}...")
                return json.load(f)
        except json.JSONDecodeError:
            print("Cache corrupted, rebuilding...")

    print("Calculating new signatures (Parallel)...")
    files = list(labeled_texts_dir.glob("*.txt"))
    known_signatures = {}

    with ProcessPoolExecutor() as executor:
        results = executor.map(_process_single_file, files)
        
    for author, sig in results:
        if sig: 
            known_signatures[author] = sig

    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(known_signatures, f, indent=4)
        print(f"Signatures saved to {cache_path}")
    except IOError as e:
        print(f"Warning: Could not save cache: {e}", file=sys.stderr)

    return known_signatures

def calculate_distance(sig1: Dict[str, float], sig2: Dict[str, float]) -> float:
    """Calculates the weighted geometric distance between two signatures.

    Args:
        sig1 (Dict[str, float]): The first signature dictionary.
        sig2 (Dict[str, float]): The second signature dictionary.

    Returns:
        float: The calculated distance score. Lower scores indicate higher similarity.
    """
    total = 0.0
    for feature, weight in WEIGHTS.items():
        total += abs(sig1[feature] - sig2[feature]) * weight
    return total

def find_closest_signature(
    unknown_sig: Dict[str, float], 
    known_sigs: Dict[str, Dict[str, float]]
) -> Optional[str]:
    """Identifies the author with the lowest signature distance.

    Args:
        unknown_sig (Dict[str, float]): The signature of the unidentified text.
        known_sigs (Dict[str, Dict[str, float]]): The database of known author signatures.

    Returns:
        Optional[str]: The name of the author with the closest match, or None
        if known_sigs is empty.
    """
    closest_author = None
    smallest_distance = float("inf")
    
    for author, known_sig in known_sigs.items():
        dist = calculate_distance(unknown_sig, known_sig)
        if dist < smallest_distance:
            smallest_distance = dist
            closest_author = author
            
    return closest_author

def guess_author(unlabeled_text_file: Path, labeled_texts_dir: Path) -> Optional[str]:
    """Determines the likely author of a specific unknown text file.

    Args:
        unlabeled_text_file (Path): Path to the unknown text file.
        labeled_texts_dir (Path): Path to the directory of known author texts.

    Returns:
        Optional[str]: The name of the predicted author.
    """
    text = unlabeled_text_file.read_text(encoding="utf-8")
    analyzer = TextStats(text)
    unknown_sig = analyzer.get_signature()

    known_sigs = make_known_signatures(labeled_texts_dir)
    return find_closest_signature(unknown_sig, known_sigs)

# --- User Interface ---

def choose_file(directory: Path) -> Path:
    """Prompts the user to select a text file from a directory via CLI.

    Args:
        directory (Path): The directory path to scan for .txt files.

    Returns:
        Path: The Path object of the selected file.

    Raises:
        SystemExit: If no text files are found in the directory.
    """
    texts = sorted([f for f in directory.iterdir() if f.is_file() and f.suffix == '.txt'])
    
    if not texts:
        print(f"No .txt files found in {directory}")
        sys.exit(1)

    print("\nAvailable Texts:")
    for i, file in enumerate(texts, start=1):
        print(f"{i}. {file.name}")
        
    while True:
        try:
            choice = input(f"\nChoose a text by number (1-{len(texts)}): ")
            idx = int(choice)
            if 1 <= idx <= len(texts):
                return texts[idx - 1]
            print("Invalid number.")
        except ValueError:
            print("Please enter a number.")

def main(labeled_dir: Path, unlabeled_dir: Path):
    """Runs the interactive mode of the authorship identification program.

    Args:
        labeled_dir (Path): Directory containing known author texts.
        unlabeled_dir (Path): Directory containing unknown texts.
    """
    try:
        text_file = choose_file(unlabeled_dir)
        print(f"\nAnalyzing '{text_file.name}'...")
        
        author = guess_author(text_file, labeled_dir)
        
        print("=" * 60)
        print(f"RESULT: The artist is likely -> {author}")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

def test_all_unknowns(labeled_dir: Path, unlabeled_dir: Path):
    """Batch processes all files in the unlabeled directory and prints predictions.

    Args:
        labeled_dir (Path): Directory containing known author texts.
        unlabeled_dir (Path): Directory containing unknown texts.
    """
    print(f"Batch testing all files in {unlabeled_dir}...\n")
    known_sigs = make_known_signatures(labeled_dir)
    
    files = sorted([f for f in unlabeled_dir.iterdir() if f.suffix == '.txt'])
    
    print(f"{'File':<30} | {'Predicted Artist'}")
    print("-" * 50)
    
    for f in files:
        text = f.read_text(encoding="utf-8")
        analyzer = TextStats(text)
        sig = analyzer.get_signature()
        author = find_closest_signature(sig, known_sigs)
        print(f"{f.name:<30} | {author}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} project_directory [--test-all]", file=sys.stderr)
        sys.exit(1)
    
    base_dir = Path(sys.argv[1])
    
    # Configuration for 'labeled-lyrics' and 'unlabeled-lyrics'
    labeled_dir = base_dir / "labeled-lyrics"
    unlabeled_dir = base_dir / "unlabeled-lyrics"
    
    if not labeled_dir.exists():
        print(f"Error: Could not find '{labeled_dir}'. Ensure the folder is named 'labeled-lyrics'.", file=sys.stderr)
        sys.exit(1)
    
    if not unlabeled_dir.exists():
        print(f"Error: Could not find '{unlabeled_dir}'. Ensure the folder is named 'unlabeled-lyrics'.", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[2] if len(sys.argv) > 2 else None
    
    if mode == "--test-all":
        test_all_unknowns(labeled_dir, unlabeled_dir)
    else:
        main(labeled_dir, unlabeled_dir)

```
