FROM    python:3.9-slim-buster AS base
ENV     PYTHONUNBUFFERED True
# Testing
ENV     SESSIONS_COLLECTION sessions
WORKDIR /src
RUN     apt update && \
        pip install pipenv

FROM    base
COPY    *.py Pipfile* ./
ADD     data/* data/
ADD     modules/* modules/

RUN     pipenv install --system --deploy
CMD     gunicorn --bind 0.0.0.0:$PORT -w 4 -k uvicorn.workers.UvicornWorker main:app 