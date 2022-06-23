
<h1 align="center">
  <br>
  <a href="http://www.amitmerchant.com/electron-markdownify"><img src="./readme_assets/logo-removebg-preview.png" alt="Markdownify" width="200"></a>
  <br>
  Cluster Storage
  <br>
</h1>

<h4 align="center">A storage solution to ensure redundancy and reliability for everyday applications.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Set Up Client</a> •
  <a href="#download">How To Set Up Nodes</a> •
  <a href="#license">License</a>
</p>


![screenshot](./readme_assets/upload-and-delete.gif)

## Key Features

* GUI Application for client
* Redundancy
* Cross-platform GUI
  - Windows, macOS and Linux ready.
* Nodes need to be run on unix based systems such as Ubuntu/

## How To Set Up Client

To clone and setup this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed on your computer. From your command line:

```bash
# Clone this repository
$ sudo git clone https://github.com/ZacharyLincoln/ClusterStorage /serv/Cluster

# Install the requirements with pip
$ pip install -r requirements.txt 

# Run gui
$ python3 <path to repository>/Client/gui.py
```

## How To Set Up Nodes

To clone and setup nodes on Ubuntu, you'll need [Git](https://git-scm.com) installed on your server. From your command line:

### Master Node
```bash
# Clone this repository
$ sudo git clone https://github.com/ZacharyLincoln/ClusterStorage /serv/Cluster

# Run setup script
$ sudo bash /serv/Cluster/MasterNode/setup.sh
```
> **Note**
> setup.sh will reboot your server

After the server is rebooted the node should start whenever the server starts.

### Node
```bash
# Clone this repository
$ sudo git clone https://github.com/ZacharyLincoln/ClusterStorage /serv/Cluster

# Run setup script
$ sudo bash /serv/Cluster/Node/setup.sh
```

> **Note**
> setup.sh will restart your server

After the server is rebooted the node should start whenever the server starts.

## License

MIT

---
> [zlincoln.dev](https://www.zlincoln.dev) &nbsp;&middot;&nbsp;
> GitHub [@ZacharyLincoln](https://github.com/ZacharyLincoln)

