#!/bin/bash

set -e

if [ $URL ]
then
  pg_dump -v $URL > /usr/src/app/backup.sql
fi