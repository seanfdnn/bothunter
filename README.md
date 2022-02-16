# Twitter Bot Hunter
This repository contains Python scripts for running useful commands against the Twitter API for conducting research on bot farms.

# Prerequisites
* [Python 3.7 or higher](https://www.python.org)
* [Pipenv](https://pipenv.pypa.io/en/latest/)
* [Twitter Developer API account and API key](https://developer.twitter.com/) You are responsible for complying with Twitter's Terms of Use

## Getting Started
* Clone this repository
* Change to this directory `cd bothunter`
* Run `pipenv install` to install all Python dependencies
* Create a `config.ini` file with the Twitter API Bearer token:
```
[Twitter]
BEARER_TOKEN=redacted
```

# Usage
## Creating a list of a user's followers

Because of Twitter's rate-limiting, requests over a few thousand followers must be done in batches with 15-minute waiting periods in-between.
The script will automatically handle this wait period. An account of 200k followers typically takes about 4-5 hours to fetch all followers.

Run the command:
```
pipenv run get-followers @jack
```

The output will be placed in a CSV file in the current working directory.
 
