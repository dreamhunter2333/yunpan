FROM python:3.9-slim

COPY . /app
WORKDIR /app
RUN python3 -m pip install -r /app/requirements.txt
RUN rm -rf /root/.cache
ENTRYPOINT ["python3", "-m", "uvicorn",  "--host", "0.0.0.0", "main:app"]
