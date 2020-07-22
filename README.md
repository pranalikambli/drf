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
6) Run the application 
   python manage.py runserver 
7) Open Register page and register yourself
   http://127.0.0.1:8000/api/rest-auth/registration/
8) After registration authorize yourself using:
   http://127.0.0.1:8000/api/doc/ :- Click on authorize button and authorize yourself using key or login.
9)You can now perform the api.
10)for /category/ use below json:
   eg
   {
      "name": "Home",
      "subcategory_of": ""
   }
   {
      "name": "Home Decor",
      "subcategory_of": "Home"
   }
11)For product
   eg,
   {
      "name": "abc",
      "price": "10.10",
      "categories": [17,18,19,20]
   }


   
