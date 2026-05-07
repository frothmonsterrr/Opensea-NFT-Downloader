# OpenSea NFT Downloader

A lightweight Python tool for backing up NFT metadata and high-resolution image assets from OpenSea collections.

This script uses the OpenSea API to fetch NFTs from a target contract, saves each NFT's metadata as a `.json` file, and attempts to download the best available image from OpenSea-hosted image URLs.

---

## Features

- Downloads NFT metadata from OpenSea API v2
- Saves each NFT's metadata as an individual JSON file
- Downloads NFT images into a local `images` folder
- Attempts higher-resolution image versions where available
- Supports OpenSea pagination
- Handles basic rate limiting
- Uses a `.env` file so API keys are not stored inside the script
- Keeps downloaded images and metadata out of GitHub by default

---

## Folder Structure

Your repository should look like this:

```text
opensea-nft-downloader/
│
├── opensea_nft_downloader.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── LICENSE
```

After running the script, these folders will be created automatically:

```text
metadata/
images/
```

Example output:

```text
metadata/1.json
metadata/2.json
metadata/3.json

images/1_0.webp
images/2_0.png
images/3_0.jpg
```

---

## Requirements

You will need:

- Python 3.9 or newer
- An OpenSea Developer API key
- The contract address of the NFT collection
- The correct OpenSea chain name, for example `ethereum`, `polygon`, `base`, or another supported chain

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

The required packages are:

```txt
requests
python-dotenv
```

---

## Configuration

This project uses a `.env` file for private settings.

Do not put your API key directly inside the Python script.

---

### 1. Create a `.env` file

In the main project folder, create a file called:

```text
.env
```

Then add the following:

```env
OPENSEA_API_KEY=your_opensea_api_key_here
CHAIN_NAME=ethereum
CONTRACT_ADDRESS=your_contract_address_here
LIMIT=50
DELAY=1.5
```

---

### 2. Update the values

Replace the example values with your own:

```env
OPENSEA_API_KEY=your_real_opensea_api_key
CHAIN_NAME=ethereum
CONTRACT_ADDRESS=0xYourContractAddressHere
LIMIT=50
DELAY=1.5
```

---

## Config Options

| Setting | Description |
|---|---|
| `OPENSEA_API_KEY` | Your OpenSea Developer API key |
| `CHAIN_NAME` | The OpenSea chain name, such as `ethereum`, `polygon`, or `base` |
| `CONTRACT_ADDRESS` | The NFT collection contract address |
| `LIMIT` | Number of NFTs requested per API call |
| `DELAY` | Delay between NFT downloads, in seconds |

---

## Usage

Once your `.env` file is set up, run:

```bash
python opensea_nft_downloader.py
```

The script will:

1. Connect to the OpenSea API
2. Fetch NFTs from the contract address
3. Save each NFT's metadata into the `metadata` folder
4. Attempt to download image assets into the `images` folder
5. Continue through all available pages until complete

---

## Example Terminal Output

```text
Fetching: https://api.opensea.io/api/v2/chain/ethereum/contract/0xYourContractAddressHere/nfts?limit=50

NFT: 1
[SAVED] #1 -> https://i.seadn.io/example-image?w=4000

NFT: 2
[SAVED] #2 -> https://i.seadn.io/example-image?w=4000

TOTAL SO FAR: 50

DONE. TOTAL NFTs: 500
```

---

## GitHub Safety

Never upload your real `.env` file.

Your `.gitignore` should include:

```gitignore
.env
metadata/
images/
```

This prevents your API key and downloaded files from being uploaded to GitHub.

---

## Files You Should Upload

These files are safe to upload:

```text
opensea_nft_downloader.py
README.md
requirements.txt
.env.example
.gitignore
LICENSE
```

---

## Files You Should Not Upload

Do not upload:

```text
.env
metadata/
images/
```

The `.env` file may contain your real API key.

The `metadata` and `images` folders may contain large downloaded files.

---

## Example `.env.example`

The repository should include a safe example file named:

```text
.env.example
```

Example contents:

```env
OPENSEA_API_KEY=your_opensea_api_key_here
CHAIN_NAME=ethereum
CONTRACT_ADDRESS=your_contract_address_here
LIMIT=50
DELAY=1.5
```

This file is safe to upload because it does not contain real credentials.

---

## Rate Limits

OpenSea may rate-limit requests.

If the script receives a rate-limit response, it will pause and retry.

You can increase the delay between downloads by changing:

```env
DELAY=2.5
```

A higher delay may make the script slower, but it can reduce the chance of being rate-limited.

---

## Notes About Image Downloads

The script checks available OpenSea image URLs and attempts to download higher-resolution versions using common width parameters such as:

```text
?w=4000
?w=3000
?w=2000
?w=1000
```

Not every NFT image will have a higher-resolution version available.

If a high-resolution version is not available, the script will try the original image URL.

---

## Important Disclaimer

This tool is intended for backing up NFT collections you own, manage, or have permission to archive.

Users are responsible for following:

- OpenSea's API rules
- OpenSea's terms of service
- Applicable copyright and intellectual property laws
- Any collection-specific licensing terms

This project is provided for educational and archival purposes only.

---

## License

This project is released under the MIT License.

See the `LICENSE` file for details.
