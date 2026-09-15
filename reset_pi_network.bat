@echo off
plink -batch -ssh shreyas@10.42.0.1 -pw Daki@upper6 "echo Daki@upper6 | sudo -S systemctl daemon-reload && echo Daki@upper6 | sudo -S systemctl restart NetworkManager"