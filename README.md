# flask_api_course
## ITVDN flask_api course

Web version of a part of this project available on [Heroku](http://flask-api-course.herokuapp.com/swagger/)
 
If you want test this project on your local machine run the following commands:

> git init
> 
> git clone https://github.com/RGBsrs/flask_api_course.git
> 
Then create virtual enviroment:

> virtualenv env

Activate this enviroment:

>On Linux/Mac
>> env/bin/activate
>>
>On Windows
>> env/Scripts/activate

Install all dependencies:
> pip install -r requirements.txt

Than you need assing you app to Flask with command:

>On Linux/Mac
>> set FLASK_APP=wsgi.py
>>
>On Windows
>> set FLASK_APP=wsgi.py

Than run migrations:

> flask db upgrade

And now you can start this app:

> flask run
