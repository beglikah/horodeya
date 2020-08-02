#!/bin/bash

cd "$(dirname "$0")"
TIMESTAMP=`/bin/date +%Y-%m-%d_%H:%M:%S`
/bin/mkdir -p backup
bash manage.sh dumpdata --natural-primary --natural-foreign --format yaml -o backup/$TIMESTAMP.yaml -e sessions -e admin.logentry
