FROM python:3.9.12-alpine3.15

RUN mkdir /app
WORKDIR /app

COPY src/requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/requestcounter.py /app
COPY src/build-info /app/build-info

RUN "md5sum /app/requestcounter.py > /app/build-info/build.signature"

EXPOSE 5555
CMD [ "python3", "./requestcounter.py" ]
