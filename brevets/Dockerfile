FROM python:3.8
LABEL maintainer="dkim11@uroegon.edu"
RUN apt-get update -y
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-B"]
CMD ["flask_brevets.py"]
