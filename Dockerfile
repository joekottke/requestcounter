FROM python:3.10.10-alpine

RUN mkdir /app
WORKDIR /app

COPY src/requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/requestcounter.py /app
COPY src/build-info /app/build-info

EXPOSE 5555
CMD [ "python3", "./requestcounter.py" ]
