.SILENT:

default:
	cat Makefile


clean:
	-rm dump.sql
	-rm reptile.db.old
	-rm *.dump
	-rm decoder.html
	-rm *.ipynb
	-rm *.to_mysql


build:
	-rm reptile.db
	quarto render decoder.qmd
	
fix_sql:
	sqlite3 reptile.db .dump > reptiledb.dump
	python fix_db_wrappers.py < reptiledb.dump > reptiledb.to_mysql

load_mysql:
	mysql -p -D reptiledb < reptiledb.to_mysql
