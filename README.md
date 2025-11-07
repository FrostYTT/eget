# Website Scraper

A small Python utility for scraping websites in this repository and extracting contact data (emails).

This repository contains a simple script-driven scraper. The primary entry point is `main.py`.

## What's here

- `main.py` — entrypoint script (reads input, performs scraping, writes CSV outputs).
- `websites.csv` — input list of websites to process (project-specific format).
- `emails.csv` — primary output CSV with discovered emails.
- `emails copy.csv` — a copy/backup of email results.
- `google.csv` — (project-specific CSV, may contain Google search results or related data).
- `requirements.txt` — Python dependencies required to run the project.
- `update.fish` — a small fish-shell helper script (may update CSVs or perform maintenance).

Note: I made minimal assumptions about exact CSV formats; inspect `main.py` to confirm expected column headers and formats.

## Prerequisites

- Python 3.8+ (or your system Python 3)
- pip

## Install

Using the fish shell (your default):

```fish
python3 -m pip install -r requirements.txt
```

If you prefer a virtual environment:

```fish
python3 -m venv .venv
source .venv/bin/activate.fish
python3 -m pip install -r requirements.txt
```

## Usage

Run the main script from the project root:

```fish
python3 main.py
```

Typical workflow

1. Edit or populate `websites.csv` with the sites you want to scan.
2. Run `python3 main.py`.
3. Results will be written to `emails.csv` (and/or other CSV files used by the script).

If `main.py` requires CLI arguments or environment variables, check the top of `main.py` for usage details and adapt the commands above.

## Assumptions

- `main.py` is the intended entrypoint. If your workflow differs (for example, you run another script or a scheduler), update this README accordingly.
- CSV formats are project-specific; verify column names by opening the existing CSVs or `main.py`.

## Development & Troubleshooting

- To debug, run `main.py` under a debugger or add logging. If you hit errors about missing packages, re-run the install step above.
- If a CSV is malformed, inspect it in a text editor or spreadsheet app and fix headers/rows.

## Contribution

Small changes are welcome — open an issue or submit a PR with a clear description. For larger rewrites, please open an issue first to discuss.

## License

This project is provided under the MIT License. See `LICENSE` if present — otherwise consider adding one if you plan to share publicly.

## Contact

If you want help improving this README or the project, reply in the repo or reach out to the maintainer.
