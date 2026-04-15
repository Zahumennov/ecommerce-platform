# E-Commerce Platform

A microservices-based e-commerce platform built with FastAPI.
Designed as a real-world learning project covering service decomposition,
async Python, event-driven architecture, and observability.

## Tech Stack

- **FastAPI** — REST API for each microservice
- **PostgreSQL** — separate database per service
- **Redis** — caching and session storage
- **RabbitMQ** — event bus for inter-service communication
- **Celery** — background task processing
- **Nginx** — reverse proxy and API gateway
- **Docker Compose** — local development orchestration
- **Prometheus + Grafana** — metrics and dashboards
- **Jaeger** — distributed tracing

## Services

| Service              | Port | Responsibility              |
|----------------------|------|-----------------------------|
| user-service         | 8001 | Auth, JWT, profiles         |
| product-service      | 8002 | Catalog, search             |
| order-service        | 8003 | Cart, checkout, history     |
| payment-service      | 8004 | Payments, invoices          |
| delivery-service     | 8005 | Warehouse, shipment tracking|
| notification-service | 8006 | Email, push notifications   |

## Architecture

Each service:
- Has its own PostgreSQL database (Database per Service pattern)
- Communicates synchronously via REST (internal calls)
- Communicates asynchronously via RabbitMQ events
- Is independently deployable as a Docker container

## Quick Start

```bash
cp .env.example .env
make up
```

After startup:

- RabbitMQ UI: http://localhost:15672 (guest/guest)
- Grafana: http://localhost:3000
- Jaeger UI: http://localhost:16686

## Project Structure

ecommerce-platform/
├── services/
│   ├── user-service/
│   ├── product-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── delivery-service/
│   └── notification-service/
├── shared/           # Common code shared across services
├── infrastructure/   # Nginx, Prometheus, Grafana configs
├── .github/
│   └── workflows/    # CI/CD pipelines
├── docker-compose.yml
├── Makefile
└── .env.example

## Development Workflow

```bash
# Start infrastructure (databases, Redis, RabbitMQ)
make up

# Run a specific service locally
make dev-user

# Run migrations
make migrate-user

# Run tests
make test-user
```

## Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature
- `fix:` — bug fix
- `chore:` — tooling, config, dependencies
- `docs:` — documentation
- `test:` — tests
- `refactor:` — code refactoring
