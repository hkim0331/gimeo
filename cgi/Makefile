SERVER = gimeo.melt.kyutech.ac.jp
USER = ubuntu

DB = gimeo.db

install:
	rsync -avu gimeo.cgi del.cgi ${USER}@${SERVER}:/srv/gimeo/cgi/

create:
	sqlite3 ${DB} < create.sql
