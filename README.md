# Song Lyrics Authorship Identification

**A stylistic analysis tool for identifying the authors of anonymous song lyrics.**

This program uses **stylometry**—the statistical analysis of literary style—to determine the authorship of unidentified text files. By calculating linguistic signatures (such as vocabulary diversity and sentence complexity) and comparing them against a database of known artists (like The Notorious B.I.G., MF DOOM, and J. Cole), it predicts the most likely songwriter for any given track.

## Features

* **Linguistic Profiling:** Generates statistical "fingerprints" based on five key metrics:
* Average word length
* Type-Token Ratio (vocabulary diversity)
* Hapax Legomena (ratio of unique words)
* Sentence length
* Phrase complexity


* **Weighted Distance Analysis:** Uses domain-specific weights to prioritize the most distinguishing features of lyrical writing.
* **High Performance:**
* **Parallel Processing:** Utilizes multi-core execution to process large artist databases simultaneously.
* **Smart Caching:** Saves generated signatures to JSON, making subsequent runs instant.



## Directory Structure

Your project must be organized exactly as follows for the script to locate the files:

```text
song-lyrics/
├── authorship.py              # The main analysis script
├── labeled-lyrics/            # Database of known artist lyrics
│   ├── The-Notorious-B.I.G.txt
│   ├── Pusha-T.txt
│   ├── MF-DOOM.txt
│   └── J-Cole.txt
└── unlabeled-lyrics/          # Files to analyze
    ├── unknown1.txt
    ├── unknown2.txt
    ├── unknown3.txt
    └── unknown4.txt

```

## Usage

Open your terminal or command prompt, navigate to the `song-lyrics` folder, and run the following commands.

### 1. Interactive Mode

Run the script pointing to the current directory (`.`). You will be prompted to select an unknown file to analyze.

```bash
python authorship.py .

```

**Example Output:**

```text
Available Texts:
1. unknown1.txt
2. unknown2.txt
...
Choose a text by number (1-4): 1

Analyzing 'unknown1.txt'...
============================================================
RESULT: The artist is likely -> hypnotize-the-notorious-b.i.g.-1997
============================================================

```

### 2. Batch Testing

To automatically test every file in the `unlabeled-lyrics` folder at once:

```bash
python authorship.py . --test-all

```

## How It Works

1. **Ingestion:** The script scans `labeled-lyrics` for text files.
2. **Vectorization:** It calculates a vector of 5 linguistic features for every known artist.
3. **Caching:** These signatures are saved to `signatures_cache.json` to speed up future runs.
4. **Comparison:** When analyzing an unknown file, it calculates the weighted distance between the unknown text and every known signature.
5. **Prediction:** The artist with the lowest distance score is identified as the author.

## Credits

**Author:** Aidan Colvin

**Original Core Logic:** Ryan Shaw, PhD

**Assignment:** A6 - Authorship Identification
