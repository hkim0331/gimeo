#!/usr/bin/env ruby
# coding: utf-8
require 'cgi'
require 'sequel'
require './common'

def index()
  print <<EOF
<ul>

<div class='dotted'>
<h4>見る</h4>

<p><a class='btn btn-success' href="./gimeo.cgi?cmd=list">
      アップロード順</a></p>
<p><a class='btn btn-success' href="./gimeo.cgi?cmd=list&by=sid">
      学生番号順</a>
<p><a class='btn btn-success' href="./gimeo.cgi?cmd=list&by=univ">
      大学別</a></p>
</div>

<p></p>

<form method='post' enctype='multipart/form-data' class='dotted'>
<h4>アップロード</h4>
<p>gif ファイル <input class='btn' name="file" type="file"></p>
<p>学生番号 <input name="sid"></p>
<p>タイトル <input name="title"></p>
<p>合言葉は <input name="secret"></p>
<p><input class='btn btn-primary' type="submit" value="アップロード"></p>
</form>
EOF
end

def list(by)
  case by
  when /sid/
    list_by_sid()
  when /univ/
    list_by_univ()
  else
    list_all()
  end
end

def encode(sid)
  sid.gsub(/./,"*")
end

def list_by_univ()
  list_by_univ_aux("東筑紫短大", 173000, 174000)
  list_by_univ_aux("下関市立大", 150000, 170000)
  list_by_univ_aux("九工大", 14000000, 18000000)
end

def list_by_univ_aux(univ, low, high)
  puts "<h3>#{univ}</h3>"
  DB[:gifs].where(:sid => low..high, stat: true).each do |w|
    print <<EOA
<a href="/upload/#{w[:id]}.gif" class="btn btn-default">
#{w[:title]}</a>&nbsp;
EOA
  end
end

def list_by_sid()
  works = Hash.new()
  titles = Array.new
  DB[:gifs].where(stat: true).each do |r|
    if works[r[:sid]].nil?
      works[r[:sid]] = [r[:id]]
    else
      works[r[:sid]].push(r[:id])
    end
    titles[r[:id]] = r[:title]
  end
  puts "<ul>"
  works.keys.sort.each do |sid|
    print "<li>#{encode(sid)}: "
    works[sid].each do |w|
      print <<EOA
<a href="/upload/#{w}.gif" class="btn btn-default">#{titles[w]}</a>&nbsp;
EOA
    end
    puts "</li>"
  end
  puts "</ul>"
end

def list_all()
  puts "<p>go to <a href='#tail'>bottom</a> of this page</p>"
  puts "<ol>"
  DB[:gifs].where(stat: true).each do |r|
    comments = ""
    DB[:comments].where(gif_id: r[:id]).each do |c|
      comments << " " << c[:comment]
    end
    print <<EOL
<li><a class='btn btn-default' href="/upload/#{r[:id]}.gif">#{r[:title]}</a>
#{comments}
<a href='/cgi/gimeo.cgi?cmd=comment&c=#{r[:id]}'>
<img src="/good.png"></a>
</li>
EOL
  end
  puts "<a name='tail'>&nbsp;</a>"
  puts "</ol>"
end

def upload(cgi)
  raise "合言葉忘れたな！" unless cgi['secret'] =~ /love/
  original_filename = cgi['file'].original_filename
  raise "アップロードするのは gif ファイルです。" unless original_filename =~/\.gif$/
  sid = cgi['sid'].read
  raise "学生番号を入力してください。" if sid.empty?
  raise "学生番号を確認してください。#{sid}?" unless sid =~ /^\d{6,8}$/
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
#  puts '"<p><a href="/cgi/gimeo.cgi?cmd=list">見る</a></p>'
end

#
# main
#
cgi = CGI.new
puts BOOTSTRAP
puts "<h1>GIF AMINE</h1>"

begin
  if cgi.request_method =~ /GET/
    if cgi['cmd'] == "list"
      list(cgi['by'])
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
<p>やり直すにはブラウザの「戻る」ボタンで</p>
EOR
ensure
  print <<EOF
<hr>
hkimura, 0.6, 2017-05-24, 2018-04-22.
</div></body></html>
EOF
end
