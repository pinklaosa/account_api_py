docker-start:
	@ echo "> Start development environment"
	@ docker-compose up -d --build

docker-stop:
	@ echo "> Stop development environment"
	@ docker-compose down

clean:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +