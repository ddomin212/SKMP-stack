FROM python:3.10.7
WORKDIR /app
COPY . /app
RUN pip install streamlit python-dotenv streamlit-autorefresh mysql-connector-python
CMD ["streamlit", "run", "viz.py"]