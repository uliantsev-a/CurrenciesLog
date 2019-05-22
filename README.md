### Currencies log and analyser on API interfaces  
###### This app is example load currencies from bitfinex.com using their [API](https://docs.bitfinex.com/v2/reference)  
  
##### API endpoints  

- Getting rate info by currency with average between last 10 days, by default
_/api/rate/<id_currency>_

- Getting list currencies with the option paginate  
_/api/currencies?page=\<num\>&perPage=\<num\>_  
____  
##### Install    
```sh  
pip install -r requirements.txt  
export FLASK_APP=app.py  
```  
  
##### Configure:  
Use the `config.py` or `instance/config.cfg` how instance config.
Fill SQLALCHEMY_DATABASE_URI or set next environment variables:
```sh
export DATABASE_NAME='' DATABASE_USER='' DATABASE_HOST='' DATABASE_PASSWORD=''
```  
for connect to your DB. Uses PostgreSQL by default.


##### DB migrate:
```sh
flask db init  
flask db migrate  
flask db upgrade
```

##### Loading first data from fixtures:
If you want add anything currency you should fill fixtures in `make_default_currency` inside `project/fixtures.py`.   
Currency should be available on _bitfinex.com_.

```sh
flask first-filling
flask test-user
```
User for testing have next login and password _test:test_
 
##### Crawl & write rates 
Loading the rates from bitfinex.com by all currency from database 
  
```sh  
flask load
```

##### Get start
```sh
flask run
```