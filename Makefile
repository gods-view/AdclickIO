venv:
	if [ ! -d "venv" ]; then pip3 install virtualenv; virtualenv venv; fi
init:
	pip install -r requirements.txt
format:
	find ./gatekeeper -name '*.py' -exec autopep8 --in-place --aggressive --aggressive '{}' \;
test:
	nosetests tests
watch_run:
	npm run watch:run
