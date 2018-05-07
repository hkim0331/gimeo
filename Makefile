create:
	sqlite3 ${DB} < create.sql

clean:
	cd cgi; make clean

