@echo off
REM E04-E06 unattended chain v2: battery A (watchdog) -> battery B -> E05 -> E06
REM v2 (2026-09-24): single-instance lock; battery-A watchdog relaunch (the v1
REM   chain was killed at launch and never resumed battery A if it died);
REM   E06 runs WITH its frozen validation gate. Downstream commands, batteries,
REM   cohorts, seeds and thresholds are UNCHANGED from the frozen protocol.
setlocal
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving

REM --- idempotency: if the chain already completed once, do nothing ---
findstr /c:"E06 done" e04_chain.log >nul 2>&1
if not errorlevel 1 (
  call :log "chain already completed earlier; repeat trigger ignored"
  exit /b 0
)

REM --- single-instance lock: refuse to start if a fresh (<8h) lock exists ---
powershell -NoProfile -Command "if (Test-Path 'e04_chain.lock') { $age=((Get-Date)-(Get-Item 'e04_chain.lock').LastWriteTime).TotalHours; if ($age -lt 8) { exit 1 } } else { exit 0 }"
if errorlevel 1 (
  call :log "another chain instance is active (fresh lock); exiting"
  exit /b 0
)
echo lock > e04_chain.lock
call :log "chain v2 start"

:wait_a
set /a count=0
for %%f in (battery_a\sub-*_nulls.npz) do set /a count+=1
if %count% GEQ 100 goto a_done
REM watchdog: if battery A is not running, relaunch it (resume-safe from parts)
REM (PowerShell returns 0 when battery A IS running, 1 when it is NOT.)
powershell -NoProfile -Command "$p = Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { $_.CommandLine -match 'null_models.py --battery a' }; if ($p) { exit 0 } else { exit 1 }"
if errorlevel 1 (
  call :log "battery A NOT running with %count%/100 npz - relaunching (resume from checkpoints)"
  powershell -NoProfile -Command "Start-Process -WindowStyle Hidden cmd -ArgumentList '/c','py null_models.py --battery a --workers 4 --no-validate >> ..\..\logs\e04a_detached.log 2>&1' -WorkingDirectory 'D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving'"
)
REM ping-based wait: robust under redirected stdin (timeout.exe can hang there)
ping -n 301 127.0.0.1 >nul
goto wait_a

:a_done
call :log "battery A complete (%count% npz), assembling manifests"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
py null_models.py --battery a --workers 1 --no-validate >> e04_chain.log 2>&1

call :log "battery B start"
py null_models.py --validate --battery b --workers 8 >> e04_chain.log 2>&1
call :log "battery B done"

call :log "E05 start"
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\04_CIS
py e05_statistics.py >> e05_run.log 2>&1
call :log "E05 done"

call :log "E06 start"
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\06_ROBUSTNESS
py robustness.py --workers 8 >> e06_run.log 2>&1
call :log "E06 done - chain complete"

del /q e04_chain.lock >nul 2>&1
exit /b 0

:log
echo [%date% %time%] %~1 >> e04_chain.log
exit /b 0
