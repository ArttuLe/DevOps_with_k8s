#!/bin/bash

WIKI_URL=$(curl -s -o /dev/null -w '%{redirect_url}' https://en.wikipedia.org/wiki/Special:Random)

TODO_SERVICE_URL="http://todo-backend-svc:2345/todo"

PAYLOAD=$(jq -n --arg title "Read $WIKI_URL" '{title: $title}')

curl -X POST -H "Content-Type: application/json" -d "$PAYLOAD" "$TODO_SERVICE_URL"
