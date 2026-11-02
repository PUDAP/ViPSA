# PowerShell DirectShow launcher quoting for MediaMTX publishers

Use when a Windows PowerShell launcher starts FFmpeg DirectShow publishers for MediaMTX and camera names contain spaces or trailing spaces, e.g. `USB CAMERA ` or `Logi Webcam C920e`.

## Symptoms

- FFmpeg log shows it received a truncated input such as `video=USB` instead of `video=USB CAMERA `.
- PowerShell parse error around multiline string concatenation:
  - `You must provide a value expression following the '+' operator.`
  - `Unexpected token 'Quote-CmdArg' in expression or statement.`

## Durable pattern

Avoid multiline `+` continuation after an operator in PowerShell. Build command text with an array and `-join ''`:

```powershell
function Quote-CmdArg($value) {
    '"' + ($value -replace '"', '""') + '"'
}

$cmdLine = @(
    '@echo off'
    [Environment]::NewLine
    (Quote-CmdArg $Ffmpeg)
    ' -hide_banner -loglevel warning -rtbufsize 256M'
    ' -f dshow -video_size 1920x1080 -vcodec mjpeg'
    ' -i '
    (Quote-CmdArg "video=$deviceName")
    ' -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p'
    ' -an -f flv '
    $url
    ' 1>'
    (Quote-CmdArg $stdoutLog)
    ' 2>'
    (Quote-CmdArg $stderrLog)
    [Environment]::NewLine
) -join ''

Set-Content -Path $cmdFile -Value $cmdLine -Encoding ASCII
Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', (Quote-CmdArg $cmdFile) -WindowStyle Hidden
```

## Operational check

If the user reports an error from an old line number/content after you patched the file, verify the exact Windows-local file contents or create a new clearly named launcher such as `run-vipsa-streams-fixed.ps1`. Users may be rerunning an older copy, a cached terminal command, or a different path than the file just patched.

Static checks before handing back:

```bash
grep -n ' +$' /mnt/c/Users/<user>/livestream/*.ps1 || echo 'no trailing plus continuations'
nl -ba /mnt/c/Users/<user>/livestream/<launcher>.ps1 | sed -n '72,96p'
```
