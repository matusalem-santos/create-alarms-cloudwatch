import boto3
import sys
import time

region = 'us-east-1'
#AWS Account and Region Definition for Reboot Actions

cw = boto3.client('cloudwatch',region_name=region)


def lambda_handler(event, context):

    response = cw.describe_alarms(
        StateValue='INSUFFICIENT_DATA'
      )
 
    alarms = response['MetricAlarms']
    for alarm in alarms:
        try:
            alarm_name = alarm['AlarmName']
            print (alarm_name)
            cw.delete_alarms(
            AlarmNames=[alarm_name]
            )
 
        except Exception as e:
            print ("Error Encountered.")
            print (e)
