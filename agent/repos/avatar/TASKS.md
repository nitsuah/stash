# Tasks

## Todo

- [ ] Repo purpose - Jupyter notebook(s) for data visualization or small experiments (avatar project).
- [ ] Make the notebook reproducible: add `requirements.txt` or `environment.yml`.
- [ ] Convert one notebook to a clean, standalone `examples/` script or HTML export.
- [ ] Add README with "how to run the notebook" and expected outputs.
- [ ] `ls *.ipynb` and open first cell to see dependencies.
- [ ] Look for `data/` or `images/`.
- [ ] Create `requirements.txt` with minimal packages (e.g., `pandas`, `matplotlib`, `jupyter`).
- [ ] Add `python -m pip install -r requirements.txt` instructions to README.
- [ ] Clear output and run notebook to ensure no hidden state.
- [ ] Export to `examples/avatar.html` (nbconvert) and commit.
- [ ] Create `run_notebook.sh` from the template below

```bash
#!/usr/bin/env bash
python -m pip install -r requirements.txt
NOTEBOOK="${1:-avatar.ipynb}"
jupyter nbconvert --to html "$NOTEBOOK" --ExecutePreprocessor.timeout=600 --execute
```

<!--
AGENT INSTRUCTIONS:
This file tracks specific actionable tasks.
1. Categorize tasks into "Todo", "In Progress", and "Done".
2. Add new tasks identified during code analysis or planning.
3. Mark tasks as [x] when verified as complete.
4. Keep task descriptions concise but actionable.
-->
