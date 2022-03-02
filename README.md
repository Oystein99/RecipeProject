# How to start the server
The server is running on localhost by default at port 8000. Use chrome as the web browser! We have encountered different browser compatabilities.
 - python3 manage.py runserver
 - http://127.0.0.1:8000/

# Other
 - python3 manage.py migrate
 - python3 manage.py makemigrations
 - python3 manage.py test

# Admin user
 - admin/admin

# Installs
In order to run the server one needs python or python 3 with django, pillow, and nltk installed. Further libraries are used for tests.

## Python and django
- sudo apt install python3
- sudo apt install pip3
- pip3 install django

## Prerequisites
 - pip3 install pillow
 - pip3 install nltk

## Other
 - pip3 install selenium
 
## Geckodriver
Newest release is avaible at https://github.com/mozilla/geckodriver/releases  
Ubuntu instructions (may require sudo privileges):
1. Download the newest 64x .tar.gz release
2. Unzip it using: tar -xvzf geckodriver-vX.XX.X-linux64.tar.gz
3. Change file permissions: chmod +x geckodriver
4. Add file (geckodriver) to PATH or workspace directory
