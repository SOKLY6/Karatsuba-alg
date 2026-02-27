build:
	pip install uv
	uv venv
	source .venv/bin/activate
	uv sync

test:
	python3 test.py > report.txt

start:
	python3 cli.py