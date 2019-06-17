FROM python:3

ADD aws-ri-utilization-prometheus-exporter.py /

RUN pip3 install boto3 
RUN pip3 install prometheus_client

CMD [ "python", "./aws-ri-utilization-prometheus-exporter.py" ]
