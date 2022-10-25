#!/usr/bin/env bash

# kubectl create secret generic cloudflare-token \
#     --namespace external-dns --from-literal="token=$CF_API_TOK"

helm upgrade --install external-dns external-dns/external-dns \
    --namespace external-dns --create-namespace \
    --set "domainFilters={$DOMAIN}" \
    --set "extraArgs={--cloudflare-proxied, --zone-id-filter=$ZONE_ID}" \
    --values external-dns-values.yaml
