# Cloud

AWS API examples and EC2 bootstrap scripts.

## Contents

| Path | Type | Covers |
|------|------|--------|
| [`aws/examples.py`](aws/examples.py) | boto3 examples | EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, CloudFormation, Route53 |
| [`iac/ubuntu-userdata.sh`](iac/ubuntu-userdata.sh) | EC2 UserData | Ubuntu 22.04: Docker, CloudWatch agent, sysctl hardening |
| [`iac/windows-userdata.ps1`](iac/windows-userdata.ps1) | EC2 UserData | Windows Server 2022: Chocolatey, IIS, CloudWatch agent, TLS/SMB hardening |

## Setup

```bash
cp cloud/.env.example cloud/.env   # add your credentials
pip install boto3 python-dotenv
```

Alternatively, use a named AWS profile:
```bash
export AWS_PROFILE=myprofile
python cloud/aws/examples.py --region us-west-2
```

---

## AWS

**Docs:** https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

### Quick start

```bash
# Read-only (lists resources across all covered services):
python CLOUD/aws/examples.py

# Target a specific region:
python cloud/aws/examples.py --region us-west-2

# Write demo (uploads then deletes a test S3 object):
python CLOUD/aws/examples.py --demo-write --bucket my-bucket
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `AWS_REGION` | No | Target region (default: `us-east-1`) |
| `AWS_PROFILE` | No | Named profile from `~/.aws/credentials` |
| `AWS_ACCESS_KEY_ID` | Alt to profile | Explicit credentials |
| `AWS_SECRET_ACCESS_KEY` | Alt to profile | Explicit credentials |
| `AWS_S3_BUCKET` | Write demo | Bucket for S3 write operations |

### Function reference

| Function | Service | Description |
|----------|---------|-------------|
| `list_instances` | EC2 | All instances with state and type |
| `list_vpcs` | EC2 | VPCs with CIDR and default flag |
| `list_security_groups` | EC2 | Security groups |
| `list_key_pairs` | EC2 | EC2 key pairs |
| `list_buckets` | S3 | All S3 buckets (global) |
| `list_objects` | S3 | Objects in a bucket |
| `get_bucket_policy` | S3 | Bucket policy JSON |
| `upload_object` | S3 | Put a text object |
| `delete_object` | S3 | Delete an object |
| `generate_presigned_url` | S3 | Time-limited GET URL |
| `get_account_summary` | IAM | Account-level quotas and counts |
| `list_users_iam` | IAM | All IAM users |
| `list_roles` | IAM | All IAM roles |
| `list_policies` | IAM | Customer-managed or AWS policies |
| `list_parameters` | SSM | Parameter Store entries |
| `get_parameter` | SSM | Single parameter value (with decryption) |
| `put_parameter` | SSM | Create or update a parameter |
| `list_alarms` | CloudWatch | Metric alarms and state |
| `get_metric_statistics` | CloudWatch | Datapoints for a namespace/metric |
| `list_log_groups` | CloudWatch Logs | Log groups with storage size |
| `list_lambdas` | Lambda | All functions with runtime and memory |
| `invoke_lambda` | Lambda | Invoke a function synchronously |
| `list_rds_instances` | RDS | DB instances with status and engine |
| `list_rds_snapshots` | RDS | DB snapshots |
| `list_clusters` | ECS | Cluster ARNs |
| `list_services` | ECS | Services in a cluster with counts |
| `list_stacks` | CloudFormation | Stacks by status |
| `get_stack_outputs` | CloudFormation | Output key/value pairs |
| `list_hosted_zones` | Route 53 | Hosted zones (global) |
| `list_records` | Route 53 | Resource record sets in a zone |
