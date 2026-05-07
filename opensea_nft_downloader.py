import requests
import json
import os
import time
import re
from dotenv import load_dotenv

# =========================
# CONFIG
# =========================

load_dotenv()

API_KEY = os.getenv("OPENSEA_API_KEY", "")
CHAIN = os.getenv("CHAIN_NAME", "")
CONTRACT = os.getenv("CONTRACT_ADDRESS", "")

LIMIT = int(os.getenv("LIMIT", 50))
DELAY = float(os.getenv("DELAY", 1.5))

if not API_KEY:
    raise ValueError("Missing OPENSEA_API_KEY in .env file")

if not CHAIN:
    raise ValueError("Missing CHAIN_NAME in .env file")

if not CONTRACT:
    raise ValueError("Missing CONTRACT_ADDRESS in .env file")

HEADERS = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

BASE = os.path.dirname(os.path.abspath(__file__))
META_DIR = os.path.join(BASE, "metadata")
IMG_DIR = os.path.join(BASE, "images")

os.makedirs(META_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# =========================
# HELPERS
# =========================

def save_json(token_id, data):
    path = os.path.join(META_DIR, f"{token_id}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def scrape_opensea_page(chain, contract, token_id):
    url = f"https://opensea.io/assets/{chain}/{contract}/{token_id}"

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)

        if r.status_code != 200:
            return []

        html = r.text

        urls = []
        urls += re.findall(r"https://i\.seadn\.io/[^\"]+", html)
        urls += re.findall(r"https://i2c\.seadn\.io/[^\"]+", html)

        return list(set(urls))

    except requests.RequestException:
        return []


# =========================
# HIGH-RES LOGIC
# =========================

def build_high_res_urls(url):
    base = url.split("?")[0]

    return [
        base + "?w=4000",
        base + "?w=3000",
        base + "?w=2000",
        base + "?w=1000",
        base
    ]


def download_best(url, token_id, index):
    candidates = build_high_res_urls(url)

    for u in candidates:
        try:
            r = requests.get(u, stream=True, timeout=60)

            if r.status_code != 200:
                continue

            ext = ".webp"
            ctype = r.headers.get("content-type", "")

            if "png" in ctype:
                ext = ".png"
            elif "jpeg" in ctype or "jpg" in ctype:
                ext = ".jpg"
            elif "gif" in ctype:
                ext = ".gif"

            path = os.path.join(IMG_DIR, f"{token_id}_{index}{ext}")

            with open(path, "wb") as f:
                for chunk in r.iter_content(8192):
                    if chunk:
                        f.write(chunk)

            print(f"[SAVED] #{token_id} -> {u}")
            return

        except requests.RequestException:
            continue

    print(f"[FAILED] #{token_id}")


# =========================
# MAIN LOOP
# =========================

def main():
    cursor = None
    total = 0

    while True:
        url = f"https://api.opensea.io/api/v2/chain/{CHAIN}/contract/{CONTRACT}/nfts?limit={LIMIT}"

        if cursor:
            url += f"&next={cursor}"

        print("\nFetching:", url)

        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
        except requests.RequestException as e:
            print("Request failed:", e)
            break

        if r.status_code == 429:
            print("Rate limited... sleeping")
            time.sleep(60)
            continue

        if r.status_code != 200:
            print("Error:", r.text)
            break

        data = r.json()
        nfts = data.get("nfts", [])

        for nft in nfts:
            token_id = nft.get("identifier")

            if not token_id:
                continue

            print("\nNFT:", token_id)

            save_json(token_id, nft)

            urls = []

            if nft.get("image_url"):
                urls.append(nft["image_url"])

            if nft.get("display_image_url"):
                urls.append(nft["display_image_url"])

            urls += scrape_opensea_page(CHAIN, CONTRACT, token_id)
            urls = list(set(urls))

            for i, u in enumerate(urls):
                download_best(u, token_id, i)

            total += 1
            time.sleep(DELAY)

        cursor = data.get("next")

        print("\nTOTAL SO FAR:", total)

        if not cursor:
            break

    print("\nDONE. TOTAL NFTs:", total)


if __name__ == "__main__":
    main()