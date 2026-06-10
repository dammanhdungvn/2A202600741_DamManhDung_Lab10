# Testing Strategy

- **Evaluation Pipeline:** The primary "tests" are the evaluation metrics. `script/run_phase1.py` acts as the baseline test, generating Hit Rate and Token F1 scores.
- **Observability Gates:** The quality checks (`src/observability/quality.py`) act as data tests. They should flag schema errors, nulls, and stale data.
- **End-to-End Testing:** `script/run_corruption_flow.py` tests the robustness of the system by intentionally breaking the data, verifying the system detects it, and repairing it.
