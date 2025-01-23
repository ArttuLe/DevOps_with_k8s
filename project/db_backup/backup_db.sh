#!/bin/bash

set -e

if [ $URL ]; then
  pg_dump -v $URL > /usr/src/app/backup.sql
  
  gsutil cp /usr/src/app/backup.sql gs://dwk-gke/backup-$(date +%Y-%m-%d_%H-%M-%S).sql
  
  echo "Backup completed and uploaded to Google Cloud Storage."
else
  echo "Database URL not provided. Set the URL environment variable."
  exit 1
fi
