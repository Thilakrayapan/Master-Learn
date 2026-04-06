# PeakPulse

[![CI](https://github.com/Thilakrayapan/Master-Learn/actions/workflows/python-app.yml/badge.svg)](https://github.com/Thilakrayapan/Master-Learn/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

PeakPulse is a lightweight study & task tracker built with Flask. It provides task management with deadlines, a study timer, session logging, and a dashboard with basic stats.

## Features
- Task CRUD with deadlines and completion tracking
- Study timer and session logging
- Dashboard with recent stats and simple API endpoints

## Requirements
- Python 3.10+
- See `requirements.txt` for Python dependencies

## Quick start
From the repository root:

Windows (PowerShell):

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python PeakPulse/app.py
```

macOS / Linux:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python PeakPulse/app.py
```

The app runs by default on port `5000` in development mode.

## Demo / Showcase
You can create a quick public demo using GitHub Pages:

- Enable Pages in the repository Settings → Pages and select the `docs/` folder on the `main` branch.
- After enabling, your site will be available at `https://<your-username>.github.io/Master-Learn/`.

Live demo (placeholder): ![demo](https://via.placeholder.com/800x400?text=PeakPulse+Demo)

## Database
The app uses SQLite by default (`sqlite:///peakpulse.db`). The database file will be created in the working directory where you run the app. To reset the data, stop the app and remove `peakpulse.db`.

## Contributing
See `CONTRIBUTING.md` for contribution guidelines and the PR template.

## License
This project is licensed under the MIT License — see the `LICENSE` file for details.

