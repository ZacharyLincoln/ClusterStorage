sudo apt install python3-flask -y
sudo git clone https://github.com/ZacharyLincoln/TempCluster /serv/Cluster/

crontab -l > tempcron
echo "@reboot bash /serv/Cluster/MasterNode/start.sh" > tempcron
crontab tempcron
rm tempcron

reboot now