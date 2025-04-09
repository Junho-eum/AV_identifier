# Age Verification Identifier for Adult Websites

This project automates the detection of **age verification (AV)** mechanisms across adult websites using `Selenium`, `BeautifulSoup`, and a custom-trained `BERT` classifier.

It detects:
- Whether the site uses **age verification prompts**
- If it relies on **third-party AV providers** (e.g., Yoti, Veratad)
- Whether the site is displaying a **protest page** due to legislation (e.g., Virginia/Utah laws)

---

## Project Structure
```
AV_identifier/
├── main.py                     # Entry point to run the crawler
├── data/
│   ├── classified_adult_sites_test.csv
│   └── age_verification_results_selenium.csv
├── crawler/
│   ├── init.py
│   ├── config.py               # Keywords and provider list
│   ├── utils.py                # Checkbox and button click logic
│   ├── detection.py            # AV & protest detection helpers
│   └── scraper.py              # Main scraping logic
├── screenshots/                # Saved screenshots for visual inspection
└── html_dumps/                 # HTML dumps for fallback debugging
```
---

## Features

- Detects **explicit AV content** using a set of defined keywords
- Identifies known **third-party AV services**
- Handles **iframes** and navigates redirects to detect third-party integrations
- Captures **screenshots** and **HTML snapshots** for auditability
- Flags **protest pages** that block content due to legal requirements

---

## How It Works

1. A BERT model classifies domains as Adult or Non-Adult.
2. The crawler:
   - Loads each adult domain in a headless browser
   - Checks for AV indicators and protest language
   - Attempts modal interaction (e.g., checkbox, AV button)
   - Follows links to AV provider if present
   - Logs results and saves screenshots

---

## Requirements

- Python 3.10+
- Google Chrome (latest)
- ChromeDriver matching your Chrome version

### Install dependencies

```bash
pip install -r requirements.txt
```

### Setup

1. Install matching ChromeDriver

If you’re using macOS:
```bash
brew install chromedriver
```

2. Run the scraper 
```bash
python main.py
```
