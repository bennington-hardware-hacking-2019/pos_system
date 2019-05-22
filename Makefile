init:
	sudo pip3 install -r requirements.txt

demo:
	./db/setup.sh
	sleep 1
	python3 main.py

run:
	python3 main.py

db-setup:
	# sudo apt-get update
	# sudo apt-get install postgresql
	# sudo apt-get install libpq-dev
	./db/setup.sh

test:
	nosetests tests
