# Puppet manifest to configure Nginx to serve static files

# Package installation
package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
}

# Directory structure setup
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/releases/test', '/data/web_static/shared']:
  ensure => 'directory',
}

# Web server directory setup
file { '/var/www':
  ensure => 'directory',
}

# Nginx configuration
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
        return 301 https://th3-gr00t.tk;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf,
}

# File content setup
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School\n",
}

# Web server file content setup
file { ['/var/www/html/index.html', '/var/www/html/404.html']:
  ensure  => 'present',
  content => "Holberton School\n",
}

# Symbolic link creation
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# File ownership adjustment
exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}

# Nginx restart
exec { 'nginx restart':
  path => '/etc/init.d/',
  refreshonly => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
