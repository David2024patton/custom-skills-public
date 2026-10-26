#!/usr/bin/env python3
"""YouTube Data API v3 CLI, authenticated through the custom.youtube connector.

The API key never appears in this code or in output. It reaches requests as an
hsurr:* surrogate that Sentinel/authd swaps for the real key on egress.
Usage:
  youtube.py channel --id UC...            public stats for a channel
  youtube.py channel --username NAME       public stats by legacy username
  youtube.py search -q "query" [--max 10]  search videos/channels/playlists
  youtube.py videos --ids VID1,VID2        details for up to 50 videos
  youtube.py uploads --channel-id UC...    latest uploads from a channel
  youtube.py comments --video-id VID       top-level comment threads
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
HELPER_MESSAGE = ("Private credential helper required: dynamic_credentials is "
                  "available only in the operator's private copy; copy it "
                  "beside this script and retry.")
_helper = None


def load_helper():
    """Import the private credential helper lazily, at point of use.

    Lazy loading keeps --help (argparse, in main) working without the
    helper. When the helper is genuinely needed and missing, print the
    message to stderr and exit 3, never 0: a missing private helper is a
    failure, not a success.
    """
    global _helper
    if _helper is None:
        try:
            import dynamic_credentials as _module
        except ImportError:
            print(HELPER_MESSAGE, file=sys.stderr)
            sys.exit(3)
        _helper = _module
    return _helper

BASE = "https://www.googleapis.com/youtube/v3"
ALLOWED = ("www.googleapis.com", "youtube.googleapis.com")
CRED = "custom.youtube"


def api_get(path, params):
    dc = load_helper()
    params = {k: v for k, v in params.items() if v is not None}
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    url = dc.url_with_surrogate_query_param(url, CRED, allowed_hosts=ALLOWED)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return dc.read_json_response(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:1500]
        raise SystemExit(f"HTTP {e.code}: {body}")


def cmd_channel(args):
    params = {"part": "snippet,statistics,contentDetails"}
    if args.id:
        params["id"] = args.id
    elif args.username:
        params["forUsername"] = args.username
    else:
        raise SystemExit("need --id or --username")
    data = api_get("/channels", params)
    out = []
    for ch in data.get("items", []):
        snip, stats = ch.get("snippet", {}), ch.get("statistics", {})
        out.append({
            "id": ch.get("id"),
            "title": snip.get("title"),
            "customUrl": snip.get("customUrl"),
            "publishedAt": snip.get("publishedAt"),
            "country": snip.get("country"),
            "subscriberCount": stats.get("subscriberCount"),
            "videoCount": stats.get("videoCount"),
            "viewCount": stats.get("viewCount"),
            "uploadsPlaylist": (ch.get("contentDetails", {})
                                .get("relatedPlaylists", {}).get("uploads")),
        })
    print(json.dumps(out, indent=2))


def cmd_search(args):
    params = {"part": "snippet", "q": args.q, "maxResults": args.max,
              "type": args.type, "order": args.order}
    data = api_get("/search", params)
    out = []
    for item in data.get("items", []):
        ids = item.get("id", {})
        kind = ids.get("kind", "").split("#")[-1]
        vid = ids.get("videoId") or ids.get("channelId") or ids.get("playlistId")
        snip = item.get("snippet", {})
        out.append({"kind": kind, "id": vid, "title": snip.get("title"),
                    "channelTitle": snip.get("channelTitle"),
                    "publishedAt": snip.get("publishedAt")})
    print(json.dumps(out, indent=2))


def cmd_videos(args):
    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    data = api_get("/videos", {"part": "snippet,statistics,contentDetails",
                               "id": ",".join(ids[:50])})
    out = []
    for v in data.get("items", []):
        snip, stats = v.get("snippet", {}), v.get("statistics", {})
        out.append({"id": v.get("id"), "title": snip.get("title"),
                    "publishedAt": snip.get("publishedAt"),
                    "duration": v.get("contentDetails", {}).get("duration"),
                    "viewCount": stats.get("viewCount"),
                    "likeCount": stats.get("likeCount"),
                    "commentCount": stats.get("commentCount")})
    print(json.dumps(out, indent=2))


def cmd_uploads(args):
    data = api_get("/playlistItems", {
        "part": "snippet,contentDetails", "playlistId": args.playlist_id,
        "maxResults": args.max})
    out = []
    for item in data.get("items", []):
        snip = item.get("snippet", {})
        out.append({"videoId": item.get("contentDetails", {}).get("videoId"),
                    "title": snip.get("title"),
                    "publishedAt": snip.get("publishedAt")})
    print(json.dumps(out, indent=2))


def cmd_comments(args):
    data = api_get("/commentThreads", {
        "part": "snippet", "videoId": args.video_id, "maxResults": args.max,
        "order": "relevance", "textFormat": "plainText"})
    out = []
    for item in data.get("items", []):
        top = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
        out.append({"author": top.get("authorDisplayName"),
                    "likeCount": top.get("likeCount"),
                    "publishedAt": top.get("publishedAt"),
                    "text": (top.get("textDisplay") or "")[:300]})
    print(json.dumps(out, indent=2))


def main():
    p = argparse.ArgumentParser(description="YouTube Data API v3 via connector")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("channel", help="public channel stats")
    c.add_argument("--id"); c.add_argument("--username")
    c.set_defaults(fn=cmd_channel)

    s = sub.add_parser("search", help="search YouTube")
    s.add_argument("-q", required=True); s.add_argument("--max", type=int, default=10)
    s.add_argument("--type", default="video")
    s.add_argument("--order", default="relevance")
    s.set_defaults(fn=cmd_search)

    v = sub.add_parser("videos", help="video details by id")
    v.add_argument("--ids", required=True)
    v.set_defaults(fn=cmd_videos)

    u = sub.add_parser("uploads", help="latest uploads from a playlist")
    u.add_argument("--playlist-id", required=True)
    u.add_argument("--max", type=int, default=10)
    u.set_defaults(fn=cmd_uploads)

    m = sub.add_parser("comments", help="comment threads on a video")
    m.add_argument("--video-id", required=True)
    m.add_argument("--max", type=int, default=10)
    m.set_defaults(fn=cmd_comments)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
