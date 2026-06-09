import json
# (url, cat, name, desc, status)
S = [
  # comms
  ("https://element.holm.chat",     "comms",  "Element",          "Matrix client"),
  ("https://cinny.holm.chat",       "comms",  "Cinny",            "Alternate Matrix client"),
  ("https://matrix.holm.chat",      "comms",  "Continuwuity",     "Matrix homeserver"),
  ("https://matrix.holm.team",      "comms",  "matrix-holm",      "Matrix homeserver (holm.team)"),
  ("https://call.holm.chat",        "comms",  "Element Call",     "Voice/video calls"),
  ("https://snikket.holm.chat",     "comms",  "Snikket",          "XMPP admin"),
  ("https://cheogram.holm.chat",    "comms",  "Cheogram",         "XMPP web client"),
  ("https://signal.holm.chat",      "comms",  "Signal Web",       "Signal-relay frontend"),
  ("https://nostr.holm.chat",       "comms",  "Strfry",           "Nostr relay"),
  ("https://groups.holm.chat",      "comms",  "Snikket groups",   "Group chat"),
  ("https://livekit.holm.chat",     "comms",  "LiveKit",          "Realtime audio/video"),

  # fediverse
  ("https://holm.community",        "fediverse", "Mastodon",       "Microblog"),
  ("https://holm.video",            "fediverse", "PeerTube",       "Federated video"),
  ("https://loops.holm.video",      "fediverse", "Loops",          "Short-form video"),
  ("https://live.holm.video",       "fediverse", "Owncast",        "Live streaming"),
  ("https://holm.photo",            "fediverse", "Pixelfed",       "Federated photos"),
  ("https://lemmy.holm.community",  "fediverse", "Lemmy",          "Federated forum"),
  ("https://news.holm.community",   "fediverse", "News",           "Fallacy tracker"),
  ("https://relay.holm.chat",       "fediverse", "AP Relay",       "ActivityPub relay"),
  ("https://fedi-studio.holm.community", "fediverse", "Fedi Studio", "Federation studio"),
  ("https://apps.holm.team",        "fediverse", "Fedi Dashboard", "Sub-apps directory"),
  ("https://holos.holm.team",       "fediverse", "Holos Discover", "Discovery frontend"),
  ("https://hunter.holm.team",      "fediverse", "Fedi Hunter",    "Hunter dashboard"),
  ("https://docs.holm.community",   "fediverse", "Docs",           "Federation docs"),
  ("https://api.holm.community",    "fediverse", "Fedi API",       "Discovery API"),
  ("https://memory.holm.team",      "fediverse", "Fedi Memory",    "Memory service"),

  # media
  ("https://photos.holm.team",      "media", "Immich",            "Photo library"),
  ("https://jellyfin.holm.team",    "media", "Jellyfin",          "Media server"),
  ("https://audiobooks.holm.team",  "media", "Audiobookshelf",    "Audiobooks + podcasts"),
  ("https://music.holm.team",       "media", "Navidrome",         "Music server"),
  ("https://tube.holm.team",        "media", "TubeArchivist",     "YouTube archive"),
  ("https://ebooks.holm.team",      "media", "Calibre-Web",       "Ebook library"),

  # tools
  ("https://search.holm.community", "tools", "SearXNG",           "Meta search"),
  ("https://rss.holm.team",         "tools", "Miniflux",          "RSS reader"),
  ("https://bookmarks.holm.team",   "tools", "Karakeep",          "Bookmarks"),
  ("https://forms.holm.team",       "tools", "Formhub",           "Forms"),
  ("https://office.holm.team",      "tools", "Office",            "Office tools"),
  ("https://v2a.holm.chat",         "tools", "Video → Audio",     "MP4 → MP3 converter"),
  ("https://vaultwarden.holm.team", "tools", "Vaultwarden",       "Password manager"),
  ("https://cryptpad.holm.team",    "tools", "Cryptpad",          "Collaborative docs"),
  ("https://drive.holm.team",       "tools", "Drive",             "File storage"),
  ("https://dl.holm.team",          "tools", "Downloader",        "Download manager"),
  ("https://workbook.holm.team",    "tools", "Workbook",          "Workbook app"),
  ("https://chapters.holm.team",    "tools", "Chapters",          "Chapters service"),
  ("https://field.holm.team",       "tools", "Field Station",     "Field tools"),
  ("https://mod.holm.team",         "tools", "Moderation",        "Mod tools"),
  ("https://qc.holm.team",          "tools", "Quality Control",   "QC tools"),
  ("https://wanderer.holm.team",    "tools", "Wanderer",          "GPS track viewer"),
  ("https://dashy.holm.team",       "tools", "Dashy",             "Dashboard generator"),
  ("https://xray.holm.team",        "tools", "Xray",              "Inspector"),
  ("https://arsenal.holm.team",     "tools", "Arsenal",           "App arsenal"),
  ("https://ai-functions.holm.team","tools", "AI Functions",      "AI workflows"),
  ("https://shell.holm.team",       "tools", "Web Shell",         "In-browser shell"),

  # infra
  ("https://forgejo.holm.team",     "infra", "Forgejo",           "Git forge + registry"),
  ("https://argo.holm.team",        "infra", "Argo CD",           "GitOps controller"),
  ("https://grafana.holm.team",     "infra", "Grafana",           "Metrics"),
  ("https://ntfy.holm.team",        "infra", "ntfy",              "Push notifications"),
  ("https://uptime.holm.team",      "infra", "Uptime Kuma",       "Uptime monitor"),
  ("https://backups.holm.team",     "infra", "Velero",            "Backup status"),
  ("https://bks.holm.team",         "infra", "Backup Dashboard",  "Backup health"),
  ("https://umami.holm.community",  "infra", "Umami",             "Analytics"),

  # auth
  ("https://auth.holm.team",        "auth",  "Keycloak",          "SSO"),

  # world
  ("https://adventure.holm.team",   "world", "WorkAdventure",     "Virtual workspace"),
  ("https://stella.holm.team",      "world", "Stella",            "Star map"),
  ("https://mini-rack.holm.team",   "world", "Mini Rack",         "Hardware dashboard"),
]
out = [{"url":u,"cat":c,"name":n,"desc":d,"status":"ok"} for (u,c,n,d) in S]
print(json.dumps(out, indent=2))
