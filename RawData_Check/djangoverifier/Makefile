.PHONY: frontend
frontend:
	cd frontend && npm start

.PHONY: backend
backend: start_redis
	pipenv install && pipenv shell "pipenv install django && cd backend && python manage.py makemigrations && python manage.py migrate && python manage.py runserver"

start_redis:
	killall redis-server || true
	redis-server &