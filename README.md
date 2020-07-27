# Products

Restful web service built using flask-restful to perform CRUD operation on product class.
Uses sqlite database.

### Setup (local)

#### Pre-requisites

1. Python3.6+ installed

#### Installation

1. Open up terminal and navigate to the `Products` folder
2. Execute the following commands:

```cmd

pip install -r requirements.txt

```

#### Verify installation

1. Execute the following command in a CMD window and check if all dependencies are installed.

```cmd
pip freeze
```

#### Running the application
1. Open up terminal and navigate to the `Products` folder
2. Execute the following commands:

```cmd

py -3 run.py
```

This should produce the following output

```
2018-12-02 19:38:13,848 INFO  * Restarting with stat
2018-12-02 19:38:14,440 WARNING  * Debugger is active!
2018-12-02 19:38:14,443 INFO  * Debugger PIN: 301-582-767
2018-12-02 19:38:14,454 INFO  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```
The endpoint would be as below:

http://127.0.0.1:5000/api/Product

## Usage
### List all products
**Request**
`GET http://127.0.0.1:5000/api/Product`
**Response**
`200 OK` on success
```json
{
    "status": "success",
    "data": [
        {
            "name": "xxxx",
            "description": "xxxxx",
            "brand": "xxxx",
            "product_code": "xxxx",
            "price": 111,
            "id": 1
        },
        {
            "name": "yyyy",
            "description": "yyyy",
            "brand": "yyyy",
            "product_code": "yyyy",
            "price": 222,
            "id": 2
        }
        ...
    ]
}
```
### Get Product by Name
**Request** 
`GET http://127.0.0.1:5000/api/Product?name=xxxx`
**Response**
`200 OK` on success
```json
{
    "status": "success",
    "data": [
        {
            "name": "xxxx",
            "description": "xxxxx",
            "brand": "xxxx",
            "product_code": "xxxx",
            "price": 111,
            "id": 1
        }
    ]
}
```

### Create new product 
**Request**
`POST http://127.0.0.1:5000/api/Product`
```json
{
	"name":"Galaxy S9",
	"description": "mobile phone",
	"product_code":"XWDSGXXADFGTHCV",
	"brand":"Samsung",
	"price":600
}
```
**Response**
`201 CREATED` on success
```json
{
    "status": "success",
    "data": {
        "name": "Galaxy S9",
        "description": "mobile phone",
        "brand": "Samsung",
        "product_code": "XWDSGXXADFGTHCV",
        "price": 600,
        "id": 2
    }
}
```

### Update Existing product 
**Request**
`PUT http://127.0.0.1:5000/api/Product`
```json
{
    "id": 2,
	"name":"Galaxy S10",
	"description": "mobile phone",
	"product_code":"XWDSGXXADFGTHCV",
	"brand":"Samsung",
	"price":600
}
```
**Response**
`200 OK` on success
```json
{
    "status": "success",
    "data": {
        "name": "Galaxy S10",
        "description": "mobile phone",
        "brand": "Samsung",
        "product_code": "XWDSGXXADFGTHCV",
        "price": 600,
        "id": 2
    }
}
```

### Delete Existing product 
**Request**
`DELETE http://127.0.0.1:5000/api/Product?id=2`

**Response**
`200 OK` on success
```json
{
    "status": "success",
    "data": {}
}
```
# Unit Testing

Start the application using the below steps.

1. Open up terminal and navigate to the `Products` folder
2. Execute the following commands:

```cmd

py -3 run.py
```

This should produce the following output

```
2018-12-02 19:38:13,848 INFO  * Restarting with stat
2018-12-02 19:38:14,440 WARNING  * Debugger is active!
2018-12-02 19:38:14,443 INFO  * Debugger PIN: 301-582-767
2018-12-02 19:38:14,454 INFO  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```
3. Open up a new terminal and navigate to the `Products\test` folder
4. Execute the following commands:

```cmd

py -3 test_helper.py
```
This should execute the unit tests and produce the following output


----------------------------------------------------------------------
Ran 10 tests in 0.356s

OK

