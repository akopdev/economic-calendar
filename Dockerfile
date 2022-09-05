FROM python:3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app /app
WORKDIR /

ENV PYTHONPATH=/app

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:80", "app.main:app", "--worker-class", "aiohttp.GunicornWebWorker"]
