from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random

CATEGORIES = {
    "mobiles": "https://www.daraz.pk/catalog/?q=mobile+phone",
    "laptops": "https://www.daraz.pk/catalog/?q=laptop",
    "headphones": "https://www.daraz.pk/catalog/?q=headphones",
    "watches": "https://www.daraz.pk/catalog/?q=smart+watch",
    "tablets": "https://www.daraz.pk/catalog/?q=tablet",
}

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def extract_price(text):
    # Remove currency symbol and spaces
    text = text.replace("Rs.", "").replace("Rs", "").replace(" ", "")
    # Remove commas (thousands separator)
    text = text.replace(",", "")
    text = text.strip()
    try:
        return float(text)
    except:
        return 0.0

def scrape_category(driver, category, url, pages=5):
    products = []

    for page in range(1, pages + 1):
        full_url = f"{url}&page={page}"
        print(f"  Page {page}...")

        try:
            driver.get(full_url)
        except Exception as e:
            print(f"  Browser crashed, restarting... {e}")
            try:
                driver.quit()
            except:
                pass
            driver = create_driver()
            driver.get(full_url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-qa-locator='product-item']"))
            )
        except:
            print(f"  Timeout on page {page}, continuing anyway...")

        time.sleep(random.uniform(3, 5))

        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        items = driver.find_elements(By.CSS_SELECTOR, "[data-qa-locator='product-item']")
        print(f"  Found {len(items)} items")

        for item in items:
            try:
                # NAME - from the <a> tag's title attribute
                name = "N/A"
                try:
                    a_tag = item.find_element(By.CSS_SELECTOR, ".RfADt a")
                    name = a_tag.get_attribute("title").strip()
                    if not name:
                        name = a_tag.text.strip()
                except:
                    pass

                # PRICE - class ooOxS confirmed from debug
                price = 0.0
                try:
                    price_el = item.find_element(By.CSS_SELECTOR, ".ooOxS")
                    price = extract_price(price_el.text.strip())
                except:
                    pass

# RATING - count filled stars (class Dy1nx = filled, W1iJ5 = half, B4Foa = empty)
                rating = 0.0
                try:
                    filled = item.find_elements(By.CSS_SELECTOR, "._9-ogB.Dy1nx")
                    half = item.find_elements(By.CSS_SELECTOR, "._9-ogB.W1iJ5")
                    rating = len(filled) + (0.5 * len(half))
                except:
                    pass

                # REVIEW COUNT - the number inside () in qzqFw
                review_count = 0
                try:
                    review_el = item.find_element(By.CSS_SELECTOR, ".qzqFw")
                    raw = review_el.text.strip().replace("(", "").replace(")", "")
                    review_count = int(raw) if raw.isdigit() else 0
                except:
                    pass

                # SOLD COUNT - inside class _1cEkb, first span says "X sold"
                reviews = 0
                try:
                    sold_el = item.find_element(By.CSS_SELECTOR, "._1cEkb span")
                    sold_text = sold_el.text.strip()
                    nums = "".join(filter(str.isdigit, sold_text))
                    reviews = int(nums) if nums else 0
                except:
                    pass

                if name != "N/A" and price > 0:
                    products.append({
                        "name": name,
                        "price": price,
                        "rating": rating,
                        "reviews": review_count,
                        "sold": reviews,
                        "category": category,
                    })
                    print(f"    OK -> {name[:50]} | Rs.{price} | rating:{rating} | sold:{reviews}")

            except Exception as e:
                print(f"  Item error: {e}")
                continue

        time.sleep(random.uniform(2, 3))

    return products


def scrape_all(pages_per_category=5):
    print("Starting browser...")
    driver = create_driver()
    all_products = []

    try:
        for category, url in CATEGORIES.items():
            print(f"\n===== Category: {category} =====")
            products = scrape_category(driver, category, url, pages=pages_per_category)
            all_products.extend(products)
            print(f"  Collected {len(products)} from {category} | Total so far: {len(all_products)}")
    finally:
        try:
            driver.quit()
        except:
            pass

    df = pd.DataFrame(all_products)

    if df.empty:
        print("\nNo products collected.")
    else:
        df.to_csv("data/raw_products.csv", index=False)
        print(f"\nDone! {len(df)} products saved to data/raw_products.csv")
        print(df.head(10))
        print(df.shape)

    return df


if __name__ == "__main__":
    df = scrape_all(pages_per_category=5)