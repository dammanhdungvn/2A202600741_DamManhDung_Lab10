# Claude Code Instructions

- **Virtual Environment:** Always assume the user has activated the virtual environment (`source ./venv/bin/activate`).
- **Commands:** When running tests or scripts, ensure they are executed within the virtual environment context.
- **Build Commands:** `python script/run_phase1.py` and `python script/run_corruption_flow.py`.
- **Environment Setup:** `pip install -r requirements.txt`.
- **Secrets:** Remind the user to populate `.env` based on `docs/qwen-api.md` before execution. Never log secrets.
