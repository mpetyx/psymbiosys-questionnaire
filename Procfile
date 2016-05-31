web: gunicorn psy_questions.wsgi --log-file -
celery_sending_emails_worker: celery -A psy_questions worker -l info
celery_regular_emails_beat: celery -A psy_questions beat -l info
# celery flower -A psy_questions --address=127.0.0.1 --port=5555
