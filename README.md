# DevOps_with_k8s

## See images folder for pictures related to certain exercises

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


# Exercise 3.06: DBaaS vs DIY

## DBaaS:

Pros:
 - Easy to setup and minimal amount of configuration needed.
 - Easy access to backups and backups are managed automatically
 - Easier to manage security(?)

Cons:
 - Customization is limited.
 - Cost, depending on the usage ofc.
 - Relying on a third-party service provider

## DIY:

Pros:
 - Minimal costs compared to DBaaS
 - Easy to customize installation to specific needs
 - Full control over changes and configurations
 - Costs

Cons:
 - More time spent on configuring and maintenance
 - Need to manage upkeep of all things, e.g., backups
 - Costs( Might get costly )

 # Exercise 4.03

 - Query that was used in prometheus " sum(kube_pod_info{namespace="prometheus", created_by_kind="StatefulSet"})"