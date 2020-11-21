#!/bin/sh

celery -A app.celery beat --loglevel=INFO&
celery -A app.celery worker --loglevel=Info
