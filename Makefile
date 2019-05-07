create:
	sqlite3 ${DB} < create.sql

clean:
	cd cgi; make clean

install:
	mkdir -p /srv/g/{cgi,public,log}
	(cd cgi; make install)

