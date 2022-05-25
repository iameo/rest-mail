#Rest-Mail

#### a simple flask setup that features user authentication and authorization, and mail sending.

#### How to run:
- fork repo and clone; cd into folder on your machine
- rename .env-example to .env and populate accordingly
- ```cmd: pip install -r requirements.txt``` to get packages for this project
- ```cmd: python slov.py```


#### Routes
* localhost:5000/register [POST method]
  
  required json: ```{
        "username": "xxxx",
        "email": "xxxx@xx.com,
        "password": "*****",
        "password2": "*****"
    }```

* localhost:5000/login [POST method]

    required json: ```{
        "username": "xxxx",
        "password": "*****"
    }```

* localhost:5000/check-auth [GET Method]

* localhost:5000/logout [GET method]
