# Questioner

[![Build Status](https://travis-ci.com/tirgei/Questioner-API.svg?branch=develop)](https://travis-ci.com/tirgei/Questioner-API)
[![Coverage Status](https://coveralls.io/repos/github/tirgei/Questioner-API/badge.svg?branch=develop)](https://coveralls.io/github/tirgei/Questioner-API?branch=develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7988c2537aea4cf4b1a9db4089e0312f)](https://www.codacy.com/app/tirgei/Questioner-API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tirgei/Questioner-API&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/e1578991a4632d8dca6c/maintainability)](https://codeclimate.com/github/tirgei/Questioner-API/maintainability)

Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered.

The project is managed using [Pivotal Tracker](https://www.pivotaltracker.com). You can view the board [here](https://www.pivotaltracker.com/n/projects/2235446).

The repo for the frontend is available at [Questioner](https://github.com/tirgei/Questioner)

## Deployment
Website is hosted on [Questioner](https://tirgei.github.io/Questioner/UI) 

Project API demo is hosted on [Heroku](http://questioner-adc.herokuapp.com)

## Prerequisites

- [VS Code](https://code.visualstudio.com)
- [Python 3.6](https://www.python.org)
- [Insomnia](https://insomnia.rest) / [Postman](https://www.getpostman.com)

## Installation

- Clone the repo
```
$ git clone https://github.com/tirgei/Questioner-API.git
```

- CD into the folder
```
$ cd Questioner-API
```

- Create a virtual environment
```
$ python3 -m venv env
```

- Activate the virtual environment
```
$ source env/bin/activate
```

- Install dependencies
```
$ pip install -r requirements.txt
```

- Set the environment variables
```
$ mv .env.example .env
$ source .env
```

- Run the app
```
$ python run.py or flask run
```

- Testing
```
$ pytest --cov=app
```

## API Endpoints (V1)

| **HTTP METHOD** | **URI** | **ACTION** |
| --- | --- | --- |
| **POST** | `/api/v1/register` | Register a new user |
| **POST** | `/api/v1/login` | Login a user |
| **POST** | `/api/v1/refresh-token` | Refresh access token |
| **POST** | `/api/v1/logout` | Logout a user |
| **POST** | `/api/v1/meetups` | Create a meetup |
| **GET** | `/api/v1/meetups` | Fetch all upcoming meetups |
| **GET** | `/api/v1/meetups/<int:meetup_id>` | Fetch a specific meetup |
| **POST** | `/api/v1/<int:meetup_id>/<string:rsvp>` | RSVP to a meetup |
| **POST** | `/api/v1/questions` | Post a question to a specific meetup |
| **PATCH** | `/api/v1/questions/<int:question_id>/upvote` | Upvote a question |
| **PATCH** | `/api/v1/questions/<int:question_id>/downvote` | Downvote a question |

## Author

Vincent Kiptirgei - [Tirgei](https://tirgei.github.io)