if File.exists?("/srv/gimeo/public/upload")
  UPLOAD = "/srv/gimeo/public/upload"
  DB = Sequel.connect("mysql2://#{ENV['GIMEO_USER']}:#{ENV['GIMEO_PASS']}@db.melt.kyutech.ac.jp/gimeo")
else
  UPLOAD = "./upload"
  DB = Sequel.sqlite("../gimeo.db")
end

BOOTSTRAP =<<EOH
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
  <style type="text/css">
  code {white-space: pre;}
  .dotted { border: dotted 1pt; padding: 10px;}
  </style>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
</head>
<body><div class="container">
EOH
