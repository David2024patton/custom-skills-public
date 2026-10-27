#!/usr/bin/env python3
"""Meta Leads CLI - retrieve Lead Ads data via Graph API."""
import sys
import json
import urllib.request
import urllib.parse
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
HELPER_MESSAGE = ("Private credential helper required: dynamic_credentials is "
                  "available only in the operator's private copy; copy it "
                  "beside this script and retry.")
_helper = None

def load_helper():
    """Import the private credential helper lazily, at point of use.

    Lazy loading keeps --help working without the helper. When the helper
    is genuinely needed and missing, print the message to stderr and
    exit 3, never 0: a missing private helper is a failure, not a success.
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

CRED = "custom.meta-leads"
HOSTS = ["graph.facebook.com"]
API_VER = "v21.0"

def api_get_with_user_token(path, params=None):
    helper = load_helper()
    base = f"https://graph.facebook.com/{API_VER}{path}"
    if params:
        base += "?" + urllib.parse.urlencode(params)
    # query_param placement: surrogate goes on the URL before Request creation
    url = helper.url_with_surrogate_query_param(base, CRED, allowed_hosts=HOSTS)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return helper.read_json_response(resp)

def api_get_with_token(path, token, params=None):
    # Use Page token directly (obtained via API, not printed)
    base = f"https://graph.facebook.com/{API_VER}{path}"
    q = dict(params or {})
    q["access_token"] = token
    base += "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(base, method="GET")
    # No surrogate here; token is in query param from previous API call
    # Ensure we only call allowed host
    helper = load_helper()
    helper.ensure_allowed_url(base, HOSTS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return helper.read_json_response(resp)

def get_page_token(page_id):
    data = api_get_with_user_token("/me/accounts", {"fields": "id,name,access_token"})
    for p in data.get("data", []):
        if p.get("id") == page_id:
            return p.get("access_token")
    raise RuntimeError(f"Page {page_id} not found in /me/accounts")

USAGE = "Usage: meta-leads.py <pages|forms <page_id>|leads <form_id> [--limit N]>"

def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help"):
        print(USAGE)
        print("Retrieve Lead Ads data via the Graph API (pages, forms, leads).")
        return
    if len(sys.argv) < 2:
        print(USAGE, file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "pages":
        data = api_get_with_user_token("/me/accounts", {"fields": "id,name"})
        # Only show id and name, never tokens
        out = {"data": [{"id": p["id"], "name": p["name"]} for p in data.get("data", [])]}
        print(json.dumps(out, indent=2))
    elif cmd == "forms":
        if len(sys.argv) < 3:
            print("Usage: meta-leads.py forms <page_id>", file=sys.stderr)
            sys.exit(1)
        page_id = sys.argv[2]
        page_token = get_page_token(page_id)
        data = api_get_with_token(f"/{page_id}/leadgen_forms", page_token, {"fields": "id,name"})
        print(json.dumps(data, indent=2))
    elif cmd == "leads":
        if len(sys.argv) < 3:
            print("Usage: meta-leads.py leads <form_id> [--limit N]", file=sys.stderr)
            sys.exit(1)
        form_id = sys.argv[2]
        limit = 10
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                limit = int(sys.argv[idx+1])
        # For leads we need the page token that owns the form; try all pages
        pages = api_get_with_user_token("/me/accounts", {"fields": "id,name,access_token"})
        last_err = None
        for p in pages.get("data", []):
            try:
                data = api_get_with_token(f"/{form_id}/leads", p["access_token"], {"fields": "id,created_time,field_data", "limit": str(limit)})
                print(json.dumps(data, indent=2))
                return
            except Exception as e:
                last_err = e
                continue
        print(f"Failed to retrieve leads: {last_err}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
