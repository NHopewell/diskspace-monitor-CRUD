# diskspace-monitor-CRUD

[![Diskspace Monitor Test Suite](https://github.com/NHopewell/diskspace-monitor-CRUD/actions/workflows/tests.yml/badge.svg)](https://github.com/NHopewell/diskspace-monitor-CRUD/actions/workflows/tests.yml)

The build system is part of a large environment with a multitude of different components. Many of the components have some sort of storage (examples: crash dump handler, versioning system, build distribution). To ensure none of the services go down due to a lack of available storage, the systems have an agent that reports disk usage back to a central monitoring facility, which evaluates the collected data against preset rules and provides status and warnings through API endpoints.

## Getting Started WITHOUT Docker

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

The application code which powers the API can be found in `src/diskspacemonitor/api/v1/main.py`. To run the webserver, navigate to this directory
and run:

```
uvicorn main:app --reload
```

Now our monitoring system is being served over localhost(http://127.0.0.1:8000). You can run my test script which automates sending requests to each end point:

```
python example_automated_api_calls.py
```

This script posts some system components and events, we can curl an endpoint to see:

```
curl http://127.0.0.1:8000/v1/component_events/ | python -m json.tool
```
