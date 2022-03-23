# diskspace-monitor-CRUD

<p align="center" width="100%">
    <img width="33%" src="fast.png">

    [![Diskspace Monitor Test Suite](https://github.com/NHopewell/diskspace-monitor-CRUD/actions/workflows/tests.yml/badge.svg)](https://github.com/NHopewell/diskspace-monitor-CRUD/actions/workflows/tests.yml)

</p>

## Background

The build system is part of a large environment with a multitude of different components. Many of the components have some sort of storage (examples: crash dump handler, versioning system, build distribution). To ensure none of the services go down due to a lack of available storage, the systems have an agent that reports disk usage back to a central monitoring facility, which evaluates the collected data against preset rules and provides status and warnings through API endpoints.

The current project implements this central monitoring facility.

To read **API Documentation**, see `API_Documentation.md`.

## Getting Started Without Docker

### Prerequisites

Python >= 3.8 and pip are the only prerequisite. I personally use Pipenv but have provided a requirements.txt file for pip.

```
pip install --upgrade pip
```

## Installation

1. Clone the repo

```
git clone  https://github.com/NHopewell/diskspace-monitor-CRUD

cd diskspace-monitor-CRUD
```

2. Create a virtual environment of your choice (in this example, venv)

```
python -m venv env
```

3. Activate the virtual environment

```
source env/bin/activate
```

4. Install the source package in the virtual environment

```
pip install -e .
```

5. Install requirements in virtual environment. If you would like to
   run tests and add onto the project, install the requirements_dev file instead.

```
# prod requirments
pip install -r requirements.txt

# dev requirements
pip install -r requirements_dev.txt
```

## Usage

The application code which powers the API can be found in `src/diskspacemonitor/`. To run the webserver:

```
cd src/diskspacemonitor/

uvicorn main:app --reload
```

Now our monitoring system is being served over localhost. You can run my test script which automates sending requests to each end point:

```
python scripts/example_automated_api_calls.py
```

This script posts some system components and events (some of which triggered warnings in the system), we can also curl these endpoints to see:

```
# events
curl http://127.0.0.1:8000/v1/component_events | python -m json.tool

# warnings triggered
curl http://127.0.0.1:8000/v1/resource_warnings | python -m json.tool
```

To see documentation auto-generated by FastAPI, go to: http://127.0.0.1:8000/docs

## Getting Started With Docker

1. Clone the repo

```
git clone  https://github.com/NHopewell/diskspace-monitor-CRUD

cd diskspace-monitor-CRUD
```

2. Build the Dockerfile:

```
docker build . -t diskspace-monitor
```

3. You'll notice in the Dockerfile that we are using the port 8000. Now run the Docker image with port forwarding:

```
docker run -p 8000:8000 diskspace-monitor
```

The application is now accessible over localhost http://127.0.0.1:8000/docs

## Testing and CI

This project is setup with the following things to ensure PEP8 compliance and proper builds:

- pre-commit hooks including black, Flake8, and other hooks.
- local tests for both the API and underlying models with Pytest.
- virtual env management with tox to run pytests on different Python versions and environments.
- github actions to automatically run tox with these different Python versions across different operating systems when changes are made to the repo.

To execute all tests manually in your virtualenv, run:

```
pytest
```

To execute all tests on your system in multiple virtual environments with different configurations, run:

```
tox
```

This will run the test suite in 6 different virtural environments using ubuntu and Windows, each with Python versions 3.8, 3.9. and 3.10.

On git pushes to master or pull requests, tox will be run in these 6 environments concurrently on 6 different machines.
