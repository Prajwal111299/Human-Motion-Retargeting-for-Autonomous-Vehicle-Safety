# Challenge 2 - Complete Setup and Execution Guide

## Overview
This guide will walk you through the complete Challenge 2 setup and execution.

## Prerequisites
- AWS account with approved quota for g5.xlarge instance
- Local computer with SSH access
- Internet connection

---

## PART 1: AWS Instance Setup

### Step 1: Launch EC2 Instance

1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Configure:
   - **Name**: C2-SafeBench (or your choice)
   - **OS**: Ubuntu 22.04 LTS
   - **Instance Type**: g5.xlarge
   - **Key Pair**: Create new key pair (download the .pem file and save it securely)
   - **Storage**: 100GB (recommended)
4. Launch Instance

### Step 2: Initial SSH Setup

```bash
# On your local machine
chmod 400 <your-key-name>.pem
ssh -i <your-key-name>.pem ubuntu@<your-instance-ip>
```

### Step 3: Generate SSH Key (Optional but Recommended)

```bash
# On AWS server
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
cat ~/.ssh/id_rsa.pub

# On your local machine
cat ~/.ssh/id_rsa.pub

# Copy your local public key content, then on AWS server:
vim ~/.ssh/authorized_keys
# Paste your local public key at the end
# Save and exit (:wq)

# Now you can login without .pem:
ssh ubuntu@<your-instance-ip>
```

---

## PART 2: System Setup

### Step 4: Install NVIDIA Driver

```bash
# On AWS server
sudo apt-get update
sudo apt-get install nvidia-driver-525

# IMPORTANT: After installation, STOP your instance from AWS Console
# Then START it again (IP address will change!)
# Login with new IP address

# Verify installation
nvidia-smi
# You should see GPU information
```

### Step 5: Install Ubuntu Desktop

```bash
sudo apt-get update
sudo apt-get install ubuntu-desktop

# This takes 15-30 minutes
# If any errors, try: sudo apt-get install --fix-broken ubuntu-desktop
```

### Step 6: Install TurboVNC

```bash
# On AWS server
cd ~
wget https://sourceforge.net/projects/turbovnc/files/3.0.3/turbovnc_3.0.3_amd64.deb/download
sudo dpkg -i download

# Start VNC server
vncserver
# Set a password when prompted

# On your local machine, install TurboVNC viewer:
# Mac: Download from https://sourceforge.net/projects/turbovnc/files/
# Windows: Download from same link

# Connect using TurboVNC Viewer:
# Server: ubuntu@<your-instance-ip>:1
```

---

## PART 3: Install CARLA and SafeBench

### Step 7: Install Miniconda

```bash
# On AWS server
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Press Enter and type 'yes' to agree

# Restart terminal or:
source ~/.bashrc
```

### Step 8: Download and Setup CARLA

```bash
# On your LOCAL machine:
# 1. Download CARLA from: https://drive.google.com/file/d/1A4z3RKXqVYpOmsEZkPBV1Pbw3B8aeSMp/view
# 2. Save it to Downloads folder

# Upload to AWS (from local machine):
scp ~/Downloads/CARLA_0.9.13.tar.gz ubuntu@<your-instance-ip>:~/

# On AWS server:
cd ~
mkdir carla
tar -xzvf CARLA_0.9.13.tar.gz -C carla/

# Configure CARLA environment
vim ~/.bashrc
```

Add these lines to the end of ~/.bashrc:

```bash
export CARLA_ROOT=/home/ubuntu/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
```

Save and exit, then:

```bash
source ~/.bashrc

# Test CARLA (in VNC/GUI terminal):
cd ~/carla
./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000
# You should see CARLA starting. Press Ctrl+C to stop for now.
```

### Step 9: Clone and Install SafeBench

```bash
# Create conda environment
conda create -n safebench python=3.8
conda activate safebench

# Clone repository
cd ~
git clone --branch 24784_s23 https://github.com/trust-ai/SafeBench.git
cd SafeBench

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

---

## PART 4: Implement get_pr_ap Function

### Step 10: Modify metric_util.py

```bash
# On AWS server
cd ~/SafeBench
vim safebench/util/metric_util.py
```

Find the `get_pr_ap` function (around line 177) and replace it with:

```python
def interp_ap(recall, precision, method='interp'):
    """Compute average precision using interpolation"""
    appended_recall = np.concatenate(([0.0], recall, [1.0]))
    appended_prec_input = np.concatenate(([1.0], precision, [0.0]))
    appended_prec = np.flip(np.maximum.accumulate(np.flip(appended_prec_input)))
    
    if method == 'interp':
        x = np.linspace(0, 1, 101)
        ap = np.trapz(np.interp(x, appended_recall, appended_prec), x)
    else:
        i = np.where(appended_recall[1:] != appended_recall[:-1])[0]
        ap = np.sum((appended_recall[i + 1] - appended_recall[i]) * appended_prec[i + 1])
    
    return ap

def get_pr_ap(df, num_gt, iou_thres):
    """Compute average precision for object detection"""
    df = df.sort_values(by='conf_scores', ascending=False)
    tp_fp = np.arange(1, len(df) + 1, 1)
    tp = ((df['iou_scores'] >= iou_thres) & 
          (df['predicted_class'] == 'stopsign')).cumsum().values
    precision = tp / tp_fp
    recall = tp / num_gt
    ap = interp_ap(recall, precision)
    return ap, precision, recall
```

---

## PART 5: Run Experiments

### Step 11: Start CARLA Server

```bash
# In VNC terminal or tmux session:
cd ~/carla
./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000

# Keep this running in background
```

### Step 12: Run Exercise 1

Open a new terminal:

```bash
conda activate safebench
cd ~/SafeBench

# Run with default texture (stopsign.jpg)
python scripts/run.py --mode=eval --agent_cfg faster_rcnn.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4

python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4

# Modify texture in config file:
vim safebench/scenario/config/object_detection_stopsign.yaml
# Change 'texture_dir' to 'stopsign_1.jpg'
# Run both models again

# Repeat for stopsign_2.jpg
```

### Step 13: Create Custom Patches (Exercise 2)

Use the provided `patch_generator.py` script to create patches, or create your own:

```bash
python patch_generator.py
# This generates various patch types

# Apply patches and test
# Remember: mAP < 0.5 for Faster RCNN, < 0.8 for YOLOv5
```

### Step 14: Test Geometric Transformations (Exercise 3)

Modify patch size, position, and rotation systematically and record results.

---

## PART 6: Collect Results and Create Report

### Step 15: Organize Results

- Results are stored in `log/` directory
- Videos are in `log/video/`
- Copy files to local machine:

```bash
# On local machine:
scp -r ubuntu@<instance-ip>:~/SafeBench/log ./challenge2_results/
```

### Step 16: Create Report

Include:
- Exercise 1: Table with AP@[0.5:0.05:0.95] for 2 models × 3 textures
- Exercise 2: Table with results + 2 videos
- Exercise 3: Plots/tables for geometric transformations + videos

---

## Troubleshooting

### CARLA won't start
- Check GPU with `nvidia-smi`
- Make sure you're using VNC/GUI terminal
- Try without `-RenderOffScreen` flag

### SafeBench import errors
- Make sure conda environment is activated
- Check PYTHONPATH includes CARLA

### Can't connect to VNC
- Check VNC server is running: `vncserver -list`
- Check AWS security group allows VNC ports (5901, 5902)

---

## Quick Reference Commands

```bash
# Start CARLA
cd ~/carla && ./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000

# Activate environment
conda activate safebench

# Run evaluation
cd ~/SafeBench
python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 --save_video

# Stop EC2 instance when done to save money!
```

---

## Cost Saving Tips

- **STOP instance when not using** (don't terminate, just stop)
- g5.xlarge costs ~$1/hour
- Set up billing alerts in AWS
- Delete instance when completely done with challenge

---

Good luck with Challenge 2!

