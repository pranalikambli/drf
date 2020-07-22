# drf
Django RESTful APIs 

Steps to run application

1) clone the application :- git clone 
2) set the virtual environment :- 
   for windows :- check url https://techpluslifestyle.com/technology/steps-to-install-django3-on-windows10/
      python -m venv env and 
   for ubuntu :- check url https://techpluslifestyle.com/technology/steps-to-install-django3-on-ubuntu/
    sudo apt-get install virtualenv
    virtualenv -p python3 env 
3) After virtual environment install packages using below command
   pip install -r requirement.txt
4) Configured the database in .env file
5) migrate the database using below command :
   python manage.py migrate
   
