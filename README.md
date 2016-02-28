pubIp
=====

Simple dynamic DNS resolver which works with
[Tomato](http://www.polarcloud.com/tomato) and requires [Python
3](http://python.org).

## `/`:

Shows the current IP that is set

## `/update/:ip`:

Updates the current IP.

`:ip` must match the request client address.

