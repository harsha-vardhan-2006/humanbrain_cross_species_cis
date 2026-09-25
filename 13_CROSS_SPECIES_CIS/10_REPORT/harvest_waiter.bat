@echo off
REM Post-chain harvester: waits for the e04_chain to finish (E06 done marker),
REM then rebuilds figures/tables and runs the gate-resolution harvest.
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\10_REPORT
call :log "harvest-waiter start"

:wait_chain
REM chain writes its completion line to e04_chain.log (dir moves with the .bat)
if exist ..\05_NULLS\degree_preserving\e04_chain.log (
  findstr /c:"E06 done" ..\05_NULLS\degree_preserving\e04_chain.log >nul 2>&1
  if not errorlevel 1 goto chain_done
)
REM fallback: harvest could also be triggered by the stamp-less completion of
REM all artifacts; poll for table_08 as the last chain output
if exist ..\09_TABLES\table_08_robustness.csv (
  findstr /c:"condition" ..\09_TABLES\table_08_robustness.csv >nul 2>&1
  if not errorlevel 1 goto chain_done
)
ping -n 601 127.0.0.1 >nul
goto wait_chain

:chain_done
call :log "chain complete - rebuilding figures and tables"
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\08_FIGURES
py make_figures.py >> harvest.log 2>&1
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\09_TABLES
py build_tables.py >> harvest.log 2>&1
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\10_REPORT
py fill_report.py >> harvest.log 2>&1
call :log "harvest done (see harvest.log)"
exit /b 0

:log
echo [%date% %time%] %~1 >> harvest.log
exit /b 0
