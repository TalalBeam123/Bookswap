FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8000

# Set an environment variable for the database URL, replace 'your_host_ip' with the actual IP address of your PostgreSQL server
# ENV DATABASE_URL "postgresql://user:db123@host.docker.internal:10000/bookswap"
# CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
