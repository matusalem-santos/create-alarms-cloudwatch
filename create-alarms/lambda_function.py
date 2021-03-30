import boto3
import os

cw = boto3.client('cloudwatch')
ec2 = boto3.resource('ec2')
region = 'us-east-1'
# SNS Topic
# sns_pager = os.environ['sns_pager_arn']
# sns_slack = os.environ['sns_slack_arn']

def lambda_handler(event, context):

    ids=get_instances()
    for id in ids:
        create_alarm(id)                 

def create_alarm(instanceid):
        
    instance_name = get_instance_name(instanceid)
    
    #Create Alarm disk_used_percent and 
    for metric in cw.list_metrics(Dimensions=[{'Name': 'InstanceId', 'Value': instanceid}])['Metrics']:
            if metric['MetricName'] == 'disk_used_percent' :
                create_alarm_disk(instance_name,instanceid,metric['Dimensions'][0]['Value'] , metric['Dimensions'][2]['Value'], metric['Dimensions'][3]['Value'])
            if metric['MetricName'] == 'mem_used_percent':
                create_alarm_mem(instance_name, instanceid)


    # Create Alarm "CPU Utilization Greater than 95% for 10+ Minutes"
    cw.put_metric_alarm(
        AlarmName=instance_name+"-"+instanceid+" Utilização de CPU > 95%",
        AlarmDescription='Utilização de CPU > 95% por 10+ Minutos',
        ActionsEnabled=True,
        # OKActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        # AlarmActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceid
            },
        ],
        Period=300,
        EvaluationPeriods=2,
        Threshold=95.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold'
    )
    
    # Create Metric "Status Check Failed (System) for 5 Minutes"
    cw.put_metric_alarm(
        AlarmName=instance_name+"-"+instanceid+" System Check Failed",
        AlarmDescription='Status Check Failed (System) for 5 Minutes',
        ActionsEnabled=True,
        # OKActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        # AlarmActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        MetricName='StatusCheckFailed_System',
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceid
            },
        ],
        Period=60,
        EvaluationPeriods=5,# tempo em minutos
        Threshold=1.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold'
    )

    # Create Alarm "Status Check Failed (Instance) for 20 Minutes"
    cw.put_metric_alarm(
        AlarmName=instance_name+"-"+instanceid+" Instance Check Failed",
        AlarmDescription='Status Check Failed (Instance) for 20 Minutes',
        ActionsEnabled=True,
        # OKActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        # AlarmActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        MetricName='StatusCheckFailed_Instance',
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceid
            },
        ],
        Period=60,
        EvaluationPeriods=20,# tempo em minutos
        Threshold=1.0,
        ComparisonOperator='GreaterThanOrEqualToThreshold'
    )

    #List All Devices of the Instance
    ec2d = boto3.resource('ec2', region_name= region)
    instance = ec2d.Instance(instanceid)
    vol_id = instance.volumes.all()
    devices = instance.block_device_mappings


        
    for v in vol_id:
        dev = [ dev['DeviceName'] for dev in devices if dev['Ebs']['VolumeId'] == v.id ]
    
        #Create Alarm device disk
        create_alarm_disk_dev(instanceid,v,dev)


def create_alarm_mem(instance_name, instanceid):
     # Create Alarm "MemoryUtilization Utilization More than 95% for 3+ Minutes"
    cw.put_metric_alarm(
        AlarmName=instance_name+"-"+instanceid+" Utilização de memória > 95%",
        AlarmDescription='Utilização de memória > 95% por 5+ Minutos',
        ActionsEnabled=True,
        # OKActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        # AlarmActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        MetricName='mem_used_percent',
        Namespace='CWAgent',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceid
            },
        ],
        Period=60,
        EvaluationPeriods=5,# tempo em minutos
        Threshold=95,
        ComparisonOperator='GreaterThanOrEqualToThreshold'
    )
    

def get_instance_name(fid):
    # When given an instance ID as str e.g. 'i-1234567', return the instance 'Name' from the name tag.
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(fid)
    instancename = ''
    try:
        for tags in ec2instance.tags:
            if tags["Key"] == 'Name':
                instancename = tags["Value"]
        return instancename
    except Exception as e:
        return fid

def get_instances():
    # Retorna os ids das intancias 
    ec2 = boto3.resource('ec2')
    ec2instances = ec2.instances.all()
    ids = []
    for instance in ec2instances:
        if instance.state['Name'] == 'running':
            ids.append(instance.id)
    return ids

def create_alarm_disk(instance_name,instanceid,path,device,fstype):

    cw.put_metric_alarm(
        AlarmName=instance_name+"-"+instanceid+" Utilização de disco > 95% no "+path,
        AlarmDescription="Utilização de disco > 95% no "+path,
        ActionsEnabled=True,
        # OKActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        # AlarmActions=[
        #     sns_slack,
        #     sns_pager
        # ],
        MetricName='disk_used_percent',
        Namespace='CWAgent',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instanceid
            },
             {
                'Name': 'device',
                'Value': device
            },
             {
                'Name': 'fstype',
                'Value': fstype
            },
            {
                'Name': 'path',
                'Value': path
            },
        ],
        Period=60,
        EvaluationPeriods=1,
        Threshold=95,
        ComparisonOperator='GreaterThanThreshold'
    )

def create_alarm_disk_dev(instanceid,v,dev):

    # Create Alarm "Volume Idle Time < 0 sec (of 5 minutes) for 60 Minutes"
    cw.put_metric_alarm(
        AlarmName=v.id+" "+instanceid+" "+dev[0]+" High Volume Activity Critical",
        AlarmDescription='Volume Idle Time <= 30 sec (of 5 minutes) for 60 Minutes',
        ActionsEnabled=True,
        # OKActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        # AlarmActions=[
        #     sns_pager,
        #     sns_slack
        # ],
        MetricName='VolumeIdleTime',
        Namespace='AWS/EBS',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'VolumeId',
                'Value': v.id
            },
        ],
        Period=300,
        EvaluationPeriods=12, # tempo em minutos
        Threshold=30.0,
        ComparisonOperator='LessThanOrEqualToThreshold'
    )
