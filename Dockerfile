FROM python:3.8

RUN useradd --create-home userapi
WORKDIR /flask_api_course

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./ .

RUN chown -R userapi:userapi ./
USER userapi

EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
