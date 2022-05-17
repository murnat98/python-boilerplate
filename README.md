# Python boilerplate

A Python boilerplate with
- [isort](https://pycqa.github.io/isort/)
- [black](https://black.readthedocs.io/en/stable/index.html)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [pre-commit](https://pre-commit.com/)
- [commitizen](https://commitizen-tools.github.io/commitizen/)

## Requirements

- [Python 3.9](https://www.python.org/downloads/release/python-390/)
- [Poetry 1.1](https://python-poetry.org/docs/#installation)

## Installation

```bash
git clone https://github.com/murnat98/python-boilerplate.git
cd /path/to/project/
poetry install
poetry run poe git-hooks
```

## Development

### Test
```bash
poetry run poe test
```