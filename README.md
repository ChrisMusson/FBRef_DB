# FBRef_DB

1. Download the `web_pages.zip` file from this [MediaFire link](https://www.mediafire.com/file/q9dza619vx0g3mu/web_pages.zip/file).

1. Unzip `web_pages.zip` - this creates a `web_pages` folder containing the html of the fbref web page for every premier league match since the start of the 2017-2018 season.

1. Run `main.py` - this checks fbref for any newly played matches and if any are found, adds them to the `web_pages/` folder. It then parses these pages and adds them to the `master.db` database file.

You can then use a program like [DB Browser](https://sqlitebrowser.org/dl/) to explore this data using SQL queries. An overview of the database structure can be found [here](https://dbdiagram.io/d/62221bf854f9ad109a5e298c).
