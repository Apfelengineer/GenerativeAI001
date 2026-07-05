# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is **not a software project** — there is no build, lint, or test tooling, no package manifest, and no source tree to compile. It is a personal research log comparing how different generative AI models/tools respond to the same prompts. Each dated test folder captures one experiment: a prompt (or reading-comprehension text) is given to several AI systems, and their outputs are saved side by side for comparison.

Models/tools appearing across experiments include: ChatGPT, Gemini, NotebookLM, AnythingLLM, and locally-run models (gemma3-4b, gpt-oss-20b, qwen3-8b).

## Repository structure and naming convention

Top-level folders are named `YYMMDD_testNNN` (e.g. `260326_test001`, `260330_test004`), one per experiment session, in chronological order. Within a folder, filenames follow loose but consistent patterns:

- `Question*.txt` — the prompt/task given to each model (in Japanese). For reading-comprehension experiments this is the list of questions; for coding experiments it's a spec (`#仕様` section describing the program to generate).
- `testfile01.txt` / a source text or PDF — the source material the reading-comprehension questions refer to (e.g. a short story, a cooking manual).
- `Answer*.txt` / `QA*.txt` — the reference ("model") answers, i.e. the expected/correct answers used to grade AI responses.
- `result*.txt` — a scoring summary (e.g. `results01.txt` lists each tool's score as `<correct>/<total>`).
- `result<N>_<model>.<ext>` — one AI model's generated output for question N, with the model name as a filename suffix (e.g. `result001_chatgpt.py`, `result002_gemini.cpp`, `result003-xls_gemma3-4b.xlsm`). The file extension matches the deliverable requested in that question's spec (`.py`, `.cpp`, `.xlsm` for Excel VBA, `.txt` for prose answers).

When a numbered question has multiple sub-parts, suffixes like `-1`/`-2` distinguish them (e.g. `result003-1_gemini.txt`, `result003-2_gemini.txt`).

## Working in this repository

- Content is predominantly Japanese. Preserve the existing language and tone when editing or adding files rather than translating.
- Code files under `result*` are AI-generated deliverables captured as historical artifacts of a specific model's output for comparison purposes — do not "fix" or refactor them as if they were production code; if a bug in one model's output is the point of comparison, it should stay as generated. Only edit them if the user explicitly asks to correct/annotate a specific result.
- When adding a new experiment, follow the existing `YYMMDD_testNNN` folder-naming and file-naming conventions above so results stay comparable across sessions.
- There are no automated checks (no CI, no test runner, no linter) — nothing to run before committing changes.
