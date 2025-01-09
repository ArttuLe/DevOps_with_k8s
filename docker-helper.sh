#!/bin/bash

set -e

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <image-name> <dockerfile-path>"
  exit 1
fi

IMAGE_NAME=$1
DOCKERFILE_PATH=$2
DOCKER_USERNAME="arskale"
TAG="latest"

echo "Building Docker image: $DOCKER_USERNAME/$IMAGE_NAME:$TAG from path: $DOCKERFILE_PATH"
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG "$DOCKERFILE_PATH"

echo "Pushing Docker image to Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG

echo "Docker image pushed: $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
