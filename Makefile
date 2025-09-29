.PHONY: build run up down dev

build:
    docker build -t mnemo_app:latest .

run:
    docker run -d --env-file .env -p 8000:8000 --name mnemo_app mnemo_app:latest

up:
    docker-compose up -d

down:
    docker-compose down

dev:
    uv run reflex run