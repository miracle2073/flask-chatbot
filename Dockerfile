FROM frolvlad/alpine-python-machinelearning

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

ADD . /app/

EXPOSE 8000

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python3.6", "app.py"]
