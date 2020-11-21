#!/bin/sh
celery -A background.celery beat --loglevel=INFO&
celery -A background.celery worker --loglevel=INFO
