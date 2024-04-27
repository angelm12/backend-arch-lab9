FROM python:3.10
EXPOSE 5000 (remove)
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt (modify)
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"] (modify)
