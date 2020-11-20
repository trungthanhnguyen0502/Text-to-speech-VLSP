FROM python:3.7

WORKDIR /app

RUN apt-get update && apt-get install -y libsndfile-dev

COPY requirement.txt /app/requirement.txt

RUN pip install -r requirement.txt

COPY . /app

EXPOSE 8881

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8881"]