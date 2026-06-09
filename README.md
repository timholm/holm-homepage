# holm-homepage

Service directory for the Holm cluster. Deployed to https://holm.team via Cloudflare Tunnel; gated behind Keycloak SSO.

## Layout

- `site/index.html` — the page (vanilla HTML/CSS/JS, no build step)
- `k8s/` — kustomize manifests (namespace + nginx + oauth2-proxy)
- ArgoCD app: `homepage`, source path `k8s/`, sync-policy automated

## Edit the page

Edit `site/index.html` (sites list is at the bottom inside the `SITES` array). Commit and push — ArgoCD will pick up the change on next sync and recreate the ConfigMap; the new RS hash forces a rolling restart.

## Secrets (not in git)

`homepage-oauth-secrets` Secret in the `homepage` namespace, three keys:
- `client-id` — Keycloak OIDC client id (`bunker` historically; rename to `homepage` later)
- `client-secret` — from Keycloak admin console
- `cookie-secret` — `openssl rand -base64 32 | head -c 32`
