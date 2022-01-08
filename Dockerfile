FROM python:3.8-slim
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip3 install -r requirements.txt
ADD . /app
EXPOSE 8000
CMD ["gunicorn"  , "--bind", "0.0.0.0:8000","--chdir","/app", "app:app"]
