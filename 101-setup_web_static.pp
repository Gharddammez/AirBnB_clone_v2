# Configures a web server for deployment of web_static.

# Nginx configuration file
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
} ->

file { '/data':
  ensure  => 'directory',
} ->

file { '/data/web_static':
  ensure => 'directory',
  require => File['/data'],
} ->

file { '/data/web_static/releases':
  ensure => 'directory',
  require => File['/data/web_static'],
} ->

file { '/data/web_static/releases/test':
  ensure => 'directory',
  require => File['/data/web_static/releases'],
} ->

file { '/data/web_static/shared':
  ensure => 'directory',
  require => File['/data/web_static'],
} ->

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
  require => File['/data/web_static/releases/test'],
} ->

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  require => File['/data/web_static'],
} ->

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

file { '/var/www':
  ensure => 'directory',
} ->

file { '/var/www/html':
  ensure => 'directory',
} ->

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n",
} ->

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
} ->

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
  notify => Exec['nginx_restart'],
} ->

service { 'nginx_restart':
  command => 'service nginx restart',
  require => File['/etc/nginx/sites-available/default'],
}
