#!/usr/bin/ruby
# coding: utf-8
# under construction, 2017-05-05 15:52

require 'cgi'
require 'sequel'

# production
UPLOAD = "/srv/gimeo/public/upload"
DB = Sequel.connect("mysql2://#{ENV['GIMEO_USER']}:#{ENV['GIMEO_PASS']}@dbs.melt.kyutech.ac.jp/gimeo")

#development
#UPLOAD = "./upload"
#DB = Sequel.sqlite("gimeo.db")
#

def list()
  puts "<ol>"
  DB[:gifs].where(stat: true).each do |r|
    name = "#{r[:id]}.gif"
    comments=""
    DB[:comments].where(gif_id: r[:id]).each do |c|
      comments << " " << c[:comment]
    end
    print <<EOL
<li><a class='btn btn-danger' href="/cgi/del.cgi?cmd=del&id=#{r[:id]}">del</a>
<a href="/upload/#{name}">#{r[:title]}</a>#{comments}</li>
EOL
  end
  puts "</ol>"
end

def del(id)
  DB[:gifs].where(id: id).update(stat: false,
                                 timestamp: Time.now.strftime("%F %T"))
end

# FIXME
def auth?()
  true
end

# FIXME
def auth()

end

# main
cgi = CGI.new
print <<EOH
content-type: text/html

<!DOCTYPE html>
<html>
<head>
  <meta http-equiv='X-UA-Compatible' content='IE=edge' />
  <meta name='viewport' content='width=device-width, initial-scale=1.0' />
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta http-equiv="Content-Style-Type" content="text/css" />
  <meta name="generator" content="pandoc" />
  <title>index</title>
  <style type="text/css">code{white-space: pre;}</style>
  <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body><div class="container">
EOH

puts "<h1>GIF AMINE(delete)</h1>"

begin
  if auth?() and (cgi['cmd'] == "del")
    del(cgi['id'])
  elsif auth?()
    list()
  else
    auth()
  end
rescue
  print <<EOR
<p style='color:red;'>#{$!}</p>
<p><a href="/cgi/gimeo.cgi">try again</a></p>
EOR
ensure
  print <<EOF
<p>
<a href="/cgi/gimeo.cgi">back</a>
</p>
<hr>
hkimura, 0.4
</div>
</body>
EOF
end
