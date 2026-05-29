"""
AWS boto3 Examples
Covers: EC2, S3, IAM, SSM, CloudWatch, Lambda, RDS, ECS, Route53, CloudFormation

Auth:  AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY  (or AWS_PROFILE for named profiles)
       AWS_REGION  (default: us-east-1)
Docs:  https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

Usage:
    # Read-only demo (lists resources across services):
    python CLOUD/aws/examples.py

    # Target a specific region:
    python CLOUD/aws/examples.py --region us-west-2

    # Include write operations:
    python CLOUD/aws/examples.py --demo-write --bucket my-unique-bucket-name
"""

import argparse
import json
import os
import sys
import time

_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
_CLOUD_DIR   = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, os.path.dirname(_CLOUD_DIR))

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("ERROR: boto3 not installed. Run: pip install boto3", file=sys.stderr)
    sys.exit(1)


def _load_env(path: str) -> None:
    if not os.path.exists(path):
        return
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(path, override=False)
        return
    except ImportError:
        pass
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def load_env(env_file: str | None = None) -> None:
    for p in [env_file,
              os.path.join(_SCRIPT_DIR, ".env"),
              os.path.join(_CLOUD_DIR, ".env")]:
        if p and os.path.exists(p):
            _load_env(p)
            return


def client(service: str, region: str) -> "boto3.client":
    return boto3.client(service, region_name=region)


def resource(service: str, region: str) -> "boto3.resource":
    return boto3.resource(service, region_name=region)


# ---------------------------------------------------------------------------
# EC2
# ---------------------------------------------------------------------------

def list_instances(region: str, max_results: int = 20) -> list[dict]:
    """EC2: describe all instances"""
    ec2 = client("ec2", region)
    resp = ec2.describe_instances(MaxResults=max_results)
    instances = [i for r in resp["Reservations"] for i in r["Instances"]]
    print(f"\n[EC2 Instances] {region}  {len(instances)} returned:")
    for i in instances:
        name = next((t["Value"] for t in i.get("Tags", []) if t["Key"] == "Name"), "—")
        print(f"  {i['InstanceId']}  [{i['State']['Name']:10s}]  "
              f"{i['InstanceType']:14s}  {name}")
    return instances


def list_security_groups(region: str) -> list[dict]:
    """EC2: list security groups"""
    ec2 = client("ec2", region)
    sgs = ec2.describe_security_groups()["SecurityGroups"]
    print(f"\n[Security Groups] {region}  {len(sgs)} returned:")
    for sg in sgs[:15]:
        print(f"  {sg['GroupId']}  {sg['GroupName']:30s}  {sg.get('Description','')[:40]}")
    return sgs


def list_vpcs(region: str) -> list[dict]:
    """EC2: list VPCs"""
    ec2 = client("ec2", region)
    vpcs = ec2.describe_vpcs()["Vpcs"]
    print(f"\n[VPCs] {region}  {len(vpcs)} returned:")
    for vpc in vpcs:
        name = next((t["Value"] for t in vpc.get("Tags", []) if t["Key"] == "Name"), "—")
        default = " [default]" if vpc.get("IsDefault") else ""
        print(f"  {vpc['VpcId']}  {vpc['CidrBlock']}  {name}{default}")
    return vpcs


def list_key_pairs(region: str) -> list[dict]:
    """EC2: list key pairs"""
    ec2 = client("ec2", region)
    keys = ec2.describe_key_pairs()["KeyPairs"]
    print(f"\n[Key Pairs] {region}  {len(keys)} returned:")
    for k in keys:
        print(f"  {k['KeyPairId']}  {k['KeyName']}  ({k.get('KeyType','?')})")
    return keys


# ---------------------------------------------------------------------------
# S3
# ---------------------------------------------------------------------------

def list_buckets() -> list[dict]:
    """S3: list all buckets (global)"""
    s3 = boto3.client("s3")
    buckets = s3.list_buckets().get("Buckets", [])
    print(f"\n[S3 Buckets] {len(buckets)} returned:")
    for b in buckets:
        print(f"  {b['Name']:50s}  created {b['CreationDate'].strftime('%Y-%m-%d')}")
    return buckets


def list_objects(bucket: str, prefix: str = "", max_keys: int = 20) -> list[dict]:
    """S3: list objects in a bucket"""
    s3 = boto3.client("s3")
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=max_keys)
    objects = resp.get("Contents", [])
    print(f"\n[S3 Objects] s3://{bucket}/{prefix}  {len(objects)} returned:")
    for obj in objects:
        size_kb = obj["Size"] / 1024
        print(f"  {obj['Key']:60s}  {size_kb:8.1f} KB")
    return objects


def get_bucket_policy(bucket: str) -> str | None:
    """S3: get bucket policy"""
    s3 = boto3.client("s3")
    try:
        policy = s3.get_bucket_policy(Bucket=bucket)["Policy"]
        parsed = json.loads(policy)
        print(f"\n[S3 Policy] {bucket}:")
        print(f"  {len(parsed.get('Statement', []))} statement(s)")
        return policy
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
            print(f"\n[S3 Policy] {bucket}: no policy attached")
        else:
            raise
    return None


def upload_object(bucket: str, key: str, content: str,
                  content_type: str = "text/plain") -> None:
    """S3: put a text object"""
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=content.encode(),
                  ContentType=content_type)
    print(f"\n[S3 Upload] s3://{bucket}/{key}")


def delete_object(bucket: str, key: str) -> None:
    """S3: delete an object"""
    s3 = boto3.client("s3")
    s3.delete_object(Bucket=bucket, Key=key)
    print(f"\n[S3 Delete] s3://{bucket}/{key}")


def generate_presigned_url(bucket: str, key: str,
                            expires_in: int = 3600) -> str:
    """S3: generate a presigned GET URL"""
    s3 = boto3.client("s3")
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expires_in,
    )
    print(f"\n[Presigned URL] s3://{bucket}/{key} (expires {expires_in}s)")
    print(f"  {url[:80]}...")
    return url


# ---------------------------------------------------------------------------
# IAM
# ---------------------------------------------------------------------------

def list_users_iam() -> list[dict]:
    """IAM: list all users"""
    iam = boto3.client("iam")
    paginator = iam.get_paginator("list_users")
    users = [u for page in paginator.paginate() for u in page["Users"]]
    print(f"\n[IAM Users] {len(users)} returned:")
    for u in users[:20]:
        print(f"  {u['UserId']}  {u['UserName']:30s}  created {u['CreateDate'].strftime('%Y-%m-%d')}")
    return users


def list_roles() -> list[dict]:
    """IAM: list roles"""
    iam = boto3.client("iam")
    paginator = iam.get_paginator("list_roles")
    roles = [r for page in paginator.paginate() for r in page["Roles"]]
    print(f"\n[IAM Roles] {len(roles)} returned:")
    for r in roles[:20]:
        print(f"  {r['RoleId']}  {r['RoleName']}")
    return roles


def list_policies(scope: str = "Local") -> list[dict]:
    """IAM: list policies — scope: Local | AWS | All"""
    iam = boto3.client("iam")
    paginator = iam.get_paginator("list_policies")
    policies = [p for page in paginator.paginate(Scope=scope) for p in page["Policies"]]
    print(f"\n[IAM Policies ({scope})] {len(policies)} returned:")
    for p in policies[:20]:
        print(f"  {p['PolicyName']:50s}  attached: {p.get('AttachmentCount', 0)}")
    return policies


def get_account_summary() -> dict:
    """IAM: account-level summary and service quotas"""
    iam = boto3.client("iam")
    summary = iam.get_account_summary()["SummaryMap"]
    print(f"\n[IAM Account Summary]")
    for k in ["Users", "Roles", "Groups", "Policies", "MFADevices",
              "AccountMFAEnabled", "AccessKeysPerUserQuota"]:
        print(f"  {k}: {summary.get(k, '?')}")
    return summary


# ---------------------------------------------------------------------------
# SSM Parameter Store
# ---------------------------------------------------------------------------

def list_parameters(region: str, path: str = "/") -> list[dict]:
    """SSM: list parameters by path"""
    ssm = client("ssm", region)
    paginator = ssm.get_paginator("describe_parameters")
    params = [p for page in paginator.paginate() for p in page["Parameters"]]
    print(f"\n[SSM Parameters] {region}  {len(params)} returned:")
    for p in params[:20]:
        print(f"  {p['Name']:60s}  [{p['Type']}]")
    return params


def get_parameter(region: str, name: str, decrypt: bool = True) -> str:
    """SSM: get a single parameter value"""
    ssm = client("ssm", region)
    resp = ssm.get_parameter(Name=name, WithDecryption=decrypt)
    value = resp["Parameter"]["Value"]
    param_type = resp["Parameter"]["Type"]
    display = "***" if param_type == "SecureString" else value[:60]
    print(f"\n[SSM Parameter] {name}  [{param_type}]  value={display}")
    return value


def put_parameter(region: str, name: str, value: str,
                  param_type: str = "SecureString",
                  description: str = "") -> None:
    """SSM: create or update a parameter"""
    ssm = client("ssm", region)
    ssm.put_parameter(
        Name=name, Value=value, Type=param_type,
        Description=description, Overwrite=True,
    )
    print(f"\n[SSM Put] {name}  [{param_type}]")


# ---------------------------------------------------------------------------
# CloudWatch
# ---------------------------------------------------------------------------

def list_alarms(region: str, max_results: int = 20) -> list[dict]:
    """CloudWatch: list metric alarms"""
    cw = client("cloudwatch", region)
    alarms = cw.describe_alarms(MaxRecords=max_results)["MetricAlarms"]
    print(f"\n[CloudWatch Alarms] {region}  {len(alarms)} returned:")
    for a in alarms:
        print(f"  [{a['StateValue']:10s}]  {a['AlarmName'][:55]}")
    return alarms


def get_metric_statistics(region: str, namespace: str, metric_name: str,
                           dimensions: list[dict] | None = None,
                           period: int = 300, lookback_seconds: int = 3600) -> list[dict]:
    """CloudWatch: get metric statistics"""
    from datetime import datetime, timezone, timedelta
    cw = client("cloudwatch", region)
    now = datetime.now(timezone.utc)
    resp = cw.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions or [],
        StartTime=now - timedelta(seconds=lookback_seconds),
        EndTime=now,
        Period=period,
        Statistics=["Average", "Maximum"],
    )
    datapoints = sorted(resp["Datapoints"], key=lambda x: x["Timestamp"])
    print(f"\n[CloudWatch Metric] {namespace}/{metric_name}  "
          f"{len(datapoints)} datapoints:")
    for dp in datapoints[-5:]:
        print(f"  {dp['Timestamp'].strftime('%H:%M')}  "
              f"avg={dp.get('Average',0):.2f}  max={dp.get('Maximum',0):.2f}")
    return datapoints


def list_log_groups(region: str, max_results: int = 20) -> list[dict]:
    """CloudWatch Logs: list log groups"""
    logs = client("logs", region)
    groups = logs.describe_log_groups(limit=max_results)["logGroups"]
    print(f"\n[CloudWatch Log Groups] {region}  {len(groups)} returned:")
    for g in groups:
        size_mb = g.get("storedBytes", 0) / (1024 ** 2)
        print(f"  {g['logGroupName']:60s}  {size_mb:6.1f} MB")
    return groups


# ---------------------------------------------------------------------------
# Lambda
# ---------------------------------------------------------------------------

def list_lambdas(region: str) -> list[dict]:
    """Lambda: list all functions"""
    lam = client("lambda", region)
    paginator = lam.get_paginator("list_functions")
    functions = [f for page in paginator.paginate() for f in page["Functions"]]
    print(f"\n[Lambda Functions] {region}  {len(functions)} returned:")
    for f in functions[:20]:
        print(f"  {f['FunctionName']:40s}  [{f['Runtime']:12s}]  "
              f"{f['MemorySize']}MB  {f.get('LastModified','?')[:10]}")
    return functions


def invoke_lambda(region: str, function_name: str,
                  payload: dict | None = None,
                  invocation_type: str = "RequestResponse") -> dict:
    """Lambda: invoke a function
    invocation_type: RequestResponse | Event | DryRun
    """
    lam = client("lambda", region)
    resp = lam.invoke(
        FunctionName=function_name,
        InvocationType=invocation_type,
        Payload=json.dumps(payload or {}).encode(),
    )
    status = resp["StatusCode"]
    result = json.loads(resp["Payload"].read()) if invocation_type == "RequestResponse" else {}
    print(f"\n[Lambda Invoke] {function_name}  status={status}")
    if result:
        print(f"  response: {str(result)[:100]}")
    return result


# ---------------------------------------------------------------------------
# RDS
# ---------------------------------------------------------------------------

def list_rds_instances(region: str) -> list[dict]:
    """RDS: list DB instances"""
    rds = client("rds", region)
    instances = rds.describe_db_instances()["DBInstances"]
    print(f"\n[RDS Instances] {region}  {len(instances)} returned:")
    for db in instances:
        print(f"  {db['DBInstanceIdentifier']:30s}  [{db['DBInstanceStatus']:12s}]  "
              f"{db['DBInstanceClass']}  {db['Engine']}")
    return instances


def list_rds_snapshots(region: str, max_results: int = 10) -> list[dict]:
    """RDS: list DB snapshots"""
    rds = client("rds", region)
    snaps = rds.describe_db_snapshots(MaxRecords=max_results)["DBSnapshots"]
    print(f"\n[RDS Snapshots] {region}  {len(snaps)} returned:")
    for s in snaps:
        print(f"  {s['DBSnapshotIdentifier']:40s}  [{s['Status']}]  "
              f"{s.get('SnapshotCreateTime','?')}")
    return snaps


# ---------------------------------------------------------------------------
# ECS
# ---------------------------------------------------------------------------

def list_clusters(region: str) -> list[str]:
    """ECS: list cluster ARNs"""
    ecs = client("ecs", region)
    arns = ecs.list_clusters()["clusterArns"]
    print(f"\n[ECS Clusters] {region}  {len(arns)} returned:")
    for arn in arns:
        print(f"  {arn.split('/')[-1]}")
    return arns


def list_services(region: str, cluster: str) -> list[str]:
    """ECS: list services in a cluster"""
    ecs = client("ecs", region)
    arns = ecs.list_services(cluster=cluster)["serviceArns"]
    if arns:
        details = ecs.describe_services(cluster=cluster, services=arns)["services"]
        print(f"\n[ECS Services] {cluster}  {len(details)} returned:")
        for svc in details:
            print(f"  {svc['serviceName']:40s}  [{svc['status']:8s}]  "
                  f"desired={svc['desiredCount']} running={svc['runningCount']}")
    return arns


# ---------------------------------------------------------------------------
# CloudFormation
# ---------------------------------------------------------------------------

def list_stacks(region: str, status_filter: list[str] | None = None) -> list[dict]:
    """CloudFormation: list stacks"""
    cfn = client("cloudformation", region)
    filters = status_filter or [
        "CREATE_COMPLETE", "UPDATE_COMPLETE", "ROLLBACK_COMPLETE"
    ]
    stacks = cfn.list_stacks(StackStatusFilter=filters)["StackSummaries"]
    print(f"\n[CloudFormation Stacks] {region}  {len(stacks)} returned:")
    for s in stacks[:20]:
        print(f"  {s['StackName']:40s}  [{s['StackStatus']}]")
    return stacks


def get_stack_outputs(region: str, stack_name: str) -> list[dict]:
    """CloudFormation: get stack outputs"""
    cfn = client("cloudformation", region)
    stack = cfn.describe_stacks(StackName=stack_name)["Stacks"][0]
    outputs = stack.get("Outputs", [])
    print(f"\n[Stack Outputs] {stack_name}:")
    for o in outputs:
        print(f"  {o['OutputKey']:30s} = {o['OutputValue'][:60]}")
    return outputs


# ---------------------------------------------------------------------------
# Route 53
# ---------------------------------------------------------------------------

def list_hosted_zones() -> list[dict]:
    """Route 53: list hosted zones (global)"""
    r53 = boto3.client("route53")
    zones = r53.list_hosted_zones()["HostedZones"]
    print(f"\n[Route53 Hosted Zones] {len(zones)} returned:")
    for z in zones:
        private = " [private]" if z["Config"]["PrivateZone"] else ""
        print(f"  {z['Id'].split('/')[-1]}  {z['Name']}{private}  "
              f"records={z['ResourceRecordSetCount']}")
    return zones


def list_records(zone_id: str, max_results: int = 20) -> list[dict]:
    """Route 53: list resource record sets in a zone"""
    r53 = boto3.client("route53")
    records = r53.list_resource_record_sets(
        HostedZoneId=zone_id, MaxItems=str(max_results)
    )["ResourceRecordSets"]
    print(f"\n[Route53 Records] zone={zone_id}  {len(records)} returned:")
    for rec in records:
        values = ", ".join(
            r["Value"] for r in rec.get("ResourceRecords", [])
        )[:60] if rec.get("ResourceRecords") else "ALIAS"
        print(f"  {rec['Name']:40s}  [{rec['Type']:6s}]  {values}")
    return records


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="AWS boto3 examples")
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--region", default=None,
                        help="AWS region (overrides AWS_REGION env var)")
    parser.add_argument("--bucket", default=None,
                        help="S3 bucket name for write demo (overrides AWS_S3_BUCKET)")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write operations (uploads then deletes a test S3 object)")
    args = parser.parse_args()

    load_env(args.env_file)
    region = args.region or os.environ.get("AWS_REGION", "us-east-1")

    print(f"\n{'='*60}")
    print(f"AWS boto3 Examples  [{region}]")
    print(f"{'='*60}")

    # ── EC2 ──────────────────────────────────────────────────────────────────
    list_instances(region)
    list_vpcs(region)
    list_security_groups(region)
    list_key_pairs(region)

    # ── S3 ───────────────────────────────────────────────────────────────────
    list_buckets()

    # ── IAM ──────────────────────────────────────────────────────────────────
    get_account_summary()
    list_users_iam()
    list_roles()
    list_policies(scope="Local")

    # ── SSM ──────────────────────────────────────────────────────────────────
    list_parameters(region)

    # ── CloudWatch ───────────────────────────────────────────────────────────
    list_alarms(region)
    list_log_groups(region)
    get_metric_statistics(region, "AWS/EC2", "CPUUtilization")

    # ── Lambda ───────────────────────────────────────────────────────────────
    list_lambdas(region)

    # ── RDS ──────────────────────────────────────────────────────────────────
    list_rds_instances(region)

    # ── ECS ──────────────────────────────────────────────────────────────────
    cluster_arns = list_clusters(region)
    if cluster_arns:
        list_services(region, cluster_arns[0])

    # ── CloudFormation ───────────────────────────────────────────────────────
    list_stacks(region)

    # ── Route 53 ─────────────────────────────────────────────────────────────
    zones = list_hosted_zones()
    if zones:
        list_records(zones[0]["Id"].split("/")[-1])

    # ── Write operations (opt-in) ────────────────────────────────────────────
    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")

        bucket = args.bucket or os.environ.get("AWS_S3_BUCKET", "")
        if not bucket:
            print("\n[Write] Set AWS_S3_BUCKET or pass --bucket to test S3 writes")
        else:
            key = "examples-test/test-object.txt"
            upload_object(bucket, key, content="Hello from CLOUD/aws/examples.py")
            generate_presigned_url(bucket, key)
            get_bucket_policy(bucket)
            time.sleep(1)
            delete_object(bucket, key)


if __name__ == "__main__":
    main()
