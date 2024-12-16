# Entry Proxy

A proxy server that forwards pre-built Tor packages to the Tor network.

## Features
- REST API for accepting pre-built Tor packages
- Direct forwarding to Tor network
- No circuit building (handled by client)

## Setup
1. Install dependencies:
   ```bash
   poetry install
   ```

2. Install and configure Tor daemon:
   ```bash
   sudo apt-get install tor
   ```

3. Run the server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

## API Documentation
POST /api/v1/forward
- Accepts raw Tor package in request body
- Returns response from Tor network
