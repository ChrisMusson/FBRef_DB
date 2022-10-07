# FBRef_DB

## Usage

1. Download the .zip files for the leagues you want in your databse from this [MediaFire link](https://www.mediafire.com/folder/7s88iqido6nvc/FBRef).

1. Unzip those dowloaded files to the `web_pages/` folder - this creates a folder containing the html of the fbref web page for every league match since the start of the 2017-2018 season for your chosen leagues. The structure of the folders must be `./web_pages/<league>/<season>/file`

1. If you have downloaded more than just the `Premier_League.zip` file, change the `competitions` parameter in the `main()` function of `main.py` to, e.g., `main(competitions=["La_Liga", "Ligue_1", "Premier_League")`

1. Run `main.py` - this checks fbref for any newly played matches in your specified leagues, and if any are found, adds them to the `web_pages/` folder. It then parses these pages and adds them to the `master.db` database file.

You can then use a program like [DB Browser](https://sqlitebrowser.org/dl/) to explore this data using SQL queries. An overview of the database structure can be found [here](https://dbdiagram.io/d/62221bf854f9ad109a5e298c).

Note that `master.db` file in this repo only contains Premier League data, but the latest version of all_leagues.db is also present in the MediaFire link.