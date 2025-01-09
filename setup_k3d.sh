#!/bin/bash

set -e

if k3d cluster list | grep -q 'default'; then
  echo "A k3d cluster named 'default' is already running. Deleting it..."
  k3d cluster delete
fi

echo "Creating k3d cluster..."
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2

echo "Creating directory /tmp/kube on k3d-k3s-default-agent-0..."
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube

echo "Cluster setup complete!"