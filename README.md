# Mirror Check
Check if mirrors are updated and generate a status web page.

![Mirror Check Screenshot](https://user-images.githubusercontent.com/24390439/46643340-0798a080-cb52-11e8-84e9-60699b45090a.png)

## Installation

### Prerequisites
* lftp
* Python 3
* Python Pip
* Jinja2
* ruamel.yaml

### Ubuntu installation
You can easy install all the prerequisites on Ubuntu with the following lines:
```sh
sudo apt-get install lftp
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install --upgrade pip
sudo pip3 install Jinja2
sudo pip3 install ruamel.yaml
```

### Configuration
Edit the ```config.yaml``` file. You can replace the example names used and add more mirrors.
If you have a new template, edit the ```template``` name, that corresponds to the folder name inside ```/templates``` folder.

Edit the ```/conf``` folder files with the settings of each ```lftp``` connection. The ```.conf``` filename relates to the used in ```config.yaml``` file.

## Running
To generate the status web page, you can setup a ```cronjob``` with this command:
```sh
cd /mirror-check ; python3 generate.py
```
Replace the ```mirror-check``` directory with your installation path. Put the files of ```/webpage``` folder in a web server directory, or just create a symbolic link between them.

## Template
If you need modify the web page style, edit the ```template.j2``` file in the chosen template folder.
