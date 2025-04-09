from crawler.scraper import run_scraper
import os
import sys

# Add the current directory (AV_identifier/) to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    print("🚀 Starting age verification crawler...\n")
    run_scraper()
    print("\n✅ Done!")


if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    main()
