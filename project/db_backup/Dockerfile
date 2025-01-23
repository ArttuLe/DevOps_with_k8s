FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    python3 \
    python3-pip \
    && curl https://sdk.cloud.google.com | bash

COPY backup_db.sh /usr/src/app/backup_db.sh
RUN chmod +x /usr/src/app/backup_db.sh

CMD ["/usr/src/app/backup_db.sh"]
