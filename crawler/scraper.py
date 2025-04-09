import os
import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .config import age_keywords, protest_keywords, providers
from .utils import click_checkbox, click_start_button
from .detection import detect_protest_page, detect_av_indicators, detect_providers


def run_scraper():
    # Create output directories if missing
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("html_dumps", exist_ok=True)

    # Load data
    df = pd.read_csv("data/classified_adult_sites_test.csv")
    adult_domains = df[df['adult_prediction']
                       == "Adult"]["Domain"].dropna().unique()

    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)

    results = []

    for domain in adult_domains:
        url = f"https://{domain.strip()}"
        print(f"\nScraping {url}...")
        info_url = None
        redirected_url = None

        try:
            driver.get(url)
            time.sleep(3)

            html = driver.page_source.lower()
            if detect_protest_page(html, protest_keywords):
                print("🚫 Landing page is a protest or opt-out page.")

                protest_path = f"screenshots/{domain.strip().replace('.', '_')}_PROTEST.png"
                driver.save_screenshot(protest_path)
                print(f"[Screenshot] Protest page saved to: {protest_path}")

                results.append({
                    "url": domain,
                    "age_verification_present": False,
                    "matched_snippets": None,
                    "providers_found": None,
                    "info_url": None,
                    "redirected_url": None,
                    "av_statement_protest": True,
                    "error": None
                })
                continue

            # Try checkbox
            try:
                click_checkbox(driver)
                print("☑️ Consent checkbox clicked.")
            except Exception as e:
                print("⚠️ Consent checkbox not found.")

            # Try button
            av_type = None

            # Try clicking AV-related button
            try:
                av_type = click_start_button(driver)
                if av_type:
                    print(f"▶️ AV button clicked: {av_type}")
                else:
                    print("⚠️ No AV button found.")
            except Exception as e:
                print(f"⚠️ AV button click failed: {e}")

            time.sleep(3)

            # Look for info link in iframes
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            print(f"🖼️ Found {len(iframes)} iframe(s)")

            for index, iframe in enumerate(iframes):
                try:
                    driver.switch_to.frame(iframe)
                    print(f"↪️ Switched to iframe {index}")

                    links = driver.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        text = link.text.strip().lower()
                        href = link.get_attribute("href")
                        print(f"[iframe {index}] ⛓️ '{text}' -> {href}")

                        if "click here for more information" in text:
                            info_url = href
                            driver.get(info_url)
                            time.sleep(2)
                            redirected_url = driver.current_url
                            print(f"🌐 Redirected to: {redirected_url}")
                            break

                    driver.switch_to.default_content()
                    if info_url:
                        break

                except Exception as e:
                    print(f"⚠️ Error in iframe {index}: {e}")
                    driver.switch_to.default_content()

            # Fallback capture
            if not info_url:
                html_path = f"html_dumps/{domain.replace('.', '_')}_post_iframe.html"
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(driver.page_source)

            # Final content analysis
            html = driver.page_source.lower()
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator=" ").lower()

            matched_snippets = detect_av_indicators(text, age_keywords)
            found_providers = detect_providers(text, providers)
            age_verification = bool(matched_snippets)

            if age_verification:
                print("✅ Age verification content FOUND.")
            else:
                print("❌ No age verification content found.")

            results.append({
                "url": domain,
                "age_verification_present": age_verification,
                "matched_snippets": " | ".join(matched_snippets) if matched_snippets else None,
                "providers_found": ", ".join(found_providers) if found_providers else None,
                "info_url": info_url,
                "redirected_url": redirected_url,
                "av_statement_protest": False,
                "error": None
            })

        except Exception as e:
            print(f"❗ Error: {e}")
            results.append({
                "url": domain,
                "age_verification_present": False,
                "matched_snippets": None,
                "providers_found": None,
                "info_url": None,
                "redirected_url": None,
                "av_statement_protest": False,
                "error": str(e),
                "av_type": av_type if av_type else "none",
            })

        time.sleep(random.uniform(2, 4))

        # Always take a final screenshot for each domain
        final_screenshot_path = f"screenshots/{domain.strip().replace('.', '_')}_FINAL.png"
        driver.save_screenshot(final_screenshot_path)
        print(f"📸 Final screenshot saved to: {final_screenshot_path}")

    driver.quit()

    output = pd.DataFrame(results)
    output.to_csv("data/age_verification_results_selenium.csv", index=False)
    print("\n✅ Scraping complete. Results saved to data/age_verification_results_selenium.csv.")
