FROM python:2.7
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
expose 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

