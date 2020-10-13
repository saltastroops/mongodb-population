## Setting up the server

Since this a Python project, we must have Python installed and ensure it's of the latest version. To check your Python
 version, run the following command:
 
 ```bash
python3.8 -V
```
Then we need to have a virtual environment for our project. To add the virtual environment, we run the following 
command:
```bash
pip3 install virtualenv
```
Then inside our project folder, run the following:
```bash
virtualenv venv
```
We then proceed to install the required packages for our project using the virtual environment, but first we activate it
using the following:
```bash
source venv/bin/activate
``` 
Then we proceed with installing the packages required for the project. This project will require these following modules
to be installed:
1. Flask
2. gunicorn
3. Supervisor

To install Flask, run this command:
```bash
pip install Flask
```
To install gunicorn, run this command:
```bash
pip install gunicorn
```
Then we deactivate our virtual environment by running
```bash
deactivate
```
We then need to install Supervisor, we run the following command:
```bash
sudo apt-get install supervisor
```
This is just for the  initially, so inside our project folder, we can create a new python file, for example,
myproject.py, and the file can be like so:

```bash
rom flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello, World!</h1>"

if __name__ == '__main__':
   app.run(host='0.0.0.0')
```
Next, we create a new file, called wsgi.py, which will act as our entry point to our 
application. A sample of the file would look like so:

```
from app import app as application
if __name__ == '__main__':
     app.run()
```
Since we use gunicorn in this project, we need to create a configuration file for it. The following represent a sample 
of what that file might look like. We choose the directory /etc to store the file.

```bash
import os
import multiprocessing

_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..'))
_VAR = os.path.join(_ROOT, 'var')
_ETC = os.path.join(_ROOT, 'etc')

errorlog = "-"
accesslog = "-"

# bind = 'unix:%s' % os.path.join(_VAR, 'run/gunicorn.sock')
bind = '0.0.0.0:5000'
# workers = 3
workers = multiprocessing.cpu_count() * 2 + 1

timeout = 3 * 60  # 3 minutes
keepalive = 24 * 60 * 60  # 1 day

capture_output = True 
```
Back inside our project folder, we create a new file called run.sh, this will start our virtual environment automatically
for us, the following is a sample file:

```bash 
#!/bin/bash -e

if [ -f venv/bin/activate ]; then
   echo   "Load Python virtualenv from 'venv/bin/activate'"
   source venv/bin/activate
fi
exec "$@"
```

The program configuration files for Supervisor programs can be found in the /etc/supervisor/conf.d directory, normally with
one program per file and a .conf extension. We then go this directory and create a new file for our project, the 
following is a sample of what the file might look like:

```bash
[program:myproject]
startretries=10
exitcodes=1
autostart=true
stderr_logfile=/var/log/supervisor/test.err.log
stdout_logfile=/var/log/supervisor/test.out.log
command={project path}/run.sh gunicorn -c /etc/gunicorn.conf.py wsgi
directory=/home/upsource/web_manager
user=www-data
```
In the file sample above "[program:myproject]", "myproject" matches the name of the python file created in our project
folder "myproject.py", if you create a file with a different name, then this part would need to change as well.

The line "directory=/home/upsource/web_manager", this is where your project folder is and should be changed according to
your project location, {project path} is the directory where your project is and would need to change accordingly as per
user needs.

We then need to install nginx, we run the following command:
```bash
sudo apt install nginx
```
We now  nginx is running with the command ```service nginx status```, if it passes, you can ope your browser and enter 
the url http://{server_ip}, you should see some welcome message from **nginx**.

Next, we configure **nginx** by running the following commands:
```bash
sudo touch /etc/nginx/sites-available/api_project
sudo ln -s /etc/nginx/sites-available/api_project /etc/nginx/sites-enabled/api_project
sudo nano /etc/nginx/sites-available/api_project
```
In the commands above 'ap_project' can be replaced with file name of your choice. Below is a sample for the
configuration file of **nginx**:

```bash
server {
    listen      80;
    server_name api.example.com;
    location / {
        proxy_pass         "http://localhost:5000";
        proxy_redirect     off;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        fastcgi_read_timeout 300s;
        proxy_read_timeout 300;
    }
    location /static {
        alias  /opt/deployment/my-api-app/static/;
    }
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;
}
```
Now we install MongoDB. First check the ubuntu release on your system as the installation varies per release. 
The following installation can be done on Linux Ubuntu 20.04 LTS("Focal").

Import the public key used by the package management system.
From the terminal, issue the following command,so we can import the MongoDB public GPG key from
[MongoDB] https://www.mongodb.org/static/pgp/server-4.4.asc.

```bash
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
```
The operation should respond with an OK.

Next, run the following commands:
```bash
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
```
```bash
sudo apt-get install -y mongodb-org
```

Then we must check which init system your Linux platform uses by running the following command:
```bash
ps --no-headers -o comm 1
```
For Ubuntu 20.04("Focal"), the init system is systemd(systemctl), so we start MongoDB with it. Then run the following 
commands to start MongoDB and check its status.

```bash
sudo systemctl start mongod.service
sudo systemctl status mongod
```
The following is s a sample output indicating that the service is up and running
```bash
mongod.service - MongoDB Database Server
     Loaded: loaded (/lib/systemd/system/mongod.service; disabled; vendor preset: enabled)
     Active: active (running) since Tue 2020-06-09 12:57:06 UTC; 2s ago
       Docs: https://docs.mongodb.org/manual
   Main PID: 37128 (mongod)
     Memory: 64.8M
     CGroup: /system.slice/mongod.service
             └─37128 /usr/bin/mongod --config /etc/mongod.conf
```
After confirming that the service is running as expected, enable the MongoDB service to start up at server boot:
```bash
sudo systemctl enable mongod
```

We then restart **nginx** with the command the following commands:
 ```bash
sudo nginx -t
sudo service nginx restart
  ```

Now, you should access your application through port 80 with your domain name: http://domain-name.
