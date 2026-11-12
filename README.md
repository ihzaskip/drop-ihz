# drop-ihz: phone drop for ihz.land

The meeting server and the phone page behind ihz.land's paired phone drop, live at
**https://drop.ihz.app**. A phone pairs with a PC once by scanning a QR code; after
that it sends photos and files straight to the PC over WebRTC. This server only
introduces the two sides and passes their small connection messages; files never
go through it.

Derived from the MIT-licensed meeting server in Oyenza Studio (see `LICENSE`). The
Oyenza name, logo and the Oyen character are not part of that license and are not
used here; the character on the page is Pulo, a small green hill with a sprout.

The protocol (rooms, proofs, message shapes, the `oyen-drop/1` labels) is the
contract with the PC app and must not change. It is written up in
[`docs/paired-drop.md`](https://github.com/ihzaskip/oyenza-studio/blob/main/docs/paired-drop.md)
in the app repo.

- `drop-server.mjs`: the meeting server. Node 20 or newer, no dependencies.
- `public/`: the phone page (installable PWA, Android share target).
- `test/`: `node --test` tests for the server and for `public/drop-core.js`.
- `make_icons.py`: draws the PNG icons (needs Pillow). `public/pulo-*.svg` are the
  page's pictures, hand-written SVG.

## Run and test

```
node drop-server.mjs --port 8797
npm test
```

| Option | Default | |
|---|---|---|
| `--port <n>` | `8797` | `0` picks a free port; the start line says which |
| `--host <addr>` | `127.0.0.1` | `0.0.0.0` behind a proxy |
| `--data <dir>` | `./data` | where `gone.json` (removed rooms, 30 days) lives |
| `--trust-proxy` | off | take the address for the rate limit from `CF-Connecting-IP` |

`TURN_KEY_ID` and `TURN_KEY_API_TOKEN` (a Cloudflare Realtime TURN key) turn on the
relay; without them `/api/ice` hands out STUN only. The server never logs rooms,
proofs, messages, names or addresses.

## Hosting

Render, free web service, Singapore, from this repo's `main` branch
(`render.yaml`). The build runs `npm test`; a red test stops the deploy. The health
check is `/api/health`. The domain `drop.ihz.app` is a CNAME to the service's
`onrender.com` name, set in Vercel DNS (where `ihz.app` lives).

What the free plan means here:

- The service sleeps after 15 minutes without requests and takes about a minute to
  wake. While the PC app is running it keeps a long poll open, so it stays awake.
- State is in memory and `./data` is not kept across restarts or deploys: a phone
  mid-pairing just tries again, and the list of removed rooms starts empty.
- One always-on service uses about 730 of the 750 free hours a month, so keep other
  free services out of the same Render workspace.

On the PC, the app uses `PONI_DROP_SERVER` (default `https://drop.ihz.app`).
