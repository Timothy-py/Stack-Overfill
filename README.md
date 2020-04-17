# Stack-Overfill
This  a simple stack overflow web application clone, created with django framework.
It features the core functionalities of Stack Overflow which include the ability to-  
*   register to the site
*   login as a user
*   ask questions
*   post answer to a question if you're a user
*   view all the answers to a question
*   search the repository for questions on a particular topic
*   accept answer for a question you post
*   view questions asked for a particular day
*   and lots more.

## Tech Stack
*   Python Programming Language
*   Django Web Framework
*   PostgreSQL Database
*   Elasticsearch Search Engine

##  How to Setup
Follow the under-listed procedures to setup locally and to test this project on your local machine.

#### * Create a new directory on your local machine and setup a virtual environment inside it OR
#### * If you are using PyCharm IDE, just setup a new project environment.

#### * Activate the virtual environment

#### * Clone the project files into the directory on your local machine
git clone https://github.com/Timothy-py/Stack-Overfill.git

#### Install the dependencies
pip3 install -r requirements.txt

### Install PostgreSQL on your local machine
* Search online on how to install and setup PostgreSQL for your Operating System.
* After the installation is successful, create a database and a user for the database.
* Go to config/settings.py in your project directory and change the NAME, USERNAME and PASSWORD value  
    of the DATABASE dictionary to the one used to configure your database.

### Install Elasticsearch
* Search online on how to install and setup Elasticsearch for your Operating System.
* After the installation is successful, enable and start the elasticsearch server.

### Database Migration
* In your project directory run the following commands  
_python manage.py makemigrations_  
_python manage.py migrate_

### Create a Superuser
* Run the command
_python manage.py createsuperuser_

### Load Database into Elasticsearch
* Run the command
_python manage.py load_questions_into_elasticsearch_

### Start the django server
* Run the command
_python manage.py runserver_

### Go to your browser to interact with the app
_localhost:8000/home_

###### contact me @  adeyeyetimothy33@gmail.com