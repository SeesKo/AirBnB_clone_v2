# Puppet manifest to configure Nginx to serve static files

# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { ['/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => directory,
}

# Create fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Set ownership to ubuntu user and group recursively
file { '/data/web_static':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Update Nginx configuration
file_line { 'hbnb_static_config':
  ensure => present,
  path   => '/etc/nginx/sites-available/default',
  line   => "        location /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n",
}

# Restart Nginx service
service { 'nginx':
  ensure     => running,
  enable     => true,
  subscribe  => File['/etc/nginx/sites-available/default'],
}
