# PiHole Setup

This repo is for my convenience, it is a way for me to make notes and backup files for the way I have my PiHoles configured.

## Setup

### Install PiHole

```
wget -O basic-install.sh https://install.pi-hole.net
sudo bash basic-install.sh
```

#### Configure PiHole

- Copy [this file](/Config_Files/pihole-FTL.conf) to `/etc/pihole/pihole-FTL.conf`
- Log into PiHole
- Navigate to Adlists
- Add desired adlists

Suggested lists: 
* https://dbl.oisd.nl/
* Any lists in the [blacklists](/Blacklists) folder

### Install Cloudflared

Use the instructions found here: https://pkg.cloudflare.com/index.html

Create a `cloudflared` user to run the daemon:

```bash
sudo useradd -s /usr/sbin/nologin -r -M cloudflared
```

Using [this Python script](/Scripts/cloudflared_config_writer.py), create the configuration file. This config file will determine which upstream DNS provider(s) used.

Copy the file to `/etc/default/cloudflared`.

Update the permissions for the configuration file and `cloudflared` binary to allow access for the cloudflared user:

```bash
sudo chown cloudflared:cloudflared /etc/default/cloudflared
sudo chown cloudflared:cloudflared /usr/local/bin/cloudflared
```

Then create the `systemd` script to control the running of the service and allow it to run on startup by either:
- Using the file [here](/Config_Files/cloudflared.service)
- Creating a new file
  - Open Nano `sudo nano /etc/systemd/system/cloudflared.service`
  - Copying the following:

```ini
[Unit]
Description=cloudflared DNS over HTTPS proxy
After=syslog.target network-online.target

[Service]
Type=simple
User=cloudflared
EnvironmentFile=/etc/default/cloudflared
ExecStart=/usr/local/bin/cloudflared proxy-dns $CLOUDFLARED_OPTS
Restart=on-failure
RestartSec=10
KillMode=process

[Install]
WantedBy=multi-user.target
```

Enable the `systemd` service to run on startup, then start the service and check its status:

```bash
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

### Configure PiHole To Work With Cloudflared

- Log into PiHole
- Navigate to Settings, DNS tab
- Uncheck all upstream servers
- Add custom upstream server with address `127.0.0.1#5053`
- Scroll down to Advanced, uncheck everything except conditional forwarding
- Put in the local network IP range (mine is 192.168.2.0/24), IP address of OPNSense (or whatever router you are using), and the network name

### Configure OPNSense To Work With PiHole

**TODO**

## Sources

[oisd blocklists](https://oisd.nl/)

[DNS over HTTPS with Cloudflared](https://docs.pi-hole.net/guides/dns/cloudflared/)

[PiHole](https://github.com/pi-hole/pi-hole/)

[PiHole FTL Config](https://docs.pi-hole.net/ftldns/configfile/)