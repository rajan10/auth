#!/bin/bash
gunicorn -w 2 --bind 0.0.0.0:5000 app:app


