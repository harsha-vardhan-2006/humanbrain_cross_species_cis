@echo off
REM Self-healing finalizer: battery B -> E05 -> harvest, with retry loop.
REM Rationale (2026-09-25): two separate detached launches were terminated
REM mid-flight by console/process-tree cleanup, NOT by a compute error. Each
REM battery-B subject is written atomically, so a retry simply resumes.
REM Memory-guarded: one heavy stage at a time (~8 GB box; battery B previously
REM died of memory starvation with 8 workers, not BLAS oversubscription).
setlocal
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set NDP=D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving
set CIS=D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\04_CIS
set REP=D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\10_REPORT
set LOG=%NDP%\finalize_chain.log
set NEED=200
set ATTEMPT=0

:run_battery_b
set /a ATTEMPT+=1
if %ATTEMPT% gtr 40 goto b_failed
call :count_b
echo [%date% %time%] battery B attempt %ATTEMPT%, %N%/%NEED% done >> %LOG%
if %N% geq %NEED% goto b_done
cd /d %NDP%
py null_models.py --battery b --workers 2 --no-validate >> b_supervisor.log 2>&1
call :count_b
echo [%date% %time%] battery B attempt %ATTEMPT% exited, %N%/%NEED% done >> %LOG%
if %N% geq %NEED% goto b_done
REM stage died -> free memory, then retry (resume-safe)
ping -n 31 127.0.0.1 >nul
goto run_battery_b

:count_b
set /a N=0
for %%f in ("%NDP%\battery_b\*_battery_b.csv") do set /a N+=1
goto :eof

:b_done
echo [%date% %time%] battery B complete (%N%/%NEED%) >> %LOG%
if exist "%NDP%\null_results_battery_b.csv" goto run_e05
echo [%date% %time%] per-subject files complete but summary missing -> rebuild >> %LOG%
py -c "import os,pandas as pd; B=r'%NDP%\battery_b'; d=pd.concat([pd.read_csv(os.path.join(B,f)) for f in sorted(os.listdir(B)) if f.endswith('_battery_b.csv')],ignore_index=True).sort_values('subject'); assert len(d)==200, len(d); d.to_csv(r'%NDP%\null_results_battery_b.csv',index=False); print('rebuilt',len(d))" >> %LOG% 2>&1

:run_e05
if exist "%CIS%\e05_statistics.json" goto run_harvest
echo [%date% %time%] running E05 >> %LOG%
cd /d %CIS%
py e05_statistics.py > e05_run.log 2>&1
if exist "%CIS%\e05_statistics.json" goto run_harvest
echo [%date% %time%] E05 FAILED - halting before harvest >> %LOG%
exit /b 1

:run_harvest
if exist "%REP%\_harvest_done.stamp" goto all_done
echo [%date% %time%] running harvest >> %LOG%
cd /d %REP%
py fill_report.py >> harvest.log 2>&1
if exist "%REP%\_harvest_done.stamp" goto all_done
echo [%date% %time%] harvest did not stamp - halting for inspection >> %LOG%
exit /b 1

:all_done
echo [%date% %time%] ALL STAGES COMPLETE >> %LOG%
exit /b 0

:b_failed
echo [%date% %time%] battery B exceeded retry limit at %N%/%NEED% >> %LOG%
exit /b 1
