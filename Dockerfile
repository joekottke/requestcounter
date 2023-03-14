FROM python:3.9.12-slim-bullseye

RUN mkdir /app
WORKDIR /app

COPY src/requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/requestcounter.py /app
COPY src/proto /app/proto
COPY src/build-info /app/build-info

RUN python -m grpc_tools.protoc --proto_path=./proto --python_out=. --grpc_python_out=. ./proto/gubernator.proto
RUN md5sum /app/requestcounter.py > /app/build-info/build.signature
RUN date > /app/build-info/build.date

EXPOSE 5555
CMD [ "python3", "./requestcounter.py" ]
