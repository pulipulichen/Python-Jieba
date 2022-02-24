#Specify the version of nodejs.
FROM python:2

#Creating an application directory
RUN mkdir /app
#Use app directory as development directory
WORKDIR /app

#Package in container.json and packate-lock.Make sure that two of json are copied
#COPY requirements.txt ./
# package.Install the package described in json.
#RUN npm i

#installed node_Copy files such as module to the container side.
#COPY . .

#RUN ls /app/*

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --upgrade --no-deps --force-reinstall pathlib

CMD [ "python", "./python-scripts/run_jieba.py" ]