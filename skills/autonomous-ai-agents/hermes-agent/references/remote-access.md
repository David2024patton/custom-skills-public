# Remote & Mobile Access to the Gateway

How a phone, tablet, or another machine reaches your Hermes gateway, and how
to tell which path (if any) is active. A gateway that works locally proves
nothing about remote reachability: the desktop app and CLI both talk to
`127.0.0.1`, so they stay green while every remote client fails.

## Diagnose first: which path is active?

Each check is one command. Run them before theorizing about the client.

| Check | Command | Healthy reads as |
|---|---|---|
| Bind address | `netstat -ano \| grep LISTEN \| grep :<port>` | a non-loopback bind (`0.0.0.0`, a LAN IP, or a Tailscale IP) — `127.0.0.1:<port>` means LOCAL ONLY |
| Relay (cloud) | `grep GATEWAY_RELAY $HERMES_HOME/.env` | `GATEWAY_RELAY_ID` and `GATEWAY_RELAY_SECRET` present = enrolled |
| hermes-mobile plugin | `find $HERMES_HOME/plugins -maxdepth 2 -iname "*mobile*"` | a plugin dir present AND its id listed in `plugins.enabled` |
| Tailscale serve | `tailscale serve status` | a configured proxy to the gateway/dashboard, not "No serve config" |
| Dashboard port | `netstat ... \| grep :9119` | LISTENING, only if web access off-machine is expected |

`127.0.0.1` is the common silent cause: the gateway is healthy, the desktop
app works, and still no other device can connect — loopback is this machine
only. Read the gateway's own port and `listener_base` from
`$HERMES_HOME/gateway_state.json` rather than assuming one.

## The ways a remote client gets in

1. **Relay connector (official remote access)** — the gateway dials OUT to a
   Nous Portal connector over one authenticated WebSocket; because it is an
   outbound dial, no inbound port is opened and NAT is not an issue. Enable
   with `hermes gateway enroll --token <token>` (requires `hermes setup`
   login); it writes `GATEWAY_RELAY_ID` / `GATEWAY_RELAY_SECRET` /
   `GATEWAY_RELAY_DELIVERY_KEY` into `.env`. The single-use token comes with
   the connector config.
2. **hermes-mobile WebSocket plugin** — adds a WS platform so your own
   mobile/desktop/web client talks directly to the gateway with no second
   backend. For a private app reaching a gateway you control; it must be
   installed AND in `plugins.enabled`.
3. **Tailscale serve** — proxies a tailnet URL to the gateway or dashboard so
   every device on your tailnet reaches it with no public port
   (`tailscale serve status` to inspect; `tailscale serve --help` to add).
   The natural choice for a Tailscale homelab: no internet exposure, and the
   phone works anywhere it has tailnet connectivity.
4. **Web dashboard** — `hermes dashboard`, exposed like (3) when it should be
   reachable off-machine.
5. **Your own reverse-proxy edge**: an existing Traefik/Dokploy (or
   equivalent) stack on your own domain, TLS at the edge, proxying to a
   login-gated dashboard. Same posture as Tailscale for a credential-gated
   service, and it reuses infrastructure you already run. Still never a raw
   unproxied gateway port.

## Making it reachable

### Gateway's own port (direct clients)

When the client talks to the gateway itself (hermes-mobile plugin, a remote
Hermes client), the bind must change from its `127.0.0.1` default:

```bash
HERMES_HOME=<root home the RUNNING gateway reads> \
  hermes config set gateway.api_server.host 0.0.0.0 --force
```

- The key is `gateway.api_server.host` (`API_SERVER_HOST` env is the
  equivalent override); adapter keys the schema does not know print "not a
  recognized config key"; pass `--force`, the loader still reads them.
- Pitfall: `hermes config set` writes to the ACTIVE profile's config, but a
  multiplexed host gateway reads the ROOT config. Run it with `HERMES_HOME`
  set to the root home, or the change lands where nothing reads it.
- A staged bind takes effect only at the next gateway restart, and a healthy
  gateway is never restarted in the foreground (it drops in-flight turns,
  including kanban workers and your own reply). Stage, then restart from a
  background job waiting on `live_work()`.
- Bind AND host firewall must both admit the port (Windows:
  `netsh advfirewall firewall show rule name=all`).

### Dashboard as the door

- Launch it off-loopback: `hermes dashboard --host 0.0.0.0 --port <n>`.
- A manually launched dashboard is culled by Hermes's orphan-dashboard
  cleanup within minutes (clean log, process simply gone) because it is not
  desktop-owned. Set `HERMES_GATEWAY_EXTERNAL_SUPERVISOR=1` in its launch
  environment (the `fixed_identity` family also accepts
  `HERMES_SUPERVISED_CHILD`) so the reaper skips it.
- Put the dashboard port in the same health watchdog as the gateway: a task
  that starts it at logon only cannot recover a mid-session death.

### Verify from where the client actually is

- Local DNS often answers your own hostnames with LAN addresses (split
  horizon), so curling the hostname from the server proves nothing about the
  public path. Resolve via a public resolver (`nslookup <host> 1.1.1.1`),
  then `curl --resolve <host>:443:<public-ip> https://<host>/` and check the
  served BODY (page title or HTML): a proxy answers with its own status
  codes, and only the body proves which service responded.

## Rules

- Pick the path from HOW the client connects (official relay vs your own app
  vs tailnet), never from which is fastest to enable.
- Never expose a raw gateway port to the public internet. Use the relay
  (outbound dial), Tailscale (private tailnet), or an own-edge reverse proxy
  with TLS and a login gate: the gateway token grants full agent control, so
  the endpoint is not a public web service.
- Standing preference for this user: expose through their own domain behind
  their existing reverse proxy, or Tailscale; hosted relays are the fallback
  when there is no own edge.
- Gateway health is not reachability. `hermes gateway list` all-green and
  `/health` returning 200 only prove the LOCAL process is up — re-check the
  bind address before blaming the client app.
- Exposure mechanisms move between releases: confirm a path's current flags
  with its own `--help` before applying.