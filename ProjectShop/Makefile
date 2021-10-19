migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

app:
	python manage.py startapp $(name) /$(name)

test_user:
	python manage.py createsuperuser

run:
	python manage.py runserver

dbshell:
	python manage.py dbshell

shell:
	python manage.py shell

test:
	python manage.py test

update:
	pip install -U -r requirements.txt

collect:
	python manage.py collectstatic --settings=$(SETTINGS) --noinput

install_hooks:
	pre-commit install -f --install-hooks
	git add .pre-commit-config.yaml

commit:
	git commit
