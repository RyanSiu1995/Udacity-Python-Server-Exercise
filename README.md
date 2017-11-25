# Catalog Web Site in Flask
This is a udacity project 3, item catalog. This project aims at 
practising the server-side coding in python with Flask library.
The basic authentication with OAuth2 is also included in order to
protect the data inside the server.
## Enviroment
1. Python 2.7.1
	1. Flask
	2. SQLAlchemy
	3. BaseHTTPServer
2. PostgreSQL 9.6.6
## Installation
Step 1 - Install the required python libraries
`bash
pip install flask sqlalchemy BaseHTTPServer
`
Step 2 - Set up the database
Please create an admin account with password. The default acoount is
postgres with password admin. Then, you should create the database called
sample so that the database_setup.py can correctly point to your local 
database.
If you want to customize the account and database, you will have to change
the value of _sql_string inside database_setup.py.

Step 3 - Launch the server
You can then launch the server by the following script.
`bash
python webserver.py
`
The server will be hosted in port 5000 by default.
## Usage
The website provides the users with CRUD operations in the database after
logging in. Please use the facebook account to login through the button in 
top right hand corner. After logging in to the system, you can enjoy the 
CRUD operations with the item catalog.
Please note that you can either create the catalogs or items in the website.
You should create at least one catalogs first in order to organize the items
well.  
## API Provided
The system provides the user with URL /catalog.json. This API will server the users
with the JSON object of the items with joining the catalog name. The URL accepts the
query parameter raw. If raw is set to be 1, you will get the id of the 
catalog instead of the name of the catalog.