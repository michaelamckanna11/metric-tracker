Metric Tracker API

This API tracks response times for any HTTP endpoint so you can monitor performance over time.
Planned endpoints:

GET /metrics – list all metrics

POST /metrics – add a metric (url, status_code, response_time, timestamp)

GET /metrics/{id} – view a single metric

DELETE /metrics/{id} – remove a metric

Data model: each metric has an id, url, status_code, response_time, and timestamp.