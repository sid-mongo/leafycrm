FROM python:3-slim
EXPOSE 8080
ADD . .
RUN pip install Flask==2.2.5 pymongo[srv] Flask-PyMongo flask-cors dnspython
ENTRYPOINT ["python"]
CMD ["run.py"]