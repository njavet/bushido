# bushido
python textual app with telethon to track progress in various activities like training and study time

## Setup
`./bushido` is the root directory

```
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
python bushido/app.py
```

## Tests
```
export PYTHONPATH='bushido/'
python -m unittest discover -s tests/
```

## TODO
* unithistory weeks, collapsible
* stats for every unit
* unit delete function

