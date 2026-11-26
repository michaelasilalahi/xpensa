# Install `mlxtend` with `--no-deps` in Docker

The backend only uses `mlxtend.frequent_patterns` (`fpgrowth` and `association_rules`), which depend only on `numpy`, `pandas`, and `joblib` (`mlxtend.frequent_patterns.__init__` eagerly imports `apriori`, which imports `joblib`). However, `mlxtend`'s package metadata also pulls in `scipy`, `scikit-learn`, `matplotlib`, `Pillow`, and `fontTools` (~245 MB combined). We replaced `mlxtend.preprocessing.TransactionEncoder` (the only import pulling in `scipy`/`scikit-learn`) with an equivalent NumPy implementation in `oneHot_encoding.py`, declare `joblib` explicitly and pin `mlxtend` in `backend/requirements.txt`, and install `mlxtend` using `--no-deps` in `backend/Dockerfile` while keeping local `pip install -r requirements.txt` unchanged.

## Consequences

- Production container images shrink by ~245 MB and avoid loading `scipy`/`scikit-learn` into RAM.
- Upgrading `mlxtend` must keep its version pinned and verify `from mlxtend.frequent_patterns import fpgrowth, association_rules` succeeds in Docker (checked during the `builder` stage in `backend/Dockerfile`).
- Future backend code must only import `mlxtend.frequent_patterns` (or other submodules requiring only `numpy`/`pandas`/`joblib`); importing `mlxtend` modules that require `scipy`, `scikit-learn`, or `matplotlib` will work locally but fail in Docker unless `--no-deps` is removed or those dependencies are added explicitly to `backend/requirements.txt`.
