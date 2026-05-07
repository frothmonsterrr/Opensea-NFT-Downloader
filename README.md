# OpenSea NFT Metadata and Image Downloader

A simple Python tool for downloading NFT metadata and image assets from an OpenSea collection using the OpenSea API.

The script fetches NFT metadata for a target contract, saves each token's metadata as a JSON file, and attempts to download the highest available image resolution from OpenSea-hosted CDN links.

## Features

- Downloads NFT metadata from OpenSea API v2
- Saves metadata as individual `.json` files
- Downloads NFT images into a local `images` folder
- Attempts multiple image resolutions, including 4000px, 3000px, 2000px, and 1000px
- Handles OpenSea pagination
- Handles basic rate limiting
- Uses `.env` configuration so API keys are not stored in the script

## Folder Output

After running the script, the following folders will be created:

```text
metadata/
images/
