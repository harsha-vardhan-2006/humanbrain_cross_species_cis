@echo off
cd /d D:\humanbrain\humanbrain\13_CROSS_SPECIES_CIS\05_NULLS\degree_preserving
py null_models.py --battery a --no-validate --workers 4 > ..\..\logs\e04a_detached.log 2>&1
