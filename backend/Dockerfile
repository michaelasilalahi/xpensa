# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./
# Install mlxtend with --no-deps (see docs/adr/0001-install-mlxtend-without-deps-in-docker.md)
# to avoid pulling unused scipy, scikit-learn, matplotlib, and Pillow (~245 MB).
RUN --mount=type=cache,target=/root/.cache/pip \
    grep -v -i -E '^[[:space:]]*mlxtend([=<>!~].*)?([[:space:]]*#.*)?$' requirements.txt > /tmp/requirements-base.txt && \
    pip install --no-compile -r /tmp/requirements-base.txt && \
    if grep -i -E '^[[:space:]]*mlxtend([=<>!~].*)?([[:space:]]*#.*)?$' requirements.txt > /tmp/requirements-mlxtend.txt; then \
        pip install --no-compile --no-deps -r /tmp/requirements-mlxtend.txt; \
    fi && \
    python -c "from mlxtend.frequent_patterns import fpgrowth, association_rules" && \
    rm -f /tmp/requirements-base.txt /tmp/requirements-mlxtend.txt && \
    pip uninstall -y pip && \
    find /opt/venv/lib/python3.12/site-packages -type d \( -name "tests" -o -name "test" \) -prune -exec rm -rf {} + && \
    python -c "import compileall; compileall.compile_dir('/opt/venv/lib/python3.12/site-packages', quiet=1)"

FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MALLOC_ARENA_MAX=2 \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    PATH="/opt/venv/bin:$PATH"

RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home --shell /usr/sbin/nologin appuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY app /app/app
RUN python -m compileall -q /app/app

ARG GIT_COMMIT_HASH=unknown
ENV GIT_COMMIT_HASH=${GIT_COMMIT_HASH}

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
