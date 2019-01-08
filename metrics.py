from prometheus_client import start_http_server, Summary, Gauge
import tesla
import configparser
import os
import time
import sys

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

gauges = {
    "solar": {
        'solar_power': Gauge('home_solar_generation', 'The amount of solar power being produced', ['id']),
        'load_power':  Gauge('home_power_load', 'The amount of power being used by the house', ['id']),
        'grid_power':  Gauge('home_power_grid_usage', 'The amount of power being drawn from the grid', ['id'])
    }
}


# Decorate function with metric.
@REQUEST_TIME.time()
def polling(t):
    print("%s - Polling!" % time.time())

    for product in t.list_products():
        if product['resource_type'] in gauges:
            data = t.solar_status(product['energy_site_id'])['response']
            for gauge in gauges[product['resource_type']]:
                value = 0
                if gauge in data:
                    value = data[gauge]

                gauges[product['resource_type']][gauge].labels(product['id']).set(value)


if __name__ == '__main__':
    c = configparser.ConfigParser()
    c.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.ini'))
    access_token_cache_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), c['general']['access_token_cache'])
    tesla = tesla.Tesla(username=os.getenv("USERNAME", 'user@email.com'), password=os.getenv('PASSWORD', 'password'), key_cache_file=access_token_cache_file)

    # Start up the server to expose the metrics.
    start_http_server(8000)
    sys.stdout.write("Listening on port 8000...\n")

    while True:
        polling(tesla)
        time.sleep(15)
