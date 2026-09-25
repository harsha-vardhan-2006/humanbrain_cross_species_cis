@echo off
setlocal
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving
py null_models.py --battery b --workers %1 --no-validate >> %2 2>&1
