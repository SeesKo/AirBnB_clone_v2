# Puppet manifest to configure Nginx to serve static files

# Nginx configuration
$nginx_configuration = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index  index.html index.htm;

    # Redirect block
    location /redirect_here {
        return 301 https://example.com;
    }

    # Static content block
    location /static_content {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    # Error handling
    error_page 404 /404_page.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

# Install Nginx package
package { 'nginx':
  ensure   => 'installed',
  provider => 'apt'
} ->

# Create directories
file { '/data_directory':
  ensure  => 'directory'
} ->

file { '/data_directory/web_static_directory':
  ensure => 'directory'
} ->

file { '/data_directory/web_static_directory/releases':
  ensure => 'directory'
} ->

file { '/data_directory/web_static_directory/releases/test':
  ensure => 'directory'
} ->

file { '/data_directory/web_static_directory/shared':
  ensure => 'directory'
} ->

# Create a fake HTML file
file { '/data_directory/web_static_directory/releases/test/fake_index.html':
  ensure  => 'present',
  content => "Holberton School\n"
} ->

# Create symbolic link
file { '/data_directory/web_static_directory/symlink_to_current':
  ensure => 'link',
  target => '/data_directory/web_static_directory/releases/test'
} ->

# Change ownership
exec { 'change_ownership':
  command => 'chown -R ubuntu:ubuntu /data_directory/',
  path    => ['/usr/bin', '/bin'],
}

# Create directories for web server
file { '/var/www':
  ensure => 'directory'
} ->

file { '/var/www/html':
  ensure => 'directory'
} ->

# Create index.html file
file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School\n"
} ->

# Create custom 404 page
file { '/var/www/html/404_page.html':
  ensure  => 'present',
  content => "This is a custom 404 page\n"
} ->

# Configure Nginx
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_configuration
} ->

# Restart Nginx
exec { 'restart_nginx':
  command => '/etc/init.d/nginx restart',
  path    => ['/usr/sbin', '/usr/bin', '/sbin', '/bin'],
}
