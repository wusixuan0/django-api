quick start
```
source venv/bin/activate
doppler run -- python manage.py runserver
```
http://127.0.0.1:8000/api/persons/  
```
doppler run -- python manage.py makemigrations
doppler run -- python manage.py migrate
```

running with Gunicorn for render.
```
doppler run -- python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```
http://127.0.0.1:8000/api/hello/  
get started
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export DOPPLER_TOKEN='dp.st.dev.'
doppler run --config dev -- python manage.py runserver
```
instead of token
```
doppler login
doppler setup
```
```
export DOPPLER_TOKEN='dp.st.prd'
```  
doppler get started:  
https://github.com/wusixuan0/seed-supabase/blob/main/README.md  

tutorial steps:  
```
touch django-api
cd django-api
# Create a virtual environment to isolate our package dependencies locally
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework && pip freeze > requirements.txt
// Create the Django project in the current directory
django-admin startproject config .
python manage.py startapp api
```

Your project structure should now look like this:
```
my-project/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── venv/
└── requirements.txt
```


```
touch api/urls.py

```
add app route to config/urls.py  
add Hello World to api/urls.py  
http://127.0.0.1:8000/api/hello/

