.PHONY: up down logs ps restart clean

# ─── Infrastructure ──────────────────────────────────────

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

# Зупинити і видалити всі volumes (clean slate)
clean:
	docker compose down -v

# ─── Dev servers ─────────────────────────────────────────

dev-user:
	cd services/user-service && uvicorn app.main:app --reload --port 8001

dev-product:
	cd services/product-service && uvicorn app.main:app --reload --port 8002

dev-order:
	cd services/order-service && uvicorn app.main:app --reload --port 8003

# ─── Migrations ──────────────────────────────────────────

migrate-user:
	cd services/user-service && alembic upgrade head

migrate-product:
	cd services/product-service && alembic upgrade head

migrate-order:
	cd services/order-service && alembic upgrade head

# ─── Tests ───────────────────────────────────────────────

test-user:
	cd services/user-service && pytest

test-unit:
	cd services/user-service && pytest tests/unit -v

test-integration:
	cd services/user-service && pytest tests/integration -v

test-cov:
	cd services/user-service && pytest --cov=app --cov-report=html --cov-fail-under=80