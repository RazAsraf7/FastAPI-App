FROM python:3.8.2-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN python ./MongoDB/MongoDB_Add_cities.py

EXPOSE 8000

CMD ["uvicorn", "DMD:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]
