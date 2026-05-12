# AWS CLI Terminal-Based Setup

## Complete terminal-based workflow for Challenge 2 using AWS CLI

---

## Step 1: Install and Configure AWS CLI

### Install AWS CLI (if not already installed)

**macOS:**
```bash
# Using Homebrew
brew install awscli

# Or using official installer
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

**Verify installation:**
```bash
aws --version
# Should show: aws-cli/2.x.x ...
```

---

## Step 2: Configure AWS Credentials

```bash
aws configure
```

**You'll be prompted for:**
- **AWS Access Key ID**: [Get from AWS Console → Security Credentials]
- **AWS Secret Access Key**: [Get from AWS Console → Security Credentials]
- **Default region name**: `us-east-1` (North Virginia - where your quota is approved)
- **Default output format**: `json`

**Test configuration:**
```bash
aws sts get-caller-identity
# Should show your account info
```

---

## Step 3: Create EC2 Key Pair

```bash
# Create key pair and save it locally
aws ec2 create-key-pair \
  --key-name challenge2-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/challenge2-key.pem

# Set correct permissions
chmod 400 ~/.ssh/challenge2-key.pem

# Verify
ls -la ~/.ssh/challenge2-key.pem
```

---

## Step 4: Launch EC2 Instance

### Find Ubuntu 22.04 AMI ID for us-east-1
```bash
# Ubuntu 22.04 LTS AMI (us-east-1)
AMI_ID="ami-0866a3c8686eaeeba"  # Ubuntu 22.04 LTS (x86_64)
```

### Launch g5.xlarge instance
```bash
aws ec2 run-instances \
  --image-id ami-0866a3c8686eaeeba \
  --instance-type g5.xlarge \
  --key-name challenge2-key \
  --security-group-ids default \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":100,"VolumeType":"gp3"}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Challenge2-SafeBench}]' \
  --region us-east-1
```

**Save the Instance ID from output:**
```bash
# Look for "InstanceId": "i-xxxxxxxxxxxxx"
INSTANCE_ID="i-0fd9b0d0298403054"  # Replace with your actual ID
```

---

## Step 5: Configure Security Group for VNC

```bash
# Get your public IP
MY_IP=$(curl -s ifconfig.me)
echo "Your IP: $MY_IP"

# Get the security group ID
SG_ID=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
  --output text)

echo "Security Group: $SG_ID"

# Allow SSH (port 22)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 22 \
  --cidr ${MY_IP}/32

# Allow VNC (port 5901)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 5901 \
  --cidr ${MY_IP}/32

# Allow VNC (port 5902 - backup)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 5902 \
  --cidr ${MY_IP}/32
```

---

## Step 6: Get Instance IP and Connect

### Get public IP
```bash
INSTANCE_IP=3.92.183.11

echo "Instance IP: $INSTANCE_IP"
```

### SSH into instance
```bash
ssh -i ~/.ssh/challenge2-key.pem ubuntu@$INSTANCE_IP
```

---

## Useful AWS CLI Commands

### Check instance status
```bash
aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].State.Name' \
  --output text
```

### Start instance
```bash
aws ec2 start-instances --instance-ids $INSTANCE_ID

# Wait for it to be running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID
echo "Instance is running!"

# Get NEW IP address (it changes after stop/start)
INSTANCE_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)
echo "New IP: $INSTANCE_IP"
```

### Stop instance (SAVE MONEY!)
```bash
aws ec2 stop-instances --instance-ids $INSTANCE_ID

# Wait for it to stop
aws ec2 wait instance-stopped --instance-ids $INSTANCE_ID
echo "Instance stopped!"
```

### Terminate instance (when completely done)
```bash
aws ec2 terminate-instances --instance-ids $INSTANCE_ID
```

### Monitor instance
```bash
# Get detailed info
aws ec2 describe-instances --instance-ids $INSTANCE_ID

# Get just the state
aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].[InstanceId,State.Name,PublicIpAddress]' \
  --output table
```

---

## Complete Setup Script

Save this as `setup_instance.sh`:

```bash
#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}Challenge 2 - AWS CLI Setup${NC}"
echo -e "${GREEN}==================================${NC}"

# Set your instance ID here
INSTANCE_ID="i-xxxxxxxxxxxxx"  # REPLACE THIS!

if [ "$INSTANCE_ID" = "i-xxxxxxxxxxxxx" ]; then
    echo -e "${RED}ERROR: Please set your INSTANCE_ID in this script!${NC}"
    exit 1
fi

# Get instance IP
echo -e "\n${YELLOW}Getting instance IP...${NC}"
INSTANCE_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

if [ -z "$INSTANCE_IP" ] || [ "$INSTANCE_IP" = "None" ]; then
    echo -e "${YELLOW}Instance not running. Starting instance...${NC}"
    aws ec2 start-instances --instance-ids $INSTANCE_ID
    aws ec2 wait instance-running --instance-ids $INSTANCE_ID
    
    INSTANCE_IP=$(aws ec2 describe-instances \
      --instance-ids $INSTANCE_ID \
      --query 'Reservations[0].Instances[0].PublicIpAddress' \
      --output text)
fi

echo -e "${GREEN}Instance IP: $INSTANCE_IP${NC}"
echo -e "\n${YELLOW}Connecting via SSH...${NC}"
ssh -i ~/.ssh/challenge2-key.pem ubuntu@$INSTANCE_IP
```

Make it executable:
```bash
chmod +x setup_instance.sh
```

---

## Quick Reference Sheet

Save these variables for easy access:

```bash
# Add to your ~/.zshrc or ~/.bashrc
export C2_INSTANCE_ID="i-xxxxxxxxxxxxx"  # Your instance ID
export C2_KEY="$HOME/.ssh/challenge2-key.pem"
export C2_REGION="us-east-1"

# Helpful aliases
alias c2-start='aws ec2 start-instances --instance-ids $C2_INSTANCE_ID'
alias c2-stop='aws ec2 stop-instances --instance-ids $C2_INSTANCE_ID'
alias c2-status='aws ec2 describe-instances --instance-ids $C2_INSTANCE_ID --query "Reservations[0].Instances[0].State.Name" --output text'
alias c2-ip='aws ec2 describe-instances --instance-ids $C2_INSTANCE_ID --query "Reservations[0].Instances[0].PublicIpAddress" --output text'
alias c2-ssh='ssh -i $C2_KEY ubuntu@$(c2-ip)'
```

Then you can simply:
```bash
c2-start          # Start instance
c2-status         # Check status
c2-ssh            # SSH into instance
c2-stop           # Stop instance
```

---

## Complete Workflow Example

```bash
# 1. Create key pair (one time)
aws ec2 create-key-pair --key-name challenge2-key \
  --query 'KeyMaterial' --output text > ~/.ssh/challenge2-key.pem
chmod 400 ~/.ssh/challenge2-key.pem

# 2. Launch instance (one time)
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id ami-0866a3c8686eaeeba \
  --instance-type g5.xlarge \
  --key-name challenge2-key \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":100}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=C2-SafeBench}]' \
  --query 'Instances[0].InstanceId' \
  --output text)

echo "Instance ID: $INSTANCE_ID"
# SAVE THIS ID!

# 3. Wait for instance to be running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# 4. Get IP address
INSTANCE_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "IP: $INSTANCE_IP"

# 5. Connect
ssh -i ~/.ssh/challenge2-key.pem ubuntu@$INSTANCE_IP

# 6. When done for the day - STOP instance
aws ec2 stop-instances --instance-ids $INSTANCE_ID
```

---

## File Transfer from Terminal

### Upload files to AWS
```bash
# Upload single file
scp -i ~/.ssh/challenge2-key.pem file.txt ubuntu@$INSTANCE_IP:~/

# Upload directory
scp -i ~/.ssh/challenge2-key.pem -r my_directory ubuntu@$INSTANCE_IP:~/

# Upload CARLA (when you download it)
scp -i ~/.ssh/challenge2-key.pem ~/Downloads/CARLA_0.9.13.tar.gz ubuntu@$INSTANCE_IP:~/
```

### Download results from AWS
```bash
# Download SafeBench logs
scp -i ~/.ssh/challenge2-key.pem -r ubuntu@$INSTANCE_IP:~/SafeBench/log ./challenge2_results/

# Download videos
scp -i ~/.ssh/challenge2-key.pem -r ubuntu@$INSTANCE_IP:~/SafeBench/log/video ./videos/
```

---

## Cost Monitoring from Terminal

```bash
# Get current month's EC2 costs (requires AWS Cost Explorer API enabled)
aws ce get-cost-and-usage \
  --time-period Start=$(date -u -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --filter file://filter.json

# Or check billing (simpler)
aws ce get-cost-forecast \
  --time-period Start=$(date -u +%Y-%m-%d),End=$(date -u -d "+7 days" +%Y-%m-%d) \
  --metric BLENDED_COST \
  --granularity DAILY
```

---

## Troubleshooting

### Can't connect via SSH
```bash
# Check instance is running
aws ec2 describe-instance-status --instance-ids $INSTANCE_ID

# Check security group allows your IP
aws ec2 describe-security-groups \
  --group-ids $SG_ID \
  --query 'SecurityGroups[0].IpPermissions'

# Get system log
aws ec2 get-console-output --instance-ids $INSTANCE_ID --output text
```

### Lost your instance ID
```bash
# List all your instances
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' \
  --output table
```

### Instance IP changed after restart
```bash
# Always get fresh IP after start/stop
INSTANCE_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)
```

---

## Next Steps

After launching and connecting to your instance:
1. Follow the setup commands in `QUICK_START.md` Steps 2-6
2. Or follow `aws_remote_setup.sh` (I'll create this next)

---

You're ready to work entirely from the terminal! 🚀

