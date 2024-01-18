# Testing
In this directory, you will find some the tests for the project.
## Locust
This is a load testing tool that can be used to test the performance of the APIs. It can be used to simulate a large number of users and see how the system behaves under load. It can be used to test the APIs in the following way:
1. Install Locust using pip
```bash
pip install locust
```
2. Create a file called `locustfile.py` with the following contents:
```python
from locust import HttpUser, task, between
import pandas as pd

class QuickstartUser(HttpUser):
    wait_time = between(0.2, 0.2)
    @task
    def ping(self):
        id_column = 'id'
        csv_data = pd.read_csv("head2.csv", index_col=id_column)
        data = csv_data.to_csv(index=id_column)
        self.client.post("/predictions/logreg", data=data, headers={'Content-Type': 'text/csv'})
```
3. Run the locust command
```bash
locust
```
4. Open the locust UI in the browser at http://localhost:8089 and see the results

## Test APIs using k6s.io
1. To test k6s you need to install it first. To make it easy i used docker container to run it. In first you must clone this repository because there are all needed files to create all containers to run k6s. More info are [here](https://webcache.googleusercontent.com/search?q=cache:https://medium.com/swlh/beautiful-load-testing-with-k6-and-docker-compose-4454edb3a2e3).
```bash
git clone https://github.com/luketn/docker-k6-grafana-influxdb.git
cd docker-k6-grafana-influxdb
```
After that run this command to run grafana and influxdb:
```bash
docker compose up -d influxdb grafana
```
2. Now you can run your test. In my case i used this command:
```bash
docker compose run k6 run /path/to/script-test.js
```
3. After this you can see the dashboard in grafana at http://localhost:3000/d/k6/k6-load-testing-results 

## Read metrics
Now you can collect all needed metrcis to see how your application works. GOOD LUCK!