"""
#############################################################
#    server side encryption - kms clean up for usecase-1    #
#############################################################
"""
from pathlib import Path
import subprocess
import sys
import os 
import json
import boto3

def main():
    """
    #######################################################
    #     Cleaning up all S3 buckets and files created    #
    #######################################################
    """
    try:
        az = subprocess.check_output(['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone'])
        list_az = az.split('-')
        region = list_az[0]+ '-' + list_az[1] + '-' + list_az[2][0]
        s3_client = boto3.client('s3', region)
        cf_client = boto3.client('cloudformation')
        
        response = cf_client.list_stacks(
            StackStatusFilter=[
                'CREATE_COMPLETE',
            ]
        )
        
        for stack in response['StackSummaries']:
            if stack['StackName'] == 'data-protection-env-setup':
                response = cf_client.delete_stack(
                    StackName='data-protection-env-setup',
                )
                
            if stack['StackName'] == 'data-protection-iam-user-creation':
                response = cf_client.delete_stack(
                    StackName='data-protection-iam-user-creation',
                )
        
        print "\n Final Cleanup Successful" 
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
    