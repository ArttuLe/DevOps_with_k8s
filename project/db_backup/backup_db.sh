#!/bin/bash

set -e

export DEBIAN_FRONTEND=noninteractive
ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime
echo "Etc/UTC" > /etc/timezone

apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    wget \
    gnupg2 \
    apt-transport-https \
    ca-certificates \
    lsb-release \
    tzdata

sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update
apt-get install -y postgresql-client-16

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

apt-get update && apt-get install -y google-cloud-sdk


if [ $URL ]; then
  pg_dump -v $URL > /usr/src/app/backup.sql
  
  gsutil cp /usr/src/app/backup.sql gs://dwk-gke/backup-$(date +%Y-%m-%d_%H-%M-%S).sql
  
  echo "Backup completed and uploaded to Google Cloud Storage."
else
  echo "Database URL not provided. Set the URL environment variable."
  exit 1
fi
