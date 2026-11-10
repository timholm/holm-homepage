# holm-homepage

Service directory for the Holm cluster. Deployed to https://index.holm.team via Cloudflare Tunnel; gated behind Holm SSO (Authelia, group `admins`). holm.team's "Log in" button links here.

## Layout

- `site/index.html` — the page (vanilla HTML/CSS/JS, no build step)
- `k8s/` — kustomize manifests (namespace + nginx + oauth2-proxy)
- ArgoCD app: `homepage`, source path `k8s/`, sync-policy automated

## Edit the page

The app list is generated from the cluster: `set -a; . ~/.config/holm/env; set +a; python3 sync-sites.py` reads the Cloudflare tunnel hostnames and HTTPRoutes/Ingresses, marks apps with no running pods (or no answer) as down, keeps names/descriptions already in `site/sites.json`, and rewrites the `SITES` array in `k8s/index.html`. To rename or describe an app, edit `site/sites.json` and re-run. Commit and push; Argo CD recreates the ConfigMap and rolls the pods.

## Secrets (not in git)

`homepage-oauth-secrets` Secret in the `homepage` namespace, three keys:
- `client-id` — Keycloak OIDC client id (`bunker` historically; rename to `homepage` later)
- `client-secret` — from Keycloak admin console
- `cookie-secret` — `openssl rand -base64 32 | head -c 32`
