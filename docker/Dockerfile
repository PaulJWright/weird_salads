# docker/Dockerfile
FROM python:3.10-slim

# Install git
RUN apt-get update && apt-get install -y git

WORKDIR /app

# Copy necessary files
COPY ../.git /app/.git
COPY ../pyproject.toml /app/
COPY ../setup.py /app/
COPY ../alembic.ini/ /app/alembic.ini

COPY ../weird_salads/ /app/weird_salads
COPY ../database/ /app/database

# https://setuptools-scm.readthedocs.io/en/latest/usage/
# https://stackoverflow.com/questions/77572077/using-setuptools-scm-pretend-version-for-package-version-inside-docker-with-git
ENV SETUPTOOLS_SCM_PRETEND_VERSION_FOR_MY_PACKAGE=0.0
RUN pip install --root-user-action=ignore --no-cache-dir .

ARG LOCATION_ID
# Command to run FastAPI using Uvicorn
# CMD ["uvicorn", "weird_salads.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh", "-c", "alembic upgrade head && python weird_salads/utils/database/seed_db.py --location_id ${LOCATION_ID} --base_path data/ && uvicorn weird_salads.api.app:app --host 0.0.0.0 --port 8000"]
# CMD ["sleep", "365d"]
