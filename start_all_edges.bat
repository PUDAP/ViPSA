@echo off
setlocal

for %%E in (
  zaber
  stage
  light
  keysight-b2902b
  keithley-707b
  keithley-2450
) do (
  start "%%E" /D "%~dp0%%E" cmd /k start_edge.bat
)

endlocal
