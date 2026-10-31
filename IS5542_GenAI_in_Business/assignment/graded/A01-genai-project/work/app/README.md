# IS5542 customer-service agent (work in progress)

Status: environment only. No agent code, no API calls and no evaluation results yet.

## What this folder will contain

A policy-guarded e-commerce customer-service agent built with LangGraph, evaluated against the
reference agent of the public tau-bench retail domain (simulated online store, 114 tasks,
official split: 74 train / 40 test).

## Setup (Windows, uv)

1. Clone tau-bench at the pinned commit (only its `data/` folder is needed at runtime):

   ```bash
   git clone https://github.com/sierra-research/tau2-bench.git
   cd tau2-bench
   git checkout da0835f6c67baef58bdda18f2a3b037dfb3a1754
   ```

2. Copy `.env.example` to `.env`, then fill in `DEEPSEEK_API_KEY` and `TAU2_DATA_DIR`
   (the `data` folder of the clone). `.env` is git-ignored; never commit keys.

3. Install dependencies from this folder. To keep the virtual environment outside a synced
   folder, point `UV_PROJECT_ENVIRONMENT` somewhere else first:

   ```bash
   export UV_PROJECT_ENVIRONMENT=E:/app-data/codex/scratchpad/is5542-a01/.venv
   uv sync --python 3.12
   uv run tau2 check-data
   ```

Versions installed on 2026-10-31: tau2 2.0.0 (commit above), langgraph 1.2.19, litellm 1.82.6;
see `uv.lock` for the full set.
