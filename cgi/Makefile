USER   = hkim
SERVER = gimeo.melt.kyutech.ac.jp
DB     = gimeo.db

install:
	rsync -avu common.rb gimeo.cgi gimeo-del.cgi ${USER}@${SERVER}:/srv/gimeo/cgi/

create:
	sqlite3 ${DB} < create.sql
