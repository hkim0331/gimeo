if File.exists?("/srv/g2/public/upload")
  UPLOAD = "/srv/g2/public/upload"
  DB = Sequel.connect("mysql2://#{ENV['GIMEO_USER']}:#{ENV['GIMEO_PASS']}@db.melt.kyutech.ac.jp/g2")
else
  UPLOAD = "/srv/g/upload"
  DB = Sequel.sqlite("/srv/g/gimeo.db")
end

BOOTSTRAP =<<EOH
content-type: text/html

<!DOCTYPE html>
<html>
<head>
  <meta charset=utf-8">
  <meta name='viewport' content='width=device-width, initial-scale=1.0' />
  <meta http-equiv='X-UA-Compatible' content='IE=edge' />
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta http-equiv="Content-Style-Type" content="text/css" />
  <meta name="generator" content="pandoc" />
  <title>index</title>
  <style type="text/css">
  code {white-space: pre;}
  .dotted { border: dotted 1pt; padding: 10px;}
  input.comment { width: 30em; }
  </style>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body><div class="container">
EOH
