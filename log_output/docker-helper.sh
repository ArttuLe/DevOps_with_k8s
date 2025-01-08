#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <image-name>"
  exit 1
fi

IMAGE_NAME=$1
DOCKER_USERNAME="arskale"
TAG="latest"

echo "Building Docker image: $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG .

echo "Pushing Docker image to Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG

echo "Docker image pushed: $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
