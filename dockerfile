FROM tiangolo/uwsgi-nginx-flask

RUN pip3 install --upgrade pip

COPY ./app /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /app
EXPOSE 80
