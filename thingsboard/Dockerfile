FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY integrate_to_thingsboard.py .

CMD ["python", "integrate_to_thingsboard.py"]

