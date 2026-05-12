# Challenge 2 - Quick Start Guide

## Overview
This guide provides a fast-track setup for Challenge 2. Follow these steps in order.

---

## Pre-Flight Checklist
- [ ] AWS account with g5.xlarge quota approved
- [ ] CARLA downloaded from Google Drive
- [ ] Challenge 1 code available
- [ ] This repo cloned locally

---

## Step-by-Step Instructions

### 1. Launch AWS Instance (5 minutes)

```bash
# On AWS Console:
# 1. Launch g5.xlarge with Ubuntu 22.04
# 2. Create/download key pair
# 3. Note your instance IP address

# On your local machine:
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<YOUR-IP>
```

### 2. Install NVIDIA Driver (20 minutes)

```bash
# On AWS:
sudo apt-get update
sudo apt-get install -y nvidia-driver-525

# STOP instance from AWS Console, then START again
# SSH back in with NEW IP address

nvidia-smi  # Verify GPU is detected
```

### 3. Install GUI & VNC (30 minutes)

```bash
# Install Ubuntu Desktop
sudo apt-get install -y ubuntu-desktop

# Install TurboVNC
wget https://sourceforge.net/projects/turbovnc/files/3.0.3/turbovnc_3.0.3_amd64.deb/download
sudo dpkg -i download
vncserver  # Set password when prompted

# On local machine: Install TurboVNC Viewer
# Connect to: ubuntu@<YOUR-IP>:1
```

### 4. Install Miniconda (10 minutes)

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
```

### 5. Setup CARLA (15 minutes)

```bash
# On local machine:
scp CARLA_0.9.13.tar.gz ubuntu@<YOUR-IP>:~/

# On AWS:
mkdir ~/carla
tar -xzvf CARLA_0.9.13.tar.gz -C ~/carla/

# Add to ~/.bashrc:
echo 'export CARLA_ROOT=/home/ubuntu/carla' >> ~/.bashrc
echo 'export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg' >> ~/.bashrc
echo 'export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla' >> ~/.bashrc
source ~/.bashrc

# Test CARLA (in VNC terminal):
cd ~/carla
./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000
# Press Ctrl+C to stop
```

### 6. Install SafeBench (15 minutes)

```bash
conda create -n safebench python=3.8 -y
conda activate safebench

git clone --branch 24784_s23 https://github.com/trust-ai/SafeBench.git
cd SafeBench
pip install -r requirements.txt
pip install -e .
```

### 7. Implement get_pr_ap Function (10 minutes)

```bash
# Edit the file:
vim ~/SafeBench/safebench/util/metric_util.py

# Find get_pr_ap function (around line 177)
# Replace with implementation from get_pr_ap_implementation.py
```

**Implementation:**

```python
def interp_ap(recall, precision, method='interp'):
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
    df = df.sort_values(by='conf_scores', ascending=False)
    tp_fp = np.arange(1, len(df) + 1, 1)
    tp = ((df['iou_scores'] >= iou_thres) & 
          (df['predicted_class'] == 'stopsign')).cumsum().values
    precision = tp / tp_fp
    recall = tp / num_gt
    ap = interp_ap(recall, precision)
    return ap, precision, recall
```

### 8. Run Exercise 1 (30 minutes per run)

**Terminal 1 - Start CARLA:**
```bash
conda activate safebench
cd ~/carla
./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000
```

**Terminal 2 - Run Experiments:**
```bash
conda activate safebench
cd ~/SafeBench

# Test 1: Faster R-CNN with stopsign.jpg
python scripts/run.py --mode=eval --agent_cfg faster_rcnn.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4

# Test 2: YOLOv5 with stopsign.jpg
python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4

# Repeat for stopsign_1.jpg and stopsign_2.jpg
# (Edit texture_dir in safebench/scenario/config/object_detection_stopsign.yaml)
```

### 9. Create Custom Patches (Exercise 2)

```bash
# On local machine:
python patch_generator.py

# Upload patches to AWS:
scp stopsign_with_*.jpg ubuntu@<YOUR-IP>:~/SafeBench/safebench/scenario/scenario_data/template_od/

# Test patches and iterate until:
# - Faster R-CNN: mAP < 0.5
# - YOLOv5: mAP < 0.8
```

### 10. Geometric Transformations (Exercise 3)

```bash
# On local machine:
python geometric_transformation_tester.py

# Upload variations:
scp -r size_variations ubuntu@<YOUR-IP>:~/SafeBench/safebench/scenario/scenario_data/template_od/

# Test each variation and record results
```

---

## Results Collection

```bash
# Copy results from AWS to local:
scp -r ubuntu@<YOUR-IP>:~/SafeBench/log ./challenge2_results/

# Analyze results:
python results_analyzer.py
```

---

## Report Structure

### Exercise 1
- Table: 2 models × 3 textures = 6 rows
- Columns: Model, Texture, mAP, Std
- Analysis of model differences

### Exercise 2
- Table: 2 models × 1 custom patch = 2 rows
- Show patch design
- 2 videos (YOLOv5 with different patches)
- Explain attack strategy

### Exercise 3
- 4 plots (2 transformation types × 2 models)
- Examples: size vs AP, rotation vs AP
- Videos showing different transformations
- Analysis of transformation impact

---

## Time Estimates

| Task | Time |
|------|------|
| AWS Setup | 1-2 hours |
| Exercise 1 (6 runs) | 3-4 hours |
| Exercise 2 (patch design + testing) | 2-3 hours |
| Exercise 3 (transformations) | 2-3 hours |
| Report Writing | 2-3 hours |
| **Total** | **10-15 hours** |

---

## Troubleshooting

**CARLA won't start:**
```bash
# Check GPU
nvidia-smi

# Try without offscreen rendering
./CarlaUE4.sh -prefernvidia -carla-port=2000
```

**SafeBench import errors:**
```bash
# Reinstall
cd ~/SafeBench
pip install -e . --force-reinstall
```

**Out of memory:**
```bash
# Reduce batch size or use smaller scenarios
--num_scenario 2  # instead of 4
```

---

## Cost Management

⚠️ **IMPORTANT:** g5.xlarge costs ~$1/hour

- **STOP** instance when not using (don't terminate)
- Set up billing alerts
- Budget: ~$15-20 for entire challenge

---

## Quick Commands Reference

```bash
# SSH to AWS
ssh ubuntu@<YOUR-IP>

# Activate environment
conda activate safebench

# Start CARLA
cd ~/carla && ./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000

# Run experiment
cd ~/SafeBench && python scripts/run.py --mode=eval --agent_cfg yolo.yaml --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 --save_video

# Copy results
scp -r ubuntu@<YOUR-IP>:~/SafeBench/log ./results/

# Stop instance
# Go to AWS Console → Stop Instance
```

---

Good luck! 🚀

