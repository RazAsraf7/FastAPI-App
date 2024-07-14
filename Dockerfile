FROM python:3.8.2-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "DMD:app", "--host", "0.0.0.0", "--port", "8000"]