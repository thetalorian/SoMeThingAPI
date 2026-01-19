# SoMeThing API
The api portion of a Social Media Thing. This project is designed to be a demonstration of coding techniques and concepts for an upcoming series of How To articles and videos covering a variety of concepts and skills required for a DevOps Engineer. Because of that, this code is not intended to necessarily demonstrate the best or most performant way to design or implement this kind of API. It is a teaching tool, and not meant to actually represent software that could properly serve as a "real" social media site.

## Installation
Create a python virtual environment and activate it.

Install dependencies using:
```
pip install -r requirements.txt
```

Or, if you intend add to the code and run tests:
```
pip install -r requirements-dev.txt
```

## Running

To launch the API from the command line:
```
uvicorn app.main:app
```

During development you may want to automatically incorporate new code changes. In that case start with:
```
uvicorn app.main:app --reload
```

Alternately you can launch the API in a docker container with:
```
docker-compose up
```

## Documentation
Documentation for the API itself is automatically generated and can be found at http://127.0.0.1:8000/docs.
