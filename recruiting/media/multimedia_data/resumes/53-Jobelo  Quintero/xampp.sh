sudo apt-get install gksu python-glade2
wget http://sourceforge.net/projects/xampp/files/XAMPP%20Linux/1.8.1/xampp-linux-1.8.1.tar.gz
sudo tar xvfz ./xampp-linux-1.8.1.tar.gz -C /opt
sudo cp /opt/lampp/htdocs/xampp/img/logo-small.jpg /opt/lampp
wget http://ubuntuone.com/1pO0S8MltiwMefW9hatVvZ
tar xvfz ./1pO0S8MltiwMefW9hatVvZ -C ~/.local/share/applications
rm ./1pO0S8MltiwMefW9hatVvZ
wget http://ubuntuone.com/11E8I5t6YgLNxCiUkShzTw
sudo tar xvfz ./11E8I5t6YgLNxCiUkShzTw -C /opt/lampp/etc/extra
rm ./11E8I5t6YgLNxCiUkShzTw
sudo chmod a+w /opt/lampp/htdocs -R
sudo chmod -R 0755 /opt/lampp/htdocs
ln -s /opt/lampp/htdocs ~/
sudo /opt/lampp/lampp start
nohup xdg-open http://localhost/
rm ./nohup.out
