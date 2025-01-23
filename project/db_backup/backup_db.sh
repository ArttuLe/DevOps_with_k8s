#!/bin/bash

set -e

export DEBIAN_FRONTEND=noninteractive
ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime
echo "Etc/UTC" > /etc/timezone

apt-get update && apt-get install -y \
    software-properties-common \
    wget \
    gnupg2 \
    lsb-release \
    tzdata

sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update
apt-get install -y postgresql-client-16

if [ $URL ]; then
  pg_dump -v $URL > /usr/src/app/backup.sql
  
  gsutil cp /usr/src/app/backup.sql gs://dwk-gke/backup-$(date +%Y-%m-%d_%H-%M-%S).sql
  
  echo "Backup completed and uploaded to Google Cloud Storage."
else
  echo "Database URL not provided. Set the URL environment variable."
  exit 1
fi
