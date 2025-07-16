#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import json
from time import sleep

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models

def update_certificate(client, old_certificate_id, pubkey, privkey, tag, resource_types):
    
    req = models.UpdateCertificateInstanceRequest()
    params = {
            "OldCertificateId": old_certificate_id,
            "CertificatePublicKey": pubkey,
            "CertificatePrivateKey": privkey,
            "ResourceTypes": resource_types,
            'ExpiringNotificationSwitch': 1,
            "Tags": [
                {
                    "TagKey": "ssl-tag",
                    "TagValue": tag
                }
            ]
        } 
    
    req.from_json_string(json.dumps(params))
    
    try:
        resp = client.UpdateCertificateInstance(req)
        return resp.to_json_string()
    
    except TencentCloudSDKException as err:
        print(err)
        return None
    

def find_certificate_id(client, tag):
    req = models.DescribeCertificatesRequest()
    
    params = {
        "Tags": [
            {
                "TagKey": "ssl-tag",
                "TagValue": tag
            }
        ],
        "Limit": 1
    }

    req.from_json_string(json.dumps(params))

    try:
        resp = client.DescribeCertificates(req)
        if resp.TotalCount > 0:
            return resp.Certificates[0].CertificateId
        else:
            print('Error: certificate not found.')
            return None
    except TencentCloudSDKException as err:
        print(err)
        return None
    
def delete_certificate(client, certificate_id):
    req = models.DeleteCertificateRequest()
    
    params = {
        "CertificateId": certificate_id
    }
    
    req.from_json_string(json.dumps(params))
    
    try:
        resp = client.DeleteCertificate(req)
        return resp.to_json_string()
    except TencentCloudSDKException as err:
        print(err)
        return None

def main():
    parser = argparse.ArgumentParser(description='Update old certificate in tencent cloud ssl')
    parser.add_argument('oldCertificateTag', type=str, help='the certificate you want to update')
    parser.add_argument('pubkey', type=str, help='path to your pubkey')
    parser.add_argument('privkey', type=str, help='path to your privkey')
    parser.add_argument('--resourceTypes', type=str, nargs='*', default=['teo', 'cdn', 'clb', 'vpc', 'waf'], help='resource types to update the certificate for')
    
    args = parser.parse_args()
    
    if (os.getenv('TENCENTCLOUD_SECRET_ID') == None):
        print('Error: TENCENTCLOUD_SECRET_ID is needed in env.')
        return 1
        
    if (os.getenv('TENCENTCLOUD_SECRET_KEY') == None):
        print('Error: TENCENTCLOUD_SECRET_KEY is needed in env.')
        return 1
    
    with open(args.pubkey, 'r') as f:
        pubkey = f.read()
    
    if not pubkey.startswith('-----BEGIN CERTIFICATE-----'):
        print('Error: pubkey is not a valid certificate.')
        return 1
    
    with open(args.privkey, 'r') as f:
        privkey = f.read()
        
    if not privkey.startswith('-----BEGIN'):
        print('Error: privkey is not a valid private key.')
        return 1
        
    try:
        cred = credential.Credential(os.getenv("TENCENTCLOUD_SECRET_ID"), os.getenv("TENCENTCLOUD_SECRET_KEY"))
        
        client = ssl_client.SslClient(cred, "")
        
        old_certificate_id = find_certificate_id(client, args.oldCertificateTag)

        print('old_cert: ' + old_certificate_id)

        print('update_cert: ' + update_certificate(client, old_certificate_id, pubkey, privkey, args.oldCertificateTag, args.resourceTypes))
        
        sleep(10) # Wait for the update to take effect

        print('delete_old_cert: ' + delete_certificate(client, old_certificate_id))
        
        print('new_cert: ' + find_certificate_id(client, args.oldCertificateTag))
        
        print('Certificate updated successfully.')

    except TencentCloudSDKException as err:
        print(err)
        return 1

    return 0

if __name__ == '__main__':
    main()