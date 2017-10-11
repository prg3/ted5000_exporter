FROM python:2.7-alpine
MAINTAINER Paul Greidanus <paul@majestik.org>
RUN pip install tornado
COPY . .
CMD [ "python", "./ted5000_exporter.py" ]
