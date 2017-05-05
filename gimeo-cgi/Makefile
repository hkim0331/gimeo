DB = gimeo.db

install:
	install gimeo.cgi -m 0755 /srv/gimeo/cgi/gimeo.cgi
	install public.html -m 0644 /srv/gimeo/public/index.html

create:
	sqlite3 ${DB} < create.sql
