FROM python:3.9-slim as base
LABEL maintainer="Tanay Upadhyaya"

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


FROM base AS runtime

# Install pipenv and compilation dependencies
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --no-install-recommends \
    vim \
    git \
    build-essential \
    pkg-config \
    software-properties-common \
    gpg-agent \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -U pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system

WORKDIR /app

# Install application into container
COPY . .

COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

# CMD gunicorn --bind 0.0.0.0:9000 --workers 1 --timeout 0 app.webservice:app -k uvicorn.workers.UvicornWorker --reload
CMD uvicorn --host 0.0.0.0 --port 9000 --reload --no-server-header app.webservice:app

