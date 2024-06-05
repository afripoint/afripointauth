#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'

exec watchfiles --filter python celery.__main__.main --args '-A appauth.celery_app beat -l INFO'