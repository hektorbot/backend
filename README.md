# Hektor backend

This is Hektor's Python backend. It's responsible for creating images based on a set of rules defined by the artist, Isabelle Gagné. It also provides a REST API to let the frontend app retrieve the data it needs.

Images processing can take a significant amount of time since we need to trigger a style transfer through FloydHub by running a temporary Model API based on [our own fork][fork] of [anishathalye/neural-style][neural-style], thus we append every request to a queue using Django-Q and a Redis backend.

[fork]: https://github.com/hektorbot/neural-style
[neural-style]: https://github.com/anishathalye/neural-style

## Requirements

These should be installed on the host machine prior to setting up the app:

- Python >= 3.7.3
- Redis >= 5.0.4

The style transfer app must be set up on the same machine: [https://github.com/hektorbot/neural-style](https://github.com/hektorbot/neural-style)

## Setup

1. Clone the project locally and `cd` into it:

```sh
$ git clone git@github.com:hektorbot/backend.git hektor-backend
$ cd hektor-backend
```

2. Create a virtual environment and activate it (optional):

```sh
$ python3 -m venv venv
$ . venv/bin/activate
```

3. Install required modules:

```sh
$ pip install -r requirements.txt
```

4. Create a `.env` file based on [`.env.example`](./.env.example) and set the variables as needed:

```sh
$ cp .env.example .env
```

5. Run migrations:

```sh
$ django manage.py migrate
```

6. Run the app:

```sh
$ django manage.py runserver
```

7. To enable image processing, you'll need to start django-q's cluster in the background (make sure Redis server is running first):

```sh
$ nohup python manage.py qcluster&
```

The app should now be running on [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
