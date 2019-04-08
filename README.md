# inotify-clamav

Simple python script
That will watch a folder. When the event "IN_CREATE" comes up clamdscan will scan this file and automatic remove them.

change the var: `watch_folder`

## Systemd-service
```
[Unit]
Description=CLamAVScan
After=clamav-daemon.service

[Service]
Type=simple
# Another Type option: forking
RestartSec=5s
StartLimitBurst=99
User=root <------ Change username for non-root user
ExecStart=/etc/clamav/inotify-clamav.py
Restart=on-failure
# Other Restart options: or always, on-abort, etc

[Install]
WantedBy=multi-user.target
```