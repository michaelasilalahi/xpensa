# Install `mlxtend` with `--no-deps` in Docker

The backend only uses `mlxtend.frequent_patterns` (`fpgrowth` and `association_rules`), which depend solely on `numpy` and `pandas`. However, `mlxtend`'s package metadata pulls in `scipy`, `scikit-learn`, `matplotlib`, `Pillow`, `fontTools`, and `joblib` (~245 MB combined). We replaced `mlxtend.preprocessing.TransactionEncoder` (the only import pulling in `scipy`/`scikit-learn`) with an equivalent NumPy implementation in `oneHot_encoding.py`, and install `mlxtend` using `--no-deps` in `backend/Dockerfile` while keeping local `pip install -r requirements.txt` unchanged.

## Consequences

- Production container images shrink by ~245 MB and avoid loading `scipy`/`scikit-learn` into RAM.
- Future backend code must only import `mlxtend.frequent_patterns` (or other pure `numpy`/`pandas` submodules); importing `mlxtend` modules that require `scipy`, `scikit-learn`, or `matplotlib` will work locally but fail in Docker unless `--no-deps` is removed or those dependencies are added explicitly to `backend/requirements.txt`.
