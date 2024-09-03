# Variables
DOCKER_COMPOSE_FILE=t2t_api/docker-compose.yml
SERVICE_WEB=web
SERVICE_DB=db

# Default target
.PHONY: all
all: build up

# Build the Docker images
.PHONY: build
build:
	docker compose -f $(DOCKER_COMPOSE_FILE) build

# Run the Docker containers in detached mode
.PHONY: up
up:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Run the Docker containers in the foreground
.PHONY: up-fg
up-fg:
	docker compose -f $(DOCKER_COMPOSE_FILE) up

# Pause the Docker containers
.PHONY: pause
pause:
	docker compose -f $(DOCKER_COMPOSE_FILE) pause

# Unpause the Docker containers
.PHONY: unpause
unpause:
	docker compose -f $(DOCKER_COMPOSE_FILE) unpause

# Stop the Docker containers
.PHONY: down
down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

# Rebuild the Docker images and run the containers in detached mode
.PHONY: rebuild
rebuild:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d --build

# View logs for the web service
.PHONY: logs-web
logs-web:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f $(SERVICE_WEB)

# View logs for the database service
.PHONY: logs-db
logs-db:
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f $(SERVICE_DB)

# Clean up Docker resources
.PHONY: clean
clean:
	docker compose -f $(DOCKER_COMPOSE_FILE) down -v --rmi all --remove-orphans

# Make migrations
.PHONY: make-migrations
make-migrations:
	python t2t_api/manage.py makemigrations

# Migrate
.PHONY: migrate
migrate:
	python t2t_api/manage.py migrate

# Run server
.PHONY: run-server
run-server:
	python t2t_api/manage.py runserver

# Display help
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make build       - Build the Docker images"
	@echo "  make up          - Run the Docker containers in detached mode"
	@echo "  make up-fg       - Run the Docker containers in the foreground"
	@echo "  make pause       - Pause the Docker containers"
	@echo "  make unpause     - Unpause the Docker containers"
	@echo "  make down        - Stop the Docker containers"
	@echo "  make rebuild     - Rebuild the Docker images and run the containers in detached mode"
	@echo "  make logs-web    - View logs for the web service"
	@echo "  make logs-db     - View logs for the database service"
	@echo "  make clean       - Clean up Docker resources"
	@echo "  make make-migrations - Django make migrations"
	@echo "  make migrate     - Django migrate"
	@echo "  make run-server  - Django run server"
	@echo "  make help        - Display this help message"
