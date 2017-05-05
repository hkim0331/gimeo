DB = gimeo.db

install:
	install gimeo.cgi del.cgi -m 0755 /srv/gimeo/cgi/
	install public.html -m 0644 /srv/gimeo/public/index.html

create:
	sqlite3 ${DB} < create.sql
