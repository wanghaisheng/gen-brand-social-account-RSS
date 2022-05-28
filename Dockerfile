FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r dev.txt

COPY . .

CMD [ "python", "./feed.py" ]
