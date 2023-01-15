web: gunicorn main:app --workers=4 --worker-class=uvicorn.workers.UvicornWorker
revision: alembic revision --autogenerate
upgrade: alembic upgrade head
