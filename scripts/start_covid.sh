#!/bin/bash

NAME="libdb"
PROJECT_SRC="/opt/covid/covid-api/src"
LOGFILE="/opt/projects/covid/data/logs/gunicorn/gunicorn.log"

USER=$(whoami)
GROUP=$(id -g -n)

if [[ "$OSTYPE" == "linux-gnu" ]]; then
  NUM_WORKERS=$((2 * $(cat /proc/cpuinfo | grep 'core id' | wc -l) + 1))
elif [[ "$OSTYPE" == "darwin"* ]]; then
  NUM_WORKERS=3
fi

NUM_WORKERS=3
NUM_THREADS=$((4 * $NUM_WORKERS))

WSGI_MODULE=wsgi

cd $PROJECT_SRC

source /opt/covid/runtime-environments/python/bin/activate
source /opt/covid/covid-devops/environments/.env

export PYTHONPATH=$PROJECT_SRC

export FLASK_ENV=production
export FLASK_APP=app

echo "Starting $NAME with $NUM_WORKERS workers and $NUM_THREADS threads!"

exec gunicorn ${WSGI_MODULE}:app \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=0.0.0.0:7000 \
  --log-level=info \
  --reload \
  --log-file=$LOGFILE \
  --timeout=1200 \
  --threads=$NUM_THREADS \
  --worker-class=gthread
