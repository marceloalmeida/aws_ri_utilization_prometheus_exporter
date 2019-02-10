# Copyright 2019 Paul Sczurek pocketcalculatorshow@gmail.com
#
#!/usr/bin/env python3

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import time
import os
import sys
import boto3
import datetime


def getAWSRIMetrics():
    client = boto3.client('ce')
    now = datetime.datetime.utcnow()
    end = datetime.datetime(year=now.year, month=now.month, day=now.day)
    # cost explorer provides updates daily so get yesterday's data
    end = end - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=1)
    start = start.strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')

    response = client.get_reservation_utilization(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity='DAILY'
    )

    net_ri_savings = response['Total']['NetRISavings']
    total_potential_ri_savings = response['Total']['TotalPotentialRISavings']
    total_amortized_fee = response['Total']['TotalAmortizedFee']
    utilization_percentage = response['Total']['UtilizationPercentage']
    purchased_hours = response['Total']['PurchasedHours']
    total_actual_hours = response['Total']['TotalActualHours']
    amortized_recurring_fee = response['Total']['AmortizedRecurringFee']
    unused_hours = response['Total']['UnusedHours']
    on_demand_cost_of_ri_hours_used = response['Total']['OnDemandCostOfRIHoursUsed']
    amortized_upfront_fee = response['Total']['AmortizedUpfrontFee']

    riValues = {
        'net_ri_savings': net_ri_savings,
        'total_potential_ri_savings': total_potential_ri_savings,
        'total_amortized_fee': total_amortized_fee,
        'utilization_percentage': utilization_percentage,
        'purchased_hours': purchased_hours,
        'total_actual_hours': total_actual_hours,
        'amortized_recurring_fee': amortized_recurring_fee,
        'unused_hours': unused_hours,
        'on_demand_cost_of_ri_hours_used': on_demand_cost_of_ri_hours_used,
        'amortized_upfront_fee': amortized_upfront_fee
    }

    return riValues


class awsRIUtilizationExporter(object):
    def collect(self):
        metric = GaugeMetricFamily(
            'reservation_utilization', 'Daily Reserved Instance Data', labels=["ri_metric"])
        for key, value in getAWSRIMetrics().items():
            metric.add_sample('reservation_utilization',
                              value=value, labels={'ri_metric': key})
        yield metric


if __name__ == '__main__':
	port = os.getenv('PORT', 9250)
	if len(sys.argv) > 2:
		print("Usage: awsRIUtilizationExporter.py [PORT]")
	else:
		if len(sys.argv) == 2:
	            port = int(sys.argv[1])
	            print('starting AWS RI Utilization Exporter on port %d' % port)
		else:
			print('starting AWS RI Utilization Exporter on default port 9250')
		start_http_server(port)
		REGISTRY.register(awsRIUtilizationExporter())
		while True:
			time.sleep(1)
