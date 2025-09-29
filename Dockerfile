FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install reflex

EXPOSE 8000

CMD ["reflex", "run", "--env", "production"]