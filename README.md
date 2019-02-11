# Prometheus RI Utilization Exporter

# Description

This exporter pulls EC2 Reserved Instance utilization metrics from the AWS Cost Explorer API. Since Cost Explorer updates only once per day, the exporter pulls yesterday's data only. The exporter provides the following RI Utilization data:

     AmortizedRecurringFee
     AmortizedUpfrontFee
     NetRISavings
     OnDemandCostOfRIHoursUsed
     PurchasedHours
     PurchasedUnits
     TotalActualHours
     TotalActualUnits
     TotalAmortizedFee
     TotalPotentialRISavings
     UnusedHours
     UnusedUnits
     UtilizationPercentage
     UtilizationPercentageInUnits
     
# Authentication

The RI utilization exporter uses Boto 3 so the running user's aws/credentials file will need to configured appropriately.

# Usage

./aws-ri-utilization-prometheus-exporter.py [PORT]

By default the exporter runs on 9250 but a custom port can be specified from the command line.

# Docker

docker run --restart always -d -p 9250:9250 -e AWS_DEFAULT_REGION="XXXX" -e AWS_ACCESS_KEY_ID="XXXXXX" -e AWS_SECRET_ACCESS_KEY="XXXXX" psczurekadapture/aws-ri-utilization-prometheus-exporter:latest

# Prometheus config

```
- job_name: aws-ri-utilization-prometheus-exporter
  scrape_interval: 43200s
  scrape_timeout: 60s
  static_configs:
  - targets:
    - localhost:9250
```

# AWS IAM Policy
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:*"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
