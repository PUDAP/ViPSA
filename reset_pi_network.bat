@echo off
rem Restart NetworkManager on the Raspberry Pi.
rem
rem Credentials are read from the environment, never from this file.
rem Set PI_HOST, PI_USER and PI_PASSWORD before running, for example in
rem reset_pi_network.local.bat next to this script (git-ignored):
rem
rem   set PI_HOST=<pi address>
rem   set PI_USER=<ssh user>
rem   set PI_PASSWORD=<ssh password>

setlocal
if exist "%~dp0reset_pi_network.local.bat" call "%~dp0reset_pi_network.local.bat"

if "%PI_HOST%"=="" goto :missing
if "%PI_USER%"=="" goto :missing
if "%PI_PASSWORD%"=="" goto :missing

plink -batch -ssh %PI_USER%@%PI_HOST% -pw "%PI_PASSWORD%" "echo '%PI_PASSWORD%' | sudo -S systemctl daemon-reload && echo '%PI_PASSWORD%' | sudo -S systemctl restart NetworkManager"
exit /b %errorlevel%

:missing
echo Set PI_HOST, PI_USER and PI_PASSWORD first, for example in reset_pi_network.local.bat. 1>&2
exit /b 1
