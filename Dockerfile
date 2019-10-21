FROM python:3.8-alpine

COPY . /opt/app

WORKDIR /opt/app
RUN pip install -r requirements.txt

ENV FLASK_APP=flaskr
ENV FLASK_ENV=development

EXPOSE 5000
CMD python -m flask init-db && python -m flask run --host=0.0.0.0
