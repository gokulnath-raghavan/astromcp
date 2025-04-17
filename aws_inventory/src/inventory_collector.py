import boto3
import json
import logging
from datetime import datetime
from typing import Dict, List
from collectors.ec2_collector import EC2Collector
from collectors.s3_collector import S3Collector
from collectors.rds_collector import RDSCollector
from collectors.lambda_collector import LambdaCollector
from collectors.iam_collector import IAMCollector
from utils.aws_client import get_aws_client
from utils.logging import setup_logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSInventoryCollector:
    def __init__(self, regions: List[str] = None):
        self.regions = regions or ['us-east-1']
        self.logger = setup_logging()
        self.collectors = {
            'ec2': EC2Collector(),
            's3': S3Collector(),
            'rds': RDSCollector(),
            'lambda': LambdaCollector(),
            'iam': IAMCollector()
        }

    def collect_inventory(self) -> Dict:
        """Collect inventory from all supported AWS services."""
        inventory = {
            'timestamp': datetime.utcnow().isoformat(),
            'regions': self.regions,
            'resources': {}
        }

        for region in self.regions:
            self.logger.info(f"Collecting inventory for region: {region}")
            inventory['resources'][region] = {}

            for service, collector in self.collectors.items():
                try:
                    self.logger.info(f"Collecting {service} resources...")
                    client = get_aws_client(service, region)
                    resources = collector.collect(client)
                    inventory['resources'][region][service] = resources
                except Exception as e:
                    self.logger.error(f"Error collecting {service} resources: {str(e)}")
                    inventory['resources'][region][service] = {'error': str(e)}

        return inventory

    def save_inventory(self, inventory: Dict, bucket: str, key: str):
        """Save inventory data to S3."""
        try:
            s3_client = get_aws_client('s3')
            s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(inventory, indent=2),
                ContentType='application/json'
            )
            self.logger.info(f"Inventory saved to s3://{bucket}/{key}")
        except Exception as e:
            self.logger.error(f"Error saving inventory: {str(e)}")
            raise

def main():
    # Get regions from environment variable or use default
    regions = os.getenv('AWS_REGIONS', 'us-east-1').split(',')
    
    # Initialize collector
    collector = AWSInventoryCollector(regions)
    
    # Collect inventory
    inventory = collector.collect_inventory()
    
    # Save to S3
    bucket = os.getenv('INVENTORY_BUCKET', 'aws-inventory-inventory')
    key = f"inventory/{datetime.utcnow().strftime('%Y/%m/%d/%H%M%S')}.json"
    
    collector.save_inventory(inventory, bucket, key)

if __name__ == '__main__':
    main() 