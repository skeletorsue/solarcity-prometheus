# Prometheus client for Tesla (SolarCity) API

This is a client application which fetches the following from the Tesla API
- Solar power generation
- System power consumption
- Grid power draw 

## To Run
`docker run -d -e "USERNAME=user@email.com" -e "PASSWORD=password" -p 8080:8000 skeletorsue/solarcity-prometheus:latest`

## Dev environment
`docker run --rm -ti -e "USERNAME=user@email.com" -e "PASSWORD=password" -v $(pwd):/app -w /app --entrypoint sh -p 8080:8000 python:3-alpine`

- pip install -r requirements.txt
- python metrics.py
