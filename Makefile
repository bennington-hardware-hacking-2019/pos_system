init:
	pip3 install -r requirements.txt

run:
	python3 main.py

db-setup:
	sudo apt-get update
	sudo apt install postgresql
	./db/setup.sh

test:
	nosetests tests
