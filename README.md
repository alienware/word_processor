![Aspose Words Editor]

Aspose.Words for Python is a powerful on-premise class library that can be used for numerous document processing tasks. It enables developers to enhance their own applications with features such as generating, modifying, converting, rendering, and printing documents, without relying on third-party applications, for example, Microsoft Word, or automation.

## Usage

```sh
# Interactive Swagger API documentation is available at http://localhost:9000/docs
```
![Swagger UI](https://github.com/alienware/word_processor/blob/main/docs/assets/img/swagger-ui.png?raw=true)

## Run (Development Environment)

Install poetry with following command:

```sh
pip3 install poetry
```

Install packages:

```sh
poetry install
```

Starting the Webservice:

```sh
poetry run gunicorn --bind 0.0.0.0:9000 --workers 1 --timeout 0 app.webservice:app -k uvicorn.workers.UvicornWorker
```

With docker compose:
```sh
docker-compose up --build
```

## Quick start

After running the docker image interactive Swagger API documentation is available at [localhost:9000/docs](http://localhost:9000/docs)

These endpoints are available:

-

## Build

Build .whl package

```sh
poetry build
```

## Docker Build

```sh
# Build Image
docker build -t word_processor .

# Run Container
docker run -d -p 9000:9000 word_processor
```

## TODO

- Unit tests
