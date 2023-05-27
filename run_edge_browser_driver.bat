@echo off
title Edge Browser Driver
cd "C:\Program Files (x86)\Microsoft\Edge\Application"
mkdir "C:\Users\Fern Aerell\Desktop\Python-Youtube-Live-Chat-Without-Api\browser\user_data"
msedge.exe --remote-debugging-port=5000 --user-data-dir="C:\Users\Fern Aerell\Desktop\Python-Youtube-Live-Chat-Without-Api\browser\user_data"