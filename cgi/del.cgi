#!/usr/local/bin/ruby
# coding: utf-8
# under construction, 2017-05-05 15:52

require 'cgi'
require 'sequel'
require './common'

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
puts BOOTSTRAP
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
</div></body></html>
EOF
end
