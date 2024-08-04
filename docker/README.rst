Overview
========

- `docker-compose.yml` spins up API and frontend
- `Dockerfile` is specifically for the FastAPI


Start the Services
==================

To get started, run the following

.. code:: bash

        cd docker # this folder
        docker compose up --build

The Docker output should indicate that both the FastAPI and Streamlit containers were successfully created and their images built:

.. code:: bash

    (fastapi_demo) ➜  weird_salads git:(feature/initial_templating) ✗ cd docker
    (fastapi_demo) ➜  docker git:(feature/initial_templating) ✗ docker compose up --build
    [+] Building 0.8s (24/24) FINISHED                                                                                                docker:desktop-linux
    [+] Running 2/0
    ✔ Container docker-fastapi-1    Created                                                                                                          0.0s
    ✔ Container docker-streamlit-1  Created                                                                                                          0.0s
    Attaching to fastapi-1, streamlit-1
    streamlit-1  |
    streamlit-1  | Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.
    streamlit-1  |
    fastapi-1    | INFO:     Started server process [1]
    fastapi-1    | INFO:     Waiting for application startup.
    fastapi-1    | INFO:     Application startup complete.
    fastapi-1    | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
    streamlit-1  |
    streamlit-1  |   You can now view your Streamlit app in your browser.
    streamlit-1  |
    streamlit-1  |   Local URL: http://localhost:8501
    streamlit-1  |   Network URL: http://172.18.0.3:8501
    streamlit-1  |   External URL: http://130.185.117.181:8501
    streamlit-1  |

with FastAPI @ http://localhost:8000 and Streamlit @ http://localhost:8501


The containers can be viewed with `docker ps`:

.. code:: bash

    (fastapi_demo) ➜  weird_salads docker ps
    CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS              PORTS                    NAMES
    6ce0716175e8   docker-streamlit   "streamlit run app.py"   About a minute ago   Up About a minute   0.0.0.0:8501->8501/tcp   docker-streamlit-1
    6f168d52906d   docker-fastapi     "sleep 365d"             About a minute ago   Up About a minute   0.0.0.0:8000->8000/tcp   docker-fastapi-1


Notes
=====

pSQL is a bit of a pain adding complexity, so SQLite instead...

.. code::

    # pSQL comes with the added headache of logging in...

    postgres:
    container_name: postgres
    image: postgres:latest
    environment:
        - POSTGRES_USER=${POSTGRES_USER}
        - POSTGRES_PASSWORD=${POSTGRES_PW}
        - POSTGRES_DB=${POSTGRES_DB}
    ports:
        - "5432:5432"
    restart: always

    pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
        - PGADMIN_DEFAULT_EMAIL=${PGADMIN_MAIL}
        - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PW}
    ports:
        - "5050:80"
    restart: always


I also shouldn't have made this pip installable as `setuptools_scm` causes havok, see below:

.. code:: bash

    # https://setuptools-scm.readthedocs.io/en/latest/usage/
    # https://stackoverflow.com/questions/77572077/using-setuptools-scm-pretend-version-for-package-version-inside-docker-with-git
    ENV SETUPTOOLS_SCM_PRETEND_VERSION_FOR_MY_PACKAGE=0.0
    RUN pip install --root-user-action=ignore --no-cache-dir .
