#!/usr/bin/env bash
# Sets up web servers for deployment of web_static

# Installing Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Creating necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Creating fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Creating symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Giving ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Updating Nginx configuration to serve static files correctly
config_file="/etc/nginx/sites-available/default"
sudo sed -i "/^\tlocation \/ {/a \\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" "$config_file"

# Restarting Nginx
sudo service nginx restart
