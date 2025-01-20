# DevOps_with_k8s


# Secret handling

- sops --encrypt \
       --age agekey \
       secret.yaml > secret.enc.yaml

- export SOPS_AGE_KEY_FILE=$(pwd)/key.txt

- $ sops --decrypt secret.enc.yaml > secret.yaml
- sops --decrypt secret.enc.yaml | kubectl apply -f -

# GKE commands

gcloud container clusters create dwk-cluster --zone=europe-north1-b --cluster-version=1.29

gcloud container clusters delete dwk-cluster --zone=europe-north1-b

gcloud container clusters get-credentials dwk-cluster --zone=europe-north1-b