FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# need this to load static files via whitenoise
# RUN python manage.py collectstatic --noinput
# RUN SECRET_KEY=temp-build-key python manage.py collectstatic --noinput

EXPOSE 8000

# # use this as default, but in my case i need another command
# CMD ["gunicorn", "base.wsgi:application", "--bind", "0.0.0.0:8000"] 

# i will use script to do some actions
# makes file executable
RUN chmod +x entrypoint.sh

# starts script when starting the container
CMD [ "sh", "entrypoint.sh"]