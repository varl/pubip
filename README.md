pubIp
=====

Simple dynamic DNS resolver which works with
[Tomato](http://www.polarcloud.com/tomato) and requires only [Python
3](http://python.org).

## Just run it.

```
$ /usr/bin/python3 pubip.py
```

## Supervisor config example

```
$ cat /etc/supervisor/conf.d/pubip.conf

[program:pubip]
command=/path/to/python3 pubip.py
directory=/YOUR_DIR/pubip
user=NOT_ROOT_FOR_PETES_SAKE
autostart=true
autorestart=true
redirect_stderr=true
```

## Setup in Tomato

0. In the left menu under `Basic -> DDNS` set "auto-refresh every" to e.g. 1 days.
0. In the `Service` dropdown choose: `Custom URL`.
0. Add URL to where you have this service running: `http://YOUR_SERVER.TLD/update/YOUR_KEY/@IP`.
0. Check `Force next update`.
0. Hit `Save`.
0. Verify `Last IP Address` and `Last Result`
0. Point your browser to `http://YOUR_SERVER.TLD/show/YOUR_KEY` to see what `YOUR_KEY` is bound to.
0. Or check if redirects works as intended with `http://YOUR_SERVER.TLD/go/YOUR_KEY/PORT`.

## API

### `/show/:user`:

Shows the current IP that is set for key `:user`.

### `/update/:user/:ip`:

Updates the current IP.

`:ip` must match the request client address.

### `/go/:user/:port`:

This redirects you to whatever IP that `:user` is set to along with `:port`.

## Caveat

All state is in-memory. If service restarts, there will be a delay (whatever you set auto-refresh to) before Tomato updates the IP. `('._.)`

Anyone can overwrite an added key. `(;._.)`

Two Tomato-routers set to update the same key will essentially slap each other silly with trouts. `(╯._.)╯︵ ┻━┻`
