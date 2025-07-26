# FBRef_DB

A tool to compile player and team statistics from FBRef match reports into a local SQLite database.

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ChrisMusson/FBRef_DB.git
   cd FBRef_DB
   ```

2. **Install dependencies with [uv](https://github.com/astral-sh/uv):**

   If you don't already have `uv` installed:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Then, create and activate a virtual environment:

   ```bash
   uv venv .venv
   source .venv/bin/activate
   ```

   And install the dependencies from pyproject.toml:

   ```bash
   uv pip install .
   ```

## Usage

1. **Download match data:**

   Download the `.zip` files for the leagues you want from this [Google Drive link](https://drive.google.com/drive/folders/1t34zhIvlk-2M0F_2v-7wvdf1mep9Kq-C?usp=drive_link). (Last updated 26 July 2025)

2. **Extract files:**

   Unzip the downloaded files into the `web_pages/` directory.  
   This should result in a folder structure like:

   ```
   web_pages/
   ├── Premier_League/
   │   ├── 2017-2018/
   │   ├── 2018-2019/
   │   └── ...
   └── Ligue_1/
       └── ...
   ```

3. **Edit `main.py` to specify your leagues:**

   If you downloaded more than just the Premier League data, change the `competitions` argument in the `main()` call:

   ```python
   main(competitions=["Premier_League", "La_Liga", "Ligue_1"])
   ```

4. **Run the script:**

   ```bash
   python main.py
   ```

   This will:
   - Check FBRef for newly played matches in your selected leagues
   - Add new match pages to the `web_pages/` folders
   - Parse the HTML pages
   - Populate/update the `master.db` SQLite database

## Explore the Data

Use [DB Browser for SQLite](https://sqlitebrowser.org/dl/) to explore `master.db` or `premier_league.db`.

A visual overview of the database schema is available here:  
https://dbdiagram.io/d/62221bf854f9ad109a5e298c

## Notes

- The `master.db` file in this repo contains all top 6 European leagues.
- A `premier_league.db` file (only Premier League) is available in the Google Drive link.
