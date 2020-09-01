# How to setup BAT

## Step 1:
Install python
<br>
Python: 
https://www.python.org/downloads/


## Step 2:
Clone this repository
```
git clone "https://github.com/williamaredal/BAT"
```

## Step 3:
You can change ```SECRET_KEY``` used to encrypt the app in ```.env```, currently it's set to ```your_secret_key```.

The host, port and debug mode can be changed from ```host='127.0.0.1', port=8000``` in ```wsgi.py```, and further config additions/edits can be done in ```config.py```

## Step 4:
Starting BAT inside the directory
```
pip install pipenv
pipenv install
pipenv shell
python wsgi.py
```
Now BAT should be running and accessible on ```http://localhost:8000``` unless the port was changed

## Step 5:
Create a user, and/or log in. Then, using the input terminal, you can run the functions listed below:

```
 -test
 -logout
 -fillmodel
[optional title (optional)] -make
[dossier title] -update
[dossier title] -update
[search term]:[required instances (optional)] -search
[word1],[word2]:[required link strength (1-0) (optional)] -link
```

The commands above, except and ```logout``` can also be run using the first letter in the command name. For example:
```
 -t
 -fm (fillmodel)
[dossier title (optional)] -m
```
