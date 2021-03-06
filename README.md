# address-normalization-example
A simple example that shows how to use address normalization techniques.

## Installing an address normalization library

As this example uses [libpostal](https://github.com/openvenues/pypostal) to normalize the addresses by
calling it from [pypostal](https://github.com/openvenues/pypostal) wrapping python library, 
[follow this installation instructions](https://github.com/openvenues/pypostal#installation) before installing any Python package via pip:

```
sudo apt-get install curl autoconf automake libtool python-dev pkg-config

# Installing libpostal (See https://github.com/openvenues/pypostal#installation for more information)
git clone https://github.com/openvenues/libpostal
cd libpostal
./bootstrap.sh
./configure --datadir=[...some dir with a few GB of space...]
make
sudo make install

# On Linux it's probably a good idea to run
sudo ldconfig
```

After having completed that earlier libpostal installation instructions, create the virtualenv and install its requirements:

```sh
$ virtualenv -p python3 venv
$ ./venv/bin/activate
(venv)$ pip install requirements.txt
```

## Running the example

### Bad in-memory approach (do not use in production, kept for documenting and educational purposes)

```python3
python3 basic_merger.py data/exercise_part1.csv data/exercise_part2.csv output/output.csv
```

### Optimal file-based approach

```python3
python3 address_csv_merger.py data/exercise_part1.csv data/exercise_part2.csv output/output.csv
```


## Tests

Tests developed with pytest.

```sh
pytest
```

## TODOs and Roadmap
- Use other address normalization techniques:
  - Knowing the country would be helpful
    - We could be using some kind of geocoding service and normalize by its coordinates.
    - We could make a ad-hoc address normalization technique by country.
  - Using partial or fuzzy matching:  
    - Make use of [fuzzywuzzy](http://jonathansoma.com/lede/algorithms-2017/classes/fuzziness-matplotlib/fuzzing-matching-in-pandas-with-fuzzywuzzy/).
or any other fuzzy matching tool for pandas.
- Parallelize matching with multiprocessing. Take a look to [Processing large files using python](https://www.blopig.com/blog/2016/08/processing-large-files-using-python/).