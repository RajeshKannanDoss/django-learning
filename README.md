Work_training repository - Django, database don't exist.

After cloning or download repository you need to:
python3 manage.py makemigrations
python3 manage.py sqlmigrate fifa_league 0001
python3 manage.py migrate

In addition:
python3 manage.py createsuperuser


App list:
- fifa_league
