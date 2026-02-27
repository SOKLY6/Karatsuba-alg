build:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv venv
	uv sync

test:
	python3 test.py > report.txt

start:
	python3 cli.py