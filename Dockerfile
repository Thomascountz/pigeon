FROM python:3.6-slim-buster
RUN pip3 install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp/ && pipenv lock --requirements > requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY . /app/
WORKDIR /app/
ENTRYPOINT ["python"]
CMD ["app.py"]
