FROM python:3.10.10-alpine

ARG BUILD_SIGNATURE="dummysignature"
ARG BUILD_COMMIT_HASH="dummycommithash"
ARG BUILD_DATE="dummydate"

ENV BUILD_SIGNATURE=${BUILD_SIGNATURE}
ENV BUILD_COMMIT_HASH=${BUILD_COMMIT_HASH}
ENV BUILD_DATE=${BUILD_DATE}

RUN mkdir /app
WORKDIR /app

COPY src/requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/requestcounter.py /app
COPY src/build-info /app/build-info

RUN echo ${BUILD_SIGNATURE} > /app/build-info/build.signature
RUN echo ${BUILD_COMMIT_HASH} > /app/build-info/build.commithash
RUN echo ${BUILD_DATE} > /app/build-info/build.date

EXPOSE 5555
CMD [ "python3", "./requestcounter.py" ]
