# 2018 setting
USER   = hkim
#SERVER = g2.melt.kyutech.ac.jp
SERVER = g.hkim.jp
DB     = g2.db

install:
	rsync -avu common.rb gimeo.cgi gimeo-del.cgi ${USER}@${SERVER}:/srv/g2/cgi/

create:
	sqlite3 ${DB} < create.sql

clean:
	${RM} *.bak
