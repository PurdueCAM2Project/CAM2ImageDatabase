FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN pip install mysql
RUN pip install pandas
CMD ["python", "connect_vitess.py"]