from typing import Dict, List
import boto3
from datetime import datetime

class EC2Collector:
    def collect(self, client) -> List[Dict]:
        """Collect EC2 instance inventory."""
        try:
            response = client.describe_instances()
            
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_data = {
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                        'Tags': instance.get('Tags', []),
                        'LaunchTime': instance['LaunchTime'].isoformat(),
                        'VpcId': instance.get('VpcId'),
                        'SubnetId': instance.get('SubnetId'),
                        'Platform': instance.get('Platform', 'linux'),
                        'Architecture': instance.get('Architecture'),
                        'RootDeviceType': instance.get('RootDeviceType'),
                        'RootDeviceName': instance.get('RootDeviceName'),
                        'PublicIpAddress': instance.get('PublicIpAddress'),
                        'PrivateIpAddress': instance.get('PrivateIpAddress'),
                        'SecurityGroups': [
                            {
                                'GroupId': sg['GroupId'],
                                'GroupName': sg['GroupName']
                            }
                            for sg in instance.get('SecurityGroups', [])
                        ],
                        'IamInstanceProfile': instance.get('IamInstanceProfile', {}).get('Arn'),
                        'MetadataOptions': {
                            'HttpTokens': instance.get('MetadataOptions', {}).get('HttpTokens'),
                            'HttpEndpoint': instance.get('MetadataOptions', {}).get('HttpEndpoint'),
                            'HttpPutResponseHopLimit': instance.get('MetadataOptions', {}).get('HttpPutResponseHopLimit')
                        }
                    }
                    instances.append(instance_data)
            
            return instances
        except Exception as e:
            raise Exception(f"Error collecting EC2 inventory: {str(e)}") 