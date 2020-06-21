# Prometheus exporter for TED5000 

This is an exporter for TED5000 home monitoring devices. (https://www.ted5000.ca/)

## Installation

Just execute the python script. Ensure that you have Python-Tornado installed

## Usage

./ted5000_exporter.py

## Configuration

There is no configuration required

Testing can be done by testing with /metrics?target=127.0.0.1

example:

curl localhost:9747/metrics?target=192.168.0.23

## Prometheus Configuration

The ted5000 exporter needs to be passed the address as a parameter, this can be
done with relabelling.

Example config:
```YAML
scrape_configs:
  - job_name: 'ted5000'
    static_configs:
      - targets:
        - 192.168.1.2  # TED5000 device.
    metrics_path: /metrics
    params:
      module: [if_mib]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9747  # TED5000 exporter.
```

This setup allows Prometheus to provide scheduling and service discovery, as
unlike all other exporters running an exporter on the machine from which we are
getting the metrics from is not possible.
