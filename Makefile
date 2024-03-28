.POSIX:
.SUFFIXES:

all: fmt test lint

fmt:
	ruff format

test:
	python3 -m unittest -v

lint:
	ruff check

mypy:
	mypy .

# run `make pre-commit` once to install the hook.
pre-commit: .git/hooks/pre-commit fmt test lint mypy
	git diff --exit-code

.git/hooks/pre-commit:
	echo "make pre-commit" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
