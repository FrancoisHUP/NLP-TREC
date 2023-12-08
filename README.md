# NLP TREC

## Installation

### Download

Before starting you must have the [TREC AP 88-90](https://drive.google.com/file/d/1cwskOAZ9gHAgHl_nPtKfwxSJQ6lR33KI/view) directory at the root directory.

### Create Virtual env

```bash
$ python -m venv .venv/
$ source .venv/Scripts/activate
$ pip install -r requirements.txt
```

## Commands

Run all tests

```bash
$ python src/main.py
```

Run single test.

```bash
$ python src/main.py -n -t base_nf_short
```

**NOTE:** You must at least download the Nltk data once. After you can lauch the program with -n, --no-download

### CLI Help

```bash
$ python src/main.py -h
```
