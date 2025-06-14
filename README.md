# django_final
Final project for NCHU django course

## Setup

### Clone the repository.
```
git clone https://github.com/hlc23/django_final.git
cd django_final
```

### Create a virtual environment. (Optional but recommended)
venv or other virtual environment tools can be used.
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Migrate the database.
```
python manage.py makemigrations
python manage.py migrate
```

### Run the server.
```
python manage.py runserver
```