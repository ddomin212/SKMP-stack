FROM python:3.10.7
WORKDIR /app
COPY . /app/app.py
RUN pip install kafka-python mysql-connector-python
CMD ["python", "app.py"]