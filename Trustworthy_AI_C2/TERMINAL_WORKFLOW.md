# Terminal-Only Workflow for Challenge 2

Complete guide for working entirely from your terminal using AWS CLI.

---

## 🚀 Quick Start (Terminal Edition)

### 1. Configure AWS CLI (One Time)

```bash
# Install AWS CLI (if needed)
brew install awscli  # macOS

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key
# Region: us-east-1
# Format: json

# Test
aws sts get-caller-identity
```

### 2. Create Key Pair (One Time)

```bash
# Create and save key
aws ec2 create-key-pair \
  --key-name challenge2-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/challenge2-key.pem

chmod 400 ~/.ssh/challenge2-key.pem
```

### 3. Launch Instance (One Time)

```bash
# Launch g5.xlarge
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
```

### 4. Wait and Connect

```bash
# Wait for instance to start
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get IP
INSTANCE_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "IP: $INSTANCE_IP"

# Connect
ssh -i ~/.ssh/challenge2-key.pem ubuntu@$INSTANCE_IP
```

---

## 📦 Setup on AWS Instance

### Option 1: Automated Setup (Recommended)

```bash
# On AWS instance - download and run setup script
wget https://raw.githubusercontent.com/your-repo/aws_remote_setup.sh
chmod +x aws_remote_setup.sh
./aws_remote_setup.sh
```

### Option 2: Manual Setup

**1. Install NVIDIA Driver**
```bash
sudo apt-get update
sudo apt-get install -y nvidia-driver-525
```

**⚠️ IMPORTANT: Stop and start instance**
```bash
# On your LOCAL terminal (not on AWS)
aws ec2 stop-instances --instance-ids $INSTANCE_ID
aws ec2 wait instance-stopped --instance-ids $INSTANCE_ID
aws ec2 start-instances --instance-ids $INSTANCE_ID
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get NEW IP
INSTANCE_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

# Reconnect
ssh -i ~/.ssh/challenge2-key.pem ubuntu@$INSTANCE_IP

# Verify GPU
nvidia-smi
```

**2. Install Ubuntu Desktop + TurboVNC**
```bash
sudo apt-get install -y ubuntu-desktop
wget https://sourceforge.net/projects/turbovnc/files/3.0.3/turbovnc_3.0.3_amd64.deb/download
sudo dpkg -i download
vncserver  # Set password
```

**3. Install Miniconda**
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
```

**4. Setup CARLA**
```bash
# On LOCAL machine - download CARLA from Google Drive first
# Then upload to AWS:
scp -i ~/.ssh/challenge2-key.pem ~/Downloads/CARLA_0.9.13.tar.gz ubuntu@$INSTANCE_IP:~/

# Back on AWS instance:
mkdir ~/carla
tar -xzvf CARLA_0.9.13.tar.gz -C ~/carla/

# Add to ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# CARLA Configuration
export CARLA_ROOT=$HOME/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
EOF

source ~/.bashrc
```

**5. Install SafeBench**
```bash
conda create -n safebench python=3.8 -y
conda activate safebench
git clone --branch 24784_s23 https://github.com/trust-ai/SafeBench.git
cd SafeBench
pip install -r requirements.txt
pip install -e .
```

---

## 💻 Implement get_pr_ap Function

### Upload implementation file
```bash
# From LOCAL terminal
scp -i ~/.ssh/challenge2-key.pem \
  ~/Desktop/Fall\ 25/24784/C2/get_pr_ap_implementation.py \
  ubuntu@35.170.203.73:~/
```

### Edit metric_util.py
```bash
# On AWS instance
vim ~/SafeBench/safebench/util/metric_util.py

# Find get_pr_ap function (around line 177)
# Replace with code from get_pr_ap_implementation.py
```

**Or use sed to add it programmatically:**
```bash
# Coming soon - automated insertion
```

---

## 🧪 Run Experiments

### Start CARLA (Terminal 1)
```bash
# Use tmux for persistent sessions
tmux new -s carla
cd ~/carla
./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000

# Detach: Ctrl+B, then D
```

### Run Experiments (Terminal 2)
```bash
conda activate safebench
cd ~/SafeBench

# Exercise 1 - Experiment 1
python scripts/run.py --mode=eval --agent_cfg faster_rcnn.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4

# Exercise 1 - Experiment 2
python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 --save_video
```

### Reattach to CARLA session
```bash
tmux attach -t carla
```

---

## 📊 Transfer Results

### Download results to local machine
```bash
# From LOCAL terminal
scp -i ~/.ssh/challenge2-key.pem -r \
  ubuntu@$INSTANCE_IP:~/SafeBench/log \
  ~/Desktop/Fall\ 25/24784/C2/results/

# Download videos
scp -i ~/.ssh/challenge2-key.pem -r \
  ubuntu@$INSTANCE_IP:~/SafeBench/log/video \
  ~/Desktop/Fall\ 25/24784/C2/videos/
```

### Upload patches to AWS
```bash
# Generate patches locally first
cd ~/Desktop/Fall\ 25/24784/C2
python3 patch_generator.py

# Upload to AWS
scp -i ~/.ssh/challenge2-key.pem \
  stopsign_with_*.jpg \
  ubuntu@$INSTANCE_IP:~/SafeBench/safebench/scenario/scenario_data/template_od/
```

---

## 🛠️ Useful Terminal Aliases

Add to your `~/.zshrc`:

```bash
# Challenge 2 AWS Shortcuts
export C2_INSTANCE_ID="i-xxxxxxxxxxxxx"  # YOUR INSTANCE ID
export C2_KEY="$HOME/.ssh/challenge2-key.pem"
export C2_REGION="us-east-1"

# Instance management
alias c2-start='aws ec2 start-instances --instance-ids $C2_INSTANCE_ID && echo "Starting..." && aws ec2 wait instance-running --instance-ids $C2_INSTANCE_ID && echo "Running!"'
alias c2-stop='aws ec2 stop-instances --instance-ids $C2_INSTANCE_ID && echo "Stopping..."'
alias c2-status='aws ec2 describe-instances --instance-ids $C2_INSTANCE_ID --query "Reservations[0].Instances[0].[State.Name,PublicIpAddress]" --output table'
alias c2-ip='aws ec2 describe-instances --instance-ids $C2_INSTANCE_ID --query "Reservations[0].Instances[0].PublicIpAddress" --output text'

# SSH connection
alias c2-ssh='ssh -i $C2_KEY ubuntu@$(c2-ip)'

# File transfer
c2-upload() {
    scp -i $C2_KEY -r "$1" ubuntu@$(c2-ip):~/
}
c2-download() {
    scp -i $C2_KEY -r ubuntu@$(c2-ip):~/"$1" .
}

# Quick commands
alias c2-logs='c2-download SafeBench/log'
alias c2-videos='c2-download SafeBench/log/video'
```

Then reload:
```bash
source ~/.zshrc
```

Now you can:
```bash
c2-start              # Start instance
c2-status             # Check status and IP
c2-ssh                # Connect via SSH
c2-upload file.txt    # Upload file
c2-logs               # Download all logs
c2-stop               # Stop instance
```

---

## 📝 Daily Workflow

### Morning (Start Work)
```bash
# 1. Start instance
c2-start

# 2. Connect
c2-ssh

# 3. Start CARLA (in tmux)
tmux new -s carla
cd ~/carla
./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000
# Detach: Ctrl+B, D

# 4. Run experiments (new terminal)
conda activate safebench
cd ~/SafeBench
# ... run experiments ...
```

### Evening (Stop Work)
```bash
# 1. Download results
c2-logs
c2-videos

# 2. Exit SSH
exit

# 3. Stop instance (FROM LOCAL TERMINAL!)
c2-stop
```

---

## 🎨 Exercise 2: Custom Patches

### Local workflow
```bash
# 1. Generate patches locally
cd ~/Desktop/Fall\ 25/24784/C2
python3 patch_generator.py

# 2. Upload to AWS
c2-upload "stopsign_with_*.jpg"

# 3. On AWS: move to correct location
c2-ssh
mv stopsign_with_*.jpg ~/SafeBench/safebench/scenario/scenario_data/template_od/
```

---

## 📐 Exercise 3: Transformations

```bash
# 1. Generate transformations locally
python3 geometric_transformation_tester.py

# 2. Upload variations
c2-upload size_variations
c2-upload rotation_variations

# 3. On AWS: move to correct location
c2-ssh
mv size_variations ~/SafeBench/safebench/scenario/scenario_data/template_od/
```

---

## 💰 Cost Monitoring

```bash
# Check instance is stopped
c2-status

# List all running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name]' \
  --output table
```

---

## 🔥 Complete Terminal Script

Save as `challenge2.sh`:

```bash
#!/bin/bash

# Challenge 2 Terminal Manager
INSTANCE_ID="i-xxxxxxxxxxxxx"  # SET THIS
KEY="$HOME/.ssh/challenge2-key.pem"

get_ip() {
    aws ec2 describe-instances \
      --instance-ids $INSTANCE_ID \
      --query 'Reservations[0].Instances[0].PublicIpAddress' \
      --output text
}

case "$1" in
    start)
        aws ec2 start-instances --instance-ids $INSTANCE_ID
        aws ec2 wait instance-running --instance-ids $INSTANCE_ID
        echo "Instance running at: $(get_ip)"
        ;;
    stop)
        aws ec2 stop-instances --instance-ids $INSTANCE_ID
        echo "Instance stopping..."
        ;;
    connect)
        ssh -i $KEY ubuntu@$(get_ip)
        ;;
    upload)
        scp -i $KEY -r "$2" ubuntu@$(get_ip):~/
        ;;
    download)
        scp -i $KEY -r ubuntu@$(get_ip):~/"$2" .
        ;;
    status)
        aws ec2 describe-instances \
          --instance-ids $INSTANCE_ID \
          --query 'Reservations[0].Instances[0].[State.Name,PublicIpAddress]' \
          --output table
        ;;
    *)
        echo "Usage: $0 {start|stop|connect|upload|download|status}"
        exit 1
esac
```

Usage:
```bash
chmod +x challenge2.sh
./challenge2.sh start
./challenge2.sh connect
./challenge2.sh stop
```

---

## 🎯 Summary

**Setup (one time):**
1. `aws configure`
2. Create key pair
3. Launch instance
4. Run setup script on instance

**Daily workflow:**
1. `c2-start` - Start instance
2. `c2-ssh` - Connect
3. Work on experiments
4. `c2-logs` - Download results
5. `c2-stop` - Stop instance

**File transfer:**
- Upload: `c2-upload file`
- Download: `c2-download path/to/file`

You're ready to work entirely from terminal! 🚀

