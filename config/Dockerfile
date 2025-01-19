FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask==2.0.3 Werkzeug==2.1.2 boto3==1.24.4 python-keycloak==0.20.0

COPY src /app

EXPOSE 5000

CMD ["python", "app.py"]
