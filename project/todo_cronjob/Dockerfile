FROM alpine:latest
RUN apk --no-cache add curl jq bash

WORKDIR /app

COPY create_random.sh .

RUN chmod +x create_random.sh

ENTRYPOINT ["./create_random.sh"]