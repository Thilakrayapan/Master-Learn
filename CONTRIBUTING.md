# Contributing to PeakPulse

Thanks for your interest in contributing! A few quick guidelines to get you started.

## Reporting bugs
- Open an issue and include a short description, steps to reproduce, and expected vs actual behavior.

## Developing locally
1. Create and activate a virtual environment.

Windows (PowerShell):

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app locally:

```
python PeakPulse/app.py
```

3. Use the existing GitHub Actions workflow for basic checks (`.github/workflows/python-app.yml`).

## Branches & PRs
- Create a feature branch named `feature/description` or `fix/short-description`.
- Open a Pull Request against `main` and fill the PR template.
- Keep PRs small and focused.

## Code style
- Follow PEP8 for Python code. Keep functions small and well-documented.

## License
By contributing you agree that your contributions will be licensed under the project's MIT license.
