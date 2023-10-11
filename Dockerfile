# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.12.0
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN pip3 install pipenv
#RUN --mount=type=cache,target=/root/.cache/pip \
#    --mount=type=bind,source=requirements.txt,target=requirements.txt \
#    python -m pip install -r requirements.txt \
COPY Pipfile .
COPY Pipfile.lock .
#RUN pip3 install -r requirements.txt
RUN pipenv install

# Switch to the non-privileged user to run the application.
#USER appuser


COPY . .
RUN pipenv install --system --deploy --ignore-pipfile


COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Run the application.
#CMD gunicorn 'venv1.Lib.site-packages.fastapi.middleware.wsgi' --bind=0.0.0.0:8000
CMD ["uvicorn", "src.main:app", "--reload"]