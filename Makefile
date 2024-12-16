test:
	python3 -m unittest discover

format:
	black .

installdb:
	python3 install.py

deepclean:
	rm -rf ./venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./main.spec

dev:
	python3 main.py

build:
	pyinstaller --onefile --hidden-import=psycopg2 --hidden-import=json --add-data "./venv/lib/python3.12/site-packages/psycopg2:psycopg2" main.py

dock-postgres:
	docker run --name postgres-farm -e POSTGRES_USER=farm -e POSTGRES_PASSWORD=farm -e POSTGRES_DB=farm -p 5432:5432 -d postgres

clean-build:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./main.spec

db-start:
	docker container start postgres-farm

db-stop:
	docker container stop postgres-farm