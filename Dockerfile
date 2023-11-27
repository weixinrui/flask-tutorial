FROM alpine:3.15

ENV SRC_PATH=/usr/src \
    WORKDIR=${SRC_PATH} \
    TZ=Asia/Shanghai

COPY . ${SRC_PATH}/flask-tutorial

WORKDIR ${SRC_PATH}/flask-tutorial

RUN echo "https://mirrors.aliyun.com/alpine/v3.15/main/" > /etc/apk/repositories \
    && echo "https://mirrors.aliyun.com/alpine/v3.15/community/" >> /etc/apk/repositories \
    && apk update \
    # install software
    # && apk add --no-cache uwsgi python3 tzdata \
    && apk add --no-cache gcc g++ musl-dev linux-headers python3-dev libpq-dev tzdata \
    # download and install pip  # there's compatibility issues of py3-pip #
    # && wget --no-check-certificate -P /tmp/ https://bootstrap.pypa.io/get-pip.py \
    # && python3 /tmp/get-pip.py -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
    && python3 -m ensurepip --upgrade
    # add local pip source and install packages for building manual
RUN  pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN  pip3 install --no-cache-dir -U waitress
RUN  pip3 install --no-cache-dir -U wheel
RUN  pip3 install --no-cache-dir -U setuptools
RUN  python3 ./setup.py bdist_wheel
RUN  pip3 install ./dist/flaskr-1.0.0-py3-none-any.whl
    # set timezone
RUN  cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN  echo "Asia/Shanghai" > /etc/timezone
    # clean
    # && rm -rf /tmp/get-pip.py \ 
RUN pip3 cache purge
RUN apk del --purge gcc g++ musl-dev linux-headers

WORKDIR /
RUN flask --app flaskr init-db

CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "--call", "flaskr:create_app"]

EXPOSE 5000
