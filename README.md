# Video to MP3 Converter

A microservices-based application for converting video files to MP3 format.

## Architecture

The project consists of the following services:

- **Auth Service** - User authorization service (Flask, PostgreSQL)
- **Gateway Service** - Main API entry point
- **Converter Service** - Service for converting video files to MP3
- **Notifications Service** - Email notification service

Infrastructure:

- **PostgreSQL** - Database for authorization service
- **MongoDB** - Database for storing video and MP3 files
- **RabbitMQ** - Message queue for inter-service communication

## Prerequisites

- Docker and Docker Compose
- Python 3.11 (for local development without Docker)
- Minikube and kubectl (for Kubernetes deployment)

## Running with Docker Compose

### 1. Configure Environment Variables

Create `.env` files in each service directory:

#### `services/auth/.env`

```env
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
JWT_SIGNING_KEY=
FLASK_RUN_PORT=
```

#### `services/gateway/.env`

```env
AUTH_SERVICE_HOST=
MONGO_HOST=
MONGO_PORT=
MONGO_USER=
MONGO_PASSWORD=
RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_USER=
RABBITMQ_PASSWORD=
PORT=
```

#### `services/converter/.env`

```env
MONGO_HOST=
MONGO_PORT=
MONGO_USER=
MONGO_PASSWORD=
RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_USER=
RABBITMQ_PASSWORD=
VIDEOS_QUEUE_NAME=
```

#### `services/notifications/.env`

```env
RABBITMQ_HOST=
RABBITMQ_PORT=
RABBITMQ_USER=
RABBITMQ_PASSWORD=
SENDER_EMAIL=
SENDER_EMAIL_PASSWORD=
MP3_QUEUE_NAME=
MP3_DOWLOAD_ENDPOINT=
```

### 2. Running with Docker Compose

In the main project directory, run:

```bash
cd services
docker-compose up --build
```

Or in the background:

```bash
docker-compose up -d --build
```

### 3. Access Services

After starting, services will be available on the following ports:

- **Gateway Service**: http://localhost:8080
- **Auth Service**: http://localhost:5000
- **RabbitMQ Management UI**: http://localhost:15672
- **MongoDB**: localhost:27017
- **PostgreSQL**: localhost:5433

### 4. Stop Services

```bash
docker-compose down
```

To remove volumes as well (data):

```bash
docker-compose down -v
```

## Running with Minikube (Kubernetes)

### 1. Prepare Minikube

```bash
# Start minikube
minikube start

# Enable ingress addon
minikube addons enable ingress
```

### 2. Configure Hosts

Add entry to `/etc/hosts` file:

```bash
sudo echo "localhost mp3converter.com" >> /etc/hosts
```

### 3. Configure Secrets and ConfigMaps

Before running, you need to create secrets and configmaps in Kubernetes. Check the files in the `manifests/` directories of each service and update them with appropriate values.

### 4. Deploy Services

```bash
# Apply manifests for each service
kubectl apply -f services/auth/manifests/
kubectl apply -f services/gateway/manifests/
kubectl apply -f services/converter/manifests/
kubectl apply -f services/notifications/manifests/
```

### 5. Start Minikube Tunnel

In a separate terminal session:

```bash
minikube tunnel
```

### 6. Access Application

The application will be available at: http://mp3converter.com

## Local Development (without Docker)

### Prerequisites

- Python 3.11
- PostgreSQL (running locally or in Docker)
- MongoDB (running locally or in Docker)
- RabbitMQ (running locally or in Docker)

### Steps

1. Create virtual environments for each service:

```bash
cd services/auth
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. Configure environment variables in `.env` files (as above, but use `localhost` instead of container names).

3. Run each service separately:

```bash
# Auth Service
cd services/auth
python3 -m src.app

# Gateway Service (in separate terminal)
cd services/gateway
python3 -m src.app

# Converter Service (in separate terminal)
cd services/converter
python3 -m src.app

# Notifications Service (in separate terminal)
cd services/notifications
python3 -m src.app
```

## Database Migrations (Auth Service)

If you're running Auth Service for the first time or have changed models:

```bash
# In services/auth directory
flask db upgrade
```

To create a new migration:

```bash
flask db migrate -m "Change description"
flask db upgrade
```

## Project Structure

```
services/
├── auth/              # Authorization service
├── gateway/           # Main API service
├── converter/         # Conversion service
├── notifications/     # Notification service
└── docker-compose.yaml  # Main docker-compose file
```

## Troubleshooting

### Database Connection Issues

- Check if PostgreSQL container is running: `docker ps`
- Check logs: `docker logs auth_postgres`
- Verify that environment variables in `.env` are correct

### RabbitMQ Issues

- Check RabbitMQ Management UI availability: http://localhost:15672
- Check logs: `docker logs rabbitmq`
- Ensure all services use the same credentials

### MongoDB Issues

- Check if MongoDB container is running
- Check logs: `docker logs mongo`
- Verify that credentials are correct
