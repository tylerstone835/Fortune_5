#!/usr/bin/bash


cd $F5_ROOT_DIRECTORY

.venv/bin/python ETLs/get_daily.py

# Massive/Polygon Free tier allows five free calls a minute
sleep 62s

.venv/bin/python ETLs/get_weekly.py

if ! git diff --quiet; then
	git add Assets/Data/.
	git commit -m "ETL Data Update - $(date +%Y-%m-%d )" -q
	git push
fi
