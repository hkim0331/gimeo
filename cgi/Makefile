USER = ubuntu
SERVER = gimeo.melt.kyutech.ac.jp

DB = gimeo.db

install:
	rsync -avu common.rb gimeo.cgi del.cgi ${USER}@${SERVER}:/srv/gimeo/cgi/
	@echo '*** check #!/usr/bin/ruby ***'

create:
	sqlite3 ${DB} < create.sql
