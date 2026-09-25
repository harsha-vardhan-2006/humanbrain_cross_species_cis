@echo off
REM Unattended finalize chain: wait for E04 battery B -> E05 -> harvest.
REM Memory-guarded: only ONE heavy python stage runs at a time (this machine has
REM ~8 GB total and battery B previously died from memory starvation, not BLAS
REM oversubscription). Stages are strictly sequential by design.
setlocal
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set NDP=D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving
set CIS=D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\04_CIS
set REP=D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\10_REPORT
set LOG=%NDP%\finalize_chain.log
set NEED=200

:wait_battery_b
REM Stage 1 done marker: the per-subject summary null_results_battery_b.csv,
REM written only by null_models.py after ALL 200 subjects complete.
if exist "%NDP%\null_results_battery_b.csv" goto have_b
REM Fallback: if all 200 per-subject CSVs exist but the process died before
REM concatenation, count them and rebuild the summary ourselves.
set /a N=0
for %%f in ("%NDP%\battery_b\*_battery_b.csv") do set /a N+=1
if %N% geq %NEED% goto rebuild_b
ping -n 61 127.0.0.1 >nul
goto wait_battery_b

:rebuild_b
echo [%date% %time%] battery_b: %N%/%NEED% per-subject files present, rebuilding summary >> %LOG%
cd /d %NDP%
py -c "import os,pandas as pd; B=r'%NDP%\battery_b'; d=pd.concat([pd.read_csv(os.path.join(B,f)) for f in sorted(os.listdir(B)) if f.endswith('_battery_b.csv')],ignore_index=True).sort_values('subject'); assert len(d)==200, len(d); d.to_csv(r'%NDP%\null_results_battery_b.csv',index=False); print('rebuilt',len(d))" >> %LOG% 2>&1
goto have_b

:have_b
echo [%date% %time%] battery B complete -> E05 >> %LOG%
cd /d %CIS%
py e05_statistics.py > e05_run.log 2>&1
if not exist "%CIS%\e05_statistics.json" (
  echo [%date% %time%] E05 FAILED - stopping before harvest >> %LOG%
  exit /b 1
)
echo [%date% %time%] E05 ok -> harvest >> %LOG%
cd /d %REP%
py fill_report.py >> harvest.log 2>&1
echo [%date% %time%] harvest finished >> %LOG%
exit /b 0
