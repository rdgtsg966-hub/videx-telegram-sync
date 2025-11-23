#!/bin/bash
gunicorn server:app --bind=0.0.0.0:$PORT &
python3 telegram_to_site.py
