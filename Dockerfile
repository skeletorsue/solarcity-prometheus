FROM python:3-alpine

LABEL org.opencontainers.image.authors="chris.staley@unixtime.site" \
      org.opencontainers.image.source="https://github.com/dmegyesi/solarcity-prometheus"

EXPOSE 8000

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["/app/metrics.py"]
