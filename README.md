# HTTPLocalServerPractice


A project to demonstrate CRUD operations on a web server.

# **Installation and Configuration**


```commandline
python3 -m venv venv

# on Linux
source venv/bin/activate

# on Windows
source venv/Scripts/activate.bat

pip3 install -r requirements.txt
```
Go to HTTPLocalServerPractice/settings.py and modify the following
setting to configure the connection to mysql database:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<database-name>',
        'USER': '<user-name>',
        'PASSWORD': '<password>',
        'HOST': '<hostname>',
        'PORT': '<port-number>',
    },
}
```

# **Usage**

Start the Django server with:
```
python3 manage.py runserver
```




**Test**

Run tests with:
```
python3 manage.py test
```

# LICENSE

[MIT](LICENSE)








