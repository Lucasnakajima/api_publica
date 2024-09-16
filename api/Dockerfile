FROM python:3.11-alpine

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir "cython<3.0.0"
RUN python3 -m pip install --no-cache-dir --upgrade --no-build-isolation -r /tmp/requirements.txt

COPY ./src /app
WORKDIR /app

EXPOSE 80

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
