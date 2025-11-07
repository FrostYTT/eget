# eget — Email Wget

A small, focused CLI tool to discover public contact email addresses from websites and append results to an output file.

Overview

- Dependencies: `requirements.txt` lists the Python packages the project needs.
- License: GPLv3

Quick start

1. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

2. Run the scraper from the project root:

```bash
python3 eget.py <input-file> <output-file> [-v] [-s]
```

- `<input-file>` — path to a file containing a list of sites or queries (one per line).
- `<output-file>` — path to the file where found addresses will be appended.
- `-v`, `--verbose` — optional, show progress and matches.
- `-s`, `--statistics` — optional, print basic run statistics after completion.