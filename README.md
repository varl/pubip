pubIp
=====

Simple dynamic DNS resolver which works with
[Tomato](http://www.polarcloud.com/tomato) and requires [Python
3](http://python.org).

## `/show/:user`:

Shows the current IP that is set for key `:user`.

## `/update/:user/:ip`:

Updates the current IP.

`:ip` must match the request client address.

## `/go/:user/:port`:

This redirects you to whatever IP that `:user` is set to along with `:port`.

