### Currencies log and analyser on API interfaces
###### example load currencies from bitfinex.com

##### Install  
```sh  
pip install -r requirements.txt  
export FLASK_APP=app.py  
```  
before other commands
  
##### Configure:
Use the `config.py` or `config.cfg` how instance config.
Fill SQLALCHEMY_DATABASE_URI or set next environment variables:
```sh
export DATABASE_NAME='' DATABASE_USER='' DATABASE_HOST='' DATABASE_PASSWORD='''
```  
for connect your DB, on PostgreSQL by default.


##### DB migrate:
```sh
flask db init  
flask db migrate  
flask db upgrade
```

##### Loading first data from fixtures:
```sh
flask first-filling
flask test-user
```
 
##### Crawl & write currencies from bitfinex.com

use after migrate
  
```sh  
flask load
```

##### Get start
```sh
flask run
```