FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
COPY src/mapproxy_wms_retry/__init__.py src/mapproxy_wms_retry/pluginmodule.py src/mapproxy_wms_retry/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install .
COPY wsgi.py pyproject.toml uv.lock ./

EXPOSE 8080/TCP

CMD ["uv", "run", "gunicorn", "wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "8"]
