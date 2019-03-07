Sample Tax Api built with Python Flask and Mysql

### Quick Start

  1. Run `docker-compose up`
  2. Visit `http://localhost:8080/apidocs` in your browser for the api specs
  3. For testing, inside the container app run `python testing.py`
 
### DB structure:  
#### Tax Table 
Column | Type | Nullable | Description 
--- | --- | --- | --- 
id | integer |  No | primary key 
name | character varying (200) | No | name of the tax object 
tax_code | integer | No | code of the tax object (only [1, 2, 3] are allowed) 
price | integer | No | price of the tax object
