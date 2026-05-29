#!/bin/bash
# =============================================================================
# Ubuntu EC2 UserData — Cloud-Init Bootstrap Script
# =============================================================================
# Usage:
#   Paste into AWS EC2 "User data" field (Launch Instance → Advanced Details)
#   or supply via AWS CLI:
#     aws ec2 run-instances --user-data file://IAS/ubuntu-userdata.sh ...
#
# Runs once as root on first boot. Logs to /var/log/cloud-init-output.log
# Tested on Ubuntu 22.04 LTS — adapt package names for 20.04/24.04
# =============================================================================

set -euo pipefail

APP_USER="appuser"
APP_DIR="/opt/app"
LOG_DIR="/var/log/app"
HOSTNAME_PREFIX="app-node"

# ── System update ────────────────────────────────────────────────────────────
echo ">>> Updating system packages..."
apt-get update -y
apt-get upgrade -y
apt-get install -y \
    curl wget git unzip jq htop vim \
    awscli python3 python3-pip python3-venv \
    ca-certificates gnupg lsb-release

# ── Set hostname ─────────────────────────────────────────────────────────────
INSTANCE_ID=$(curl -sf http://169.254.169.254/latest/meta-data/instance-id || echo "local")
hostnamectl set-hostname "${HOSTNAME_PREFIX}-${INSTANCE_ID}"
echo "127.0.0.1  ${HOSTNAME_PREFIX}-${INSTANCE_ID}" >> /etc/hosts

# ── Create app user ──────────────────────────────────────────────────────────
if ! id "${APP_USER}" &>/dev/null; then
    useradd -m -s /bin/bash "${APP_USER}"
    echo "${APP_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/${APP_USER}
    chmod 0440 /etc/sudoers.d/${APP_USER}
fi

mkdir -p "${APP_DIR}" "${LOG_DIR}"
chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}" "${LOG_DIR}"

# ── Install Docker ───────────────────────────────────────────────────────────
echo ">>> Installing Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable docker && systemctl start docker
usermod -aG docker "${APP_USER}"

# ── Install CloudWatch agent ─────────────────────────────────────────────────
echo ">>> Installing CloudWatch agent..."
wget -q https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb \
    -O /tmp/amazon-cloudwatch-agent.deb
dpkg -i /tmp/amazon-cloudwatch-agent.deb
rm /tmp/amazon-cloudwatch-agent.deb

cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'EOF'
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          { "file_path": "/var/log/syslog",    "log_group_name": "/ec2/syslog", "log_stream_name": "{instance_id}/syslog" },
          { "file_path": "/var/log/app/*.log", "log_group_name": "/ec2/app",    "log_stream_name": "{instance_id}/app"    }
        ]
      }
    }
  }
}
EOF
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config -m ec2 -s \
    -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json

# ── sysctl hardening ─────────────────────────────────────────────────────────
echo ">>> Applying sysctl hardening..."
cat >> /etc/sysctl.d/99-hardening.conf << 'EOF'
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
EOF
sysctl -p /etc/sysctl.d/99-hardening.conf

# ── Unattended security upgrades ─────────────────────────────────────────────
apt-get install -y unattended-upgrades
dpkg-reconfigure -f noninteractive unattended-upgrades

# ── SSM Parameter Store (example — requires ssm:GetParameter IAM permission) ─
# DB_PASSWORD=$(aws ssm get-parameter \
#     --name "/myapp/prod/db-password" --with-decryption \
#     --query "Parameter.Value" --output text --region us-east-1)
# echo "DB_PASSWORD=${DB_PASSWORD}" > /etc/app.env && chmod 600 /etc/app.env

# ── CloudFormation signal (if launched via CFN stack) ────────────────────────
# /opt/aws/bin/cfn-signal -e $? \
#     --stack "${AWS_STACK_NAME}" --resource AutoScalingGroup --region "${AWS_REGION}"

echo ">>> Bootstrap complete: $(date)"
echo ">>> Instance: $(curl -sf http://169.254.169.254/latest/meta-data/instance-id)"
