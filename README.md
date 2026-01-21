# Archived
This project is archived due to FBRef [no longer having xG data](https://www.sports-reference.com/blog/2026/01/fbref-stathead-data-update/]) available on their website. There are multiple things one would need to change to get this repository to work from the current state it is in - I have fixed it locally, but the changes are messy and liable to change very often so don't feel it is worth updating until there is more clarity on the future of FBRef. The web pages and the master database can be downloaded from this [Google Drive link](https://drive.google.com/drive/folders/1t34zhIvlk-2M0F_2v-7wvdf1mep9Kq-C?usp=drive_link). The matches included in the dataset are all the valid matches (not abandoned, e.g.) in the date ranges below:

![FBRef data date ranges](https://i.imgur.com/0ckkXv1.png)

The rest of this README.md is unaltered from how it was when the project wasn't archived.

## FBRef_DB

A tool to compile player and team statistics from FBRef match reports into a local SQLite database.

### Setup

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

### Usage

1. **Download match data:**

   Download the `.zip` files for the leagues you want from this [Google Drive link](https://drive.google.com/drive/folders/1t34zhIvlk-2M0F_2v-7wvdf1mep9Kq-C?usp=drive_link). (Last updated 15 Jan 2026)

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

    By default, `main.py` is set to process the 2024-2025 season for the top 6 European leagues. You can modify the `competitions` and `seasons` lists to include/exclude the leagues and seasons you want to process.

   ```python
    competitions = ["Premier_League", "Bundesliga", "La_Liga", "Ligue_1", "Serie_A", "Primeira_Liga"]
    seasons = ["2023-2024", "2024-2025"]
    main("master.db", competitions=competitions, seasons=seasons)
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

### Explore the Data

Use [DB Browser for SQLite](https://sqlitebrowser.org/dl/) to explore `master.db` or `premier_league.db`.

A visual overview of the database schema is available here:  
https://dbdiagram.io/d/62221bf854f9ad109a5e298c

### Notes

- The `master.db` file in this repo contains all top 6 European leagues.
- A `premier_league.db` file (only Premier League) is available in the Google Drive link.
