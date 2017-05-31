FROM python:2.7

ADD jug /opt/jug

WORKDIR /opt/jug
RUN pip install -r requirements.txt

EXPOSE 8080
USER 1000
CMD gunicorn -w 5 --bind 0.0.0.0:8080 --access-logfile - demo:app
