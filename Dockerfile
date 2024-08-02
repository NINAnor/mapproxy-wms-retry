FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && pip install gunicorn
COPY pyproject.toml .
COPY src/mapproxy_wms_retry/__init__.py src/mapproxy_wms_retry/pluginmodule.py src/mapproxy_wms_retry/
RUN pip install .
COPY wsgi.py .

EXPOSE 8080/TCP

CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "8"]
