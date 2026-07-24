# to be run with docker compose in smoke-tests directory
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=2.4.1 \
  POETRY_HOME=/opt/poetry

# Install Poetry in its own virtualenv so that installing the project's deps
# (with virtualenvs.create=false, i.e. into the system env) can't downgrade
# Poetry's own dependencies out from under it. Symlink the entrypoint only so
# the app still runs under the system `python`.
RUN python -m venv "$POETRY_HOME" \
  && "$POETRY_HOME/bin/pip" install "poetry==$POETRY_VERSION" \
  && ln -s "$POETRY_HOME/bin/poetry" /usr/local/bin/poetry
# This image is single purpose, so we won't need to compartmentalize Py deps in virtualenvs.
RUN poetry config virtualenvs.create false

COPY README.md pyproject.toml poetry.lock ./
COPY src/ ./src/
RUN poetry install

# Copy the examples into the image and install deps.
COPY examples/ ./examples/
# The example is an app, not a package, so skip installing it as a root package
# (Poetry 2.x errors on this instead of warning); its deps are still installed.
RUN cd ./examples/hello-world && poetry install --no-root

# From this point forward, we're operating on the example app.
WORKDIR /app/examples/hello-world
CMD ["python", "app.py"]
