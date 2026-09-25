@echo off
REM One-click recovery after reboot/power loss (2026-09-24).
REM The scheduled tasks are DISABLED (they hang under the scheduler context);
REM the live pipeline runs as detached processes from a user session. After a
REM reboot, run THIS file once - it resumes whatever stage is next.
REM Idempotent: safe to run multiple times (chain has lock + completion guards;
REM harvest is stamp-protected).
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving

set /a npz=0
for %%f in (battery_a\sub-*_nulls.npz) do set /a npz+=1

if %npz% LSS 100 (
  echo [recovery] battery A incomplete (%npz%/100 npz) - resuming battery A
  powershell -NoProfile -Command "Start-Process -WindowStyle Hidden cmd -ArgumentList '/c','py null_models.py --battery a --workers 4 --no-validate >> ..\..\logs\e04a_detached.log 2>&1' -WorkingDirectory 'D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving'"
) else (
  echo [recovery] battery A complete (%npz%/100 npz)
)

echo [recovery] (re)starting chain v2 + harvest waiter
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden cmd -ArgumentList '/c','D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving\e04_chain.bat' -WorkingDirectory 'D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving'"
powershell -NoProfile -Command "Start-Process -WindowStyle Hidden cmd -ArgumentList '/c','D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\10_REPORT\harvest_waiter.bat' -WorkingDirectory 'D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\10_REPORT'"
echo [recovery] done - monitor: e04_chain.log, e04a_run.log, harvest.log
pause
