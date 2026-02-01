# Lyric Detective

**An optimized stylometric analysis tool for identifying the authorship of song lyrics.**

`Lyric Detective` uses statistical linguistics (stylometry) to analyze the unique "fingerprint" of musical artists. By comparing unknown lyrics against a labeled database of known artists (such as *The Notorious B.I.G.*, *MF DOOM*, *J. Cole*, and *Pusha T*), the system calculates weighted distances to predict the most likely songwriter.

---

## Features

### Core Capabilities

* **Linguistic Profiling:** vectorizes text into statistical signatures based on five key metrics:
* **Average Word Length:** Measures vocabulary complexity.
* **Type-Token Ratio:** Calculates vocabulary diversity (unique words vs. total words).
* **Hapax Legomena:** Analyzes the ratio of words appearing exactly once.
* **Sentence Length:** Measures the average length of lines/bars.
* **Sentence Complexity:** Counts phrases per sentence to determine structural density.


* **Weighted Distance Algorithm:** Uses domain-specific weights to prioritize features that matter most in lyricism (e.g., unique word usage is weighted higher than sentence length).

### Performance Optimizations

* **Parallel Processing:** Utilizes Python's `ProcessPoolExecutor` to analyze multiple artist files simultaneously, significantly reducing startup time for large datasets.
* **Smart Caching:** Automatically serializes generated signatures to `signatures_cache.json`. Subsequent runs load data instantly, bypassing expensive re-calculation.
* **Memory Efficient:** Implements a custom `TextStats` class that tokenizes and normalizes text a single time during initialization, preventing redundant processing cycles.

---

## Directory Structure

For the tool to function correctly, your project **must** adhere to the following structure. The script relies on specific folder names to locate data.

```text
song-lyrics/
├── authorship.py              # The main analysis script
├── signatures_cache.json      # (Auto-generated) Cache file for speed
├── labeled-lyrics/            # Database of known artist lyrics
│   ├── J-Cole.txt
│   ├── MF-DOOM.txt
│   ├── Pusha-T.txt
│   └── The-Notorious-B.I.G.txt
└── unlabeled-lyrics/          # Unknown files to test
    ├── unknown1.txt
    ├── unknown2.txt
    ├── unknown3.txt
    └── unknown4.txt

```

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/lyric-detective.git
cd lyric-detective

```


2. **Navigate to the project directory:**
Ensure you are inside the folder containing the script and data subfolders.
```bash
cd song-lyrics

```


3. **Requirements:**
* Python 3.8+
* No external pip dependencies required (uses standard library).



---

## Usage

Run the program from the command line using the directory path argument (usually `.` for current directory).

### 1. Interactive Mode

Select a specific unknown file to analyze from a menu.

```bash
python authorship.py .

```

**Example Output:**

```text
Available Texts:
1. unknown1.txt
2. unknown2.txt
3. unknown3.txt
...
Choose a text by number: 1

Analyzing 'unknown1.txt'...
============================================================
RESULT: The artist is likely -> Pusha-T
============================================================

```

### 2. Batch Testing

Automatically process all files in the `unlabeled-lyrics` directory and print a summary table.

```bash
python authorship.py . --test-all

```

**Example Output:**

```text
Batch testing all files in unlabeled-lyrics...

File                           | Predicted Artist
--------------------------------------------------
unknown1.txt                   | Pusha-T
unknown2.txt                   | The-Notorious-B.I.G
unknown3.txt                   | J-Cole
unknown4.txt                   | MF-DOOM

```

---

## Configuration

The analysis is governed by a `WEIGHTS` dictionary found at the top of `authorship.py`. You can adjust these values to tune the sensitivity of the model:

```python
WEIGHTS = {
    "average_word_length": 11,
    "different_to_total": 33,      # High weight for vocabulary diversity
    "exactly_once_to_total": 50,   # Highest weight for unique word usage
    "average_sentence_length": 1.5,
    "average_sentence_complexity": 4
}

```

---

## How It Works 

1. **Ingestion:** The script scans `labeled-lyrics` for `.txt` files.
2. **Tokenization:** Files are normalized (punctuation removed, lowercase) and split. **Crucially**, the system treats newlines as sentence terminators to correctly analyze song bars.
3. **Signature Generation:**
* If a `signatures_cache.json` exists, it loads the data.
* If not, it spins up parallel processes to calculate the 5 linguistic features for every artist and saves the cache.


4. **Comparison:** The system calculates the weighted geometric distance between the unknown text's vector and every known artist's vector.
5. **Prediction:** The artist with the lowest distance score (closest statistical match) is returned.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

## Credits & License

* **Author:** Aidan Colvin
* **Original Core Logic:** Ryan Shaw, PhD
* **License:** Apache License 2.0

*Developed for Assignment A6: Authorship Identification.*
