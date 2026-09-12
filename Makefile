PY ?= python3

install:
	$(PY) -m pip install -r hands/requirements.txt -r voice/requirements.txt

test:
	cd brain && $(PY) test_guard.py

demo:
	cd hands && $(PY) -m uvicorn app:app --host 0.0.0.0 --port 8000
