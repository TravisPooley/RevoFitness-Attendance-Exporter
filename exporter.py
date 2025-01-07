import requests
from prometheus_client import start_http_server, Gauge
from bs4 import BeautifulSoup
import time

interval = 10*60

# Define Prometheus gauge metrics
gym_count_metric = Gauge('revo_fitness_gym_count', 'Live gym occupancy count', ['gym_name'])

def scrape_gym_counts():
    """Scrape live gym member counts from the Revo Fitness website."""
    url = "https://revofitness.com.au/livemembercount/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        counts = {}

        # Find gym data from HTML
        for span in soup.find_all('span', attrs={'data-live-count': True}):
            gym_name = span['data-live-count']
            try:
                count = int(span.text.strip())
            except ValueError:
                count = -1  # Handle potential parsing issues gracefully
            counts[gym_name] = count

        return counts
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

if __name__ == '__main__':
    # Start Prometheus HTTP server
    start_http_server(8000)
    print("Prometheus exporter running on port 8000.")

    while True:
        gym_counts = scrape_gym_counts()
        for gym_name, count in gym_counts.items():
            print(f"Gym: {gym_name}, Count: {count}")
            # Set the value of the Prometheus metric
            gym_count_metric.labels(gym_name=gym_name).set(count)
        time.sleep(interval)  # Scrape every x minutes
