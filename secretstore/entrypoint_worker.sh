#!/bin/bash
mkdir -p $LOG_PATH
celery -A make_celery worker --concurrency=2
celery -A make_celery beat