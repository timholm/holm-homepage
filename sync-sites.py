#!/usr/bin/env python3
"""Rebuild the app list from what the cluster actually serves.

Sources: the Cloudflare tunnel's hostnames (remote-managed config) plus the
cluster's HTTPRoutes/Ingresses. Each hostname is mapped to its namespace; an
app is "down" when that namespace has no running pods or the URL doesn't answer.
Names/descriptions/categories already in site/sites.json are kept.

Run from the repo root (needs kubectl and HOLM_CF_* from ~/.config/holm/env):
    set -a; . ~/.config/holm/env; set +a; python3 sync-sites.py
Then commit site/sites.json and k8s/index.html; Argo rolls it out.
"""
import concurrent.futures as cf, json, os, re, subprocess, urllib.request
from collections import Counter

# Hostnames that are plumbing, not something to open in a browser.
SKIP = re.compile(r"^(autoconfig|autodiscover|mta-sts|streaming|livekit-jwt|cdn|telemetry|"
                  r"ollama-api|mini-rack-api|jmap|cryptpad-sandbox|orc-legacy|www|index)\.")
INFRA = {"argo", "grafana", "k8s", "headlamp", "forgejo", "backups", "bks", "uptime", "umami", "status",
         "rtr", "ntfy", "orc", "shell", "agents", "manus", "ops", "current", "hq", "internet", "xray", "qc", "mod"}
AUTH = {"auth", "sso", "vault"}


def kubectl_json(*args):
    return json.loads(subprocess.run(["kubectl", *args, "-o", "json"], check=True,
                                     capture_output=True, text=True).stdout)["items"]


def tunnel_hosts():
    acct, tok = os.environ["HOLM_CF_ACCOUNT"], os.environ["HOLM_CF_TOKEN"]
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{acct}/cfd_tunnel/{os.environ['HOLM_CF_TUNNEL_K8S']}/configurations",
        headers={"Authorization": f"Bearer {tok}"})
    ingress = json.load(urllib.request.urlopen(req, timeout=30))["result"]["config"]["ingress"]
    out = {}
    for r in ingress:
        if r.get("hostname") and not r.get("path"):
            m = re.match(r"https?://[^.:/]+\.([^.:/]+)\.svc", r.get("service", ""))
            out[r["hostname"]] = m.group(1) if m else None
    return out


def cluster_hosts():
    out = {}
    for x in kubectl_json("get", "httproute", "-A") + kubectl_json("get", "ingress", "-A"):
        hs = x["spec"].get("hostnames") or [r["host"] for r in x["spec"].get("rules", []) if r.get("host")]
        for h in hs:
            out[h] = x["metadata"]["namespace"]
    return out


def running_pods():
    c = Counter()
    for p in kubectl_json("get", "pods", "-A"):
        if p["status"].get("phase") == "Running":
            c[p["metadata"]["namespace"]] += 1
    return c


def answers(host):
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-m", "10", "-w", "%{http_code}", f"https://{host}/"],
                       capture_output=True, text=True)
    return host, r.stdout not in ("", "000", "502", "503", "504", "530")


def guess_cat(host):
    sub = host.split(".")[0]
    if sub in AUTH: return "auth"
    if sub in INFRA: return "infra"
    if host.endswith("holm.chat"): return "comms"
    if host.endswith("holm.community"): return "fediverse"
    if host.endswith(("holm.video", "holm.photo")): return "media"
    return "tools"


def main():
    hosts = {**cluster_hosts(), **{h: ns for h, ns in tunnel_hosts().items() if ns}}
    hosts = {h: ns for h, ns in hosts.items() if not SKIP.match(h)}
    pods = running_pods()
    with cf.ThreadPoolExecutor(24) as ex:
        up = dict(ex.map(answers, hosts))
    old = {s["url"].rstrip("/"): s for s in json.load(open("site/sites.json"))}
    sites = []
    for h, ns in sorted(hosts.items()):
        url = f"https://{h}"
        prev = old.get(url, {})
        sites.append({
            "url": url,
            "cat": prev.get("cat") or guess_cat(h),
            "name": prev.get("name") or h.split(".")[0].replace("-", " ").title(),
            "desc": prev.get("desc") or f"{ns} app",
            "ns": ns,
            "status": "ok" if pods[ns] and up[h] else "down",
        })
    dropped = sorted(set(old) - {s["url"] for s in sites})
    json.dump(sites, open("site/sites.json", "w"), indent=2)
    page = open("k8s/index.html").read()
    page, n = re.subn(r"const SITES = \[.*?\n\]\n;", lambda _: "const SITES = " + json.dumps(sites, indent=2) + "\n;",
                      page, count=1, flags=re.S)
    assert n == 1, "SITES block not found in k8s/index.html"
    open("k8s/index.html", "w").write(page)
    down = [s["url"] for s in sites if s["status"] == "down"]
    print(f"{len(sites)} apps, {len(down)} down, {len(dropped)} dropped (no longer served)")
    for u in down: print("  down   ", u)
    for u in dropped: print("  dropped", u)


if __name__ == "__main__":
    main()
