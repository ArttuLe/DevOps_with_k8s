# DevOps_with_k8s


sops --encrypt \
       --age agekey \
       secret.yaml > secret.enc.yaml

export SOPS_AGE_KEY_FILE=$(pwd)/key.txt

$ sops --decrypt secret.enc.yaml > secret.yaml
sops --decrypt secret.enc.yaml | kubectl apply -f -