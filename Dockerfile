FROM python:3.6
WORKDIR /usr/src/tests
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
