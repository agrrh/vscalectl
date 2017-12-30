# Rationale

This is a simple wrapper around original [vscale.io](https://vscale.io/) API.

Written during Python practice session.

Currently lacks some "complex" methods like upgrading, making backups and managing SSH keys. Feel free to clone or PR.

# Installation

### Method 1: Python script

```
# git clone ... && cd vscalectl

export VSCALE_API_TOKEN="my-secret-token"

pip3 install -r requirements.txt
./vscalectl.py --help
```

### Method 2: Executable binary

- Download latest release binary from [releases page](https://github.com/agrrh/vscalectl/releases)
- Just copy it inside one of path directories

```
chmod +x vscalectl
cp vscalectl /usr/local/bin/
```

# Notes

When creating server, this tool automatically tries to:

  - determine closest DC by asking [freegeoip.net](http://freegeoip.net/)
  - choose latest Ubuntu LTS release
  - select most basic plan to let you scale up later
