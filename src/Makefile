all:
	@	echo Hello

run:
	python manage.py runserver 8081

migrations:
 	python manage.py makemigrations
	python manage.py migrate

venv:
	python3 -m venv core
	sudo ./core/bin/activate
	pip install django