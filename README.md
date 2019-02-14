# address-normalization-example
A simple example that shows how to use address normalization techniques.

## Installing an address normalization library

As this example uses [https://github.com/openvenues/pypostal](libpostal) to normalize the addresses by
calling it from [pypostal](https://github.com/openvenues/pypostal) wrapping python library, 
[follow this installation instructions](https://github.com/openvenues/pypostal#installation) before installing any Python package via pip.

After having completed that instructions:

```sh
$ virtualenv -p python3 venv
$ ./venv/bin/activate
(venv)$ pip install requirements.txt
```

## Running the example

### In-memory approach

```python3
python3 basic_merger.py data/exercise_part1.csv data/exercise_part2.csv output/output.csv
```
