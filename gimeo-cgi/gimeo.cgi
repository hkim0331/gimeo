#!/usr/bin/ruby
# coding: utf-8
require 'cgi'
require 'sequel'

# production
UPLOAD = "/srv/gimeo/public/upload"
DB = Sequel.connect("mysql2://#{ENV['GIMEO_USER']}:#{ENV['GIMEO_PASS']}@dbs.melt.kyutech.ac.jp/gimeo")

#development
#UPLOAD = "./upload"
#DB = Sequel.sqlite("gimeo.db")
#

def index()
  print <<EOF
<ul>

<li><a class='btn btn-primary' href="./gimeo.cgi?cmd=list">見る</a></li>

<li>アップロード

<form method='post' enctype='multipart/form-data'
  style='border:dotted 1pt; padding:10px;'>
<p>gif ファイル <input class='btn' name="file" type="file"></p>
<p>学生番号 <input name="sid"></p>
<p>タイトル <input name="title"></p>
<p><input class='btn btn-primary' type="submit" value="アップロード"></p>
</form>
</li>

</ul>
EOF
end

def list()
  puts "<ol>"
  DB[:gifs].where(stat: true).each do |r|
    name = "#{r[:id]}.gif"
    comments=""
    DB[:comments].where(gif_id: r[:id]).each do |c|
      comments << " " << c[:comment]
    end
    print <<EOL
<li><a class='btn btn-default' href="/upload/#{name}">#{r[:title]}</a>
#{comments}
<a href='/cgi/gimeo.cgi?cmd=comment&c=#{r[:id]}'>
<img src="/good.png"></a>
</li>
EOL
  end
  puts "</ol>"
end

def upload(cgi)
  original_filename = cgi['file'].original_filename
  raise "アップロードするのは gif ファイルです。" unless original_filename =~/\.gif$/
  sid = cgi['sid'].read
  raise "学生番号を入力してください。" if sid.empty?
  title = cgi['title'].read
  raise "タイトルが空です。" if title.empty?
  now = Time.now.strftime("%F %T")
  id = DB[:gifs].insert(sid: sid, title: title, timestamp: now)
  upload = "#{UPLOAD}/#{id}.gif"
  raise "同じ名前のファイルがあります。やり直しましょう。" if File.exists?(upload)
  File.open(upload, "w") do |fp|
    cgi['file'].readlines.each do |line|
      fp.puts line
    end
  end
  print <<EOM
<p>アップロードできました。</p>
<p>見てみる？ &rArr; <a href="/cgi/gimeo.cgi?cmd=list">見る</a></p>
EOM
end

def comment(n)
  print <<EOF
<p>いいねコメントどうぞ</p>
<div style='border:dotted 1pt; padding:10px;'>
<form method='post'>
<input type='hidden' name='cmd' value='do'>
<input type='hidden' name='c' value='#{n}'>
<p><input name="comment">
<input type="submit" value="送信"></p>
</form>
</div>
EOF
end

def do_comment(cgi)
  DB[:comments].insert(gif_id: cgi['c'], comment: cgi['comment'],
                       timestamp: Time.now.strftime("%F %T"))
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

puts "<h1>GIF AMINE</h1>"

begin

  if cgi.request_method =~ /GET/
    if cgi['cmd'] == "list"
      list()
    elsif cgi['cmd'] == "comment"
      comment(cgi['c'])
    else
      index()
    end
  elsif cgi.request_method =~ /POST/
    if cgi['cmd'] == "do"
      do_comment(cgi)
    else
      upload(cgi)
    end
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
