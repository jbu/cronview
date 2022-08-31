# Cronview

Cronview takes a crontab(5) string and prints the expanded list of times from the string.
For example
```
*/15 0 1,15 * 1-5 /usr/bin/find
```
returns 
```
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

To run try

```bash
$ ./cronview "*/15 0 1,15 * 1-5 /usr/bin/find"
```

## Installation

There is a `Pipfile`, so if you have `pipenv` then

```bash
$ pipenv install
$ pipenv shell
```
will set up the correct environment

## Testing 

```bash
$ python -m unittest
```

## Other Checks

```bash
$ pipenv install --dev
$ flake8 .
$ mypy .
$ black .
```