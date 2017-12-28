# Rationale

This is a simple wrapper around original [vscale.io](https://vscale.io/) API.

Written during Python practice session.

Currently lacks some "complex" methods like upgrading, making backups and managing SSH keys. Feel free to clone or PR.

# Installation

```
# git clone ... && cd vscalectl

pip3 install -r requirements.txt
./vscalectl.py --help
```

# Notes

When creating server, this tool automatically tries to:

  - determine closest DC by asking [freegeoip.net](http://freegeoip.net/)
  - choose latest Ubuntu LTS release
  - select most basic plan to let you scale up later
