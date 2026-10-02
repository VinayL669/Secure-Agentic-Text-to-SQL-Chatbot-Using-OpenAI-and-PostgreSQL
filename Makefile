.PHONY: test test-security lint migrate
test:            ## run all tests (stdlib only; works without pytest)
	cd backend && python3 -m unittest discover -s tests -t . -p "test_*.py" -v
test-security:
	cd backend && python3 -m unittest discover -s tests/security -t . -p "test_*.py" -v
lint:
	cd backend && ruff check app tests
migrate:
	cd backend && alembic upgrade head
