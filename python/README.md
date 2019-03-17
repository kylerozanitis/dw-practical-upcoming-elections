# Upcoming Elections Practical
Full instructions for installing Flask can be found [here](http://flask.pocoo.org/docs/1.0/installation/)
otherwise:

```
pip install -r requirements.txt
```

## Running

```
export FLASK_APP=elections
export FLASK_ENV=development
flask run
```

## Testing

```
pytest
```

## External Libraries
- Requests
- JSON
- Unittest
- Functools
- Flask

## Current Functionality
- User can enter address to search for local elections
- System will parse the request to obtain the city and state
- System will query the TurboVote API to receive local election information
- System will present local election info to user if it exists
- System will inform user of no local elections if empty object returned
