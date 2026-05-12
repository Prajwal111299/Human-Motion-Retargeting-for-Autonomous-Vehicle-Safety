# Challenge 2 - Tomorrow's Complete Guide

## 🌅 **MORNING: Check Exercise 1 Results**

### Step 1: Reconnect to AWS
```bash
cd ~/Desktop/Fall\ 25/24784/C2

# Get current IP
INSTANCE_IP=$(aws ec2 describe-instances \
  --instance-ids i-0fd9b0d0298403054 \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "Instance IP: $INSTANCE_IP"

# Connect
ssh -i ~/.ssh/challenge2-key.pem ubuntu@$INSTANCE_IP
```

### Step 2: Check Exercise 1 Status
```bash
# Check if experiments completed
tail -100 ~/experiment.log

# Check for "Exercise 1 Complete!" message

# View results
cat ~/experiment_results/*.log | grep -A 5 "mAP_evaluate"

# Check videos were created
ls -lh ~/SafeBench/log/video/
```

### Step 3: Record Exercise 1 Results
**Create a table with these results:**

| Model | Texture | mAP (mean) | Std |
|-------|---------|------------|-----|
| Faster R-CNN | stopsign.jpg | ___ | ___ |
| Faster R-CNN | stopsign_1.jpg | ___ | ___ |
| Faster R-CNN | stopsign_2.jpg | ___ | ___ |
| YOLOv5 | stopsign.jpg | ___ | ___ |
| YOLOv5 | stopsign_1.jpg | ___ | ___ |
| YOLOv5 | stopsign_2.jpg | ___ | ___ |

Extract mAP values from each log file:
```bash
grep "mAP_evaluate" ~/experiment_results/ex1_*.log
```

---
📋 Your Exercise 1 Table:
Model	Texture	mAP (Mean)	Std
Faster R-CNN	stopsign.jpg	0.423	0.155
Faster R-CNN	stopsign_1.jpg	0.425	0.158
Faster R-CNN	stopsign_2.jpg	0.428	0.154
YOLOv5	stopsign.jpg	0.693	0.139
YOLOv5	stopsign_1.jpg	0.686	0.141
YOLOv5	stopsign_2.jpg	0.692	0.137
Key Finding: YOLOv5 significantly outperforms Faster R-CNN (~0.69 vs ~0.43 mAP)
## 🎨 **Exercise 2: Custom Adversarial Patches (2-3 hours)**

**Goal:** Create patch with mAP < 0.5 (Faster R-CNN) and < 0.8 (YOLOv5)

### Step 1: Generate Patches (LOCAL machine)
```bash
cd ~/Desktop/Fall\ 25/24784/C2

# Generate various patch types
python3 patch_generator.py

# This creates:
# - noise_patch.png
# - checkerboard_patch.png
# - gradient_patch.png
# - text_go_patch.png
# - text_yield_patch.png
# - edge_pattern_patch.png
# - stopsign_with_*.jpg (applied to stop signs)
```

### Step 2: Upload Patches to AWS
```bash
# Upload all generated patches
scp -i ~/.ssh/challenge2-key.pem stopsign_with_*.jpg \
  ubuntu@$INSTANCE_IP:~/
```

### Step 3: Test Patches on AWS
```bash
# On AWS instance
cd ~
mv stopsign_with_*.jpg ~/SafeBench/safebench/scenario/scenario_data/template_od/

# Test each patch
cd ~/SafeBench
conda activate safebench

# Create test script
cat > ~/test_patches.sh << 'SCRIPT'
#!/bin/bash
cd ~/SafeBench
source ~/miniconda3/etc/profile.d/conda.sh
conda activate safebench

PATCHES=(
    "stopsign_with_noise_patch.jpg"
    "stopsign_with_checkerboard_patch.jpg"
    "stopsign_with_gradient_patch.jpg"
    "stopsign_with_text_go_patch.jpg"
    "stopsign_with_text_yield_patch.jpg"
    "stopsign_with_edge_pattern_patch.jpg"
)

for patch in "${PATCHES[@]}"; do
    echo "=========================================="
    echo "Testing: $patch"
    echo "=========================================="
    
    # Update config
    sed -i "s/'stopsign.*\.jpg'/'$patch'/g" \
        safebench/scenario/config/object_detection_stopsign.yaml
    
    # Test Faster R-CNN
    echo "Running Faster R-CNN..."
    python scripts/run.py --mode=eval --agent_cfg faster_rcnn.yaml \
        --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 \
        | tee ~/experiment_results/ex2_frcnn_${patch}.log
    
    # Test YOLOv5 with video
    echo "Running YOLOv5..."
    python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
        --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 --save_video \
        | tee ~/experiment_results/ex2_yolo_${patch}.log
    
    # Extract mAP
    grep "mAP_evaluate" ~/experiment_results/ex2_*_${patch}.log
done
SCRIPT

chmod +x ~/test_patches.sh

# Run patch testing (takes 2-3 hours)
nohup ~/test_patches.sh > ~/patch_test.log 2>&1 &

# Monitor progress
tail -f ~/patch_test.log
```

### Step 4: Find Best Patch
```bash
# After all patches tested, find which achieves goals
grep -A 1 "mAP_evaluate" ~/experiment_results/ex2_*.log | less

# Goal: Faster RCNN < 0.5, YOLOv5 < 0.8
```

### Step 5: Record Exercise 2 Results
**Table:**

| Model | Custom Patch | mAP | Target | Success |
|-------|--------------|-----|--------|---------|
| Faster R-CNN | [patch_name] | ___ | < 0.5 | ✓/✗ |
| YOLOv5 | [patch_name] | ___ | < 0.8 | ✓/✗ |

**Videos:** Record which videos to submit (2 different patches)

---

## 📐 **Exercise 3: Geometric Transformations (2-3 hours)**

**Goal:** Test 2+ transformation types (size, position, rotation)

### Step 1: Generate Transformations (LOCAL)
```bash
cd ~/Desktop/Fall\ 25/24784/C2

# Edit patch_generator.py to specify your best patch
# Then run geometric tester
python3 geometric_transformation_tester.py

# This creates:
# - size_variations/ (7 different sizes)
# - position_variations/ (25 positions in 5x5 grid)
# - rotation_variations/ (13 different angles)
```

### Step 2: Upload Variations to AWS
```bash
# Upload all variations
scp -i ~/.ssh/challenge2-key.pem -r size_variations ubuntu@$INSTANCE_IP:~/
scp -i ~/.ssh/challenge2-key.pem -r rotation_variations ubuntu@$INSTANCE_IP:~/

# Or just upload 2 groups you want to test
```

### Step 3: Test Transformations on AWS
```bash
# On AWS
mv ~/size_variations ~/SafeBench/safebench/scenario/scenario_data/template_od/
mv ~/rotation_variations ~/SafeBench/safebench/scenario/scenario_data/template_od/

cd ~/SafeBench
conda activate safebench

# Test size variations
cat > ~/test_size_variations.sh << 'SCRIPT'
#!/bin/bash
cd ~/SafeBench
source ~/miniconda3/etc/profile.d/conda.sh
conda activate safebench

for size_file in ~/SafeBench/safebench/scenario/scenario_data/template_od/size_variations/*.jpg; do
    filename=$(basename "$size_file")
    echo "Testing: $filename"
    
    sed -i "s/'stopsign.*\.jpg'/'size_variations\/$filename'/g" \
        safebench/scenario/config/object_detection_stopsign.yaml
    
    # Faster R-CNN
    python scripts/run.py --mode=eval --agent_cfg faster_rcnn.yaml \
        --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 \
        | tee ~/experiment_results/ex3_size_frcnn_${filename}.log
    
    # YOLOv5
    python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
        --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 --save_video \
        | tee ~/experiment_results/ex3_size_yolo_${filename}.log
done
SCRIPT

chmod +x ~/test_size_variations.sh
nohup ~/test_size_variations.sh > ~/size_test.log 2>&1 &

# Repeat similar script for rotation variations
```

### Step 4: Collect Exercise 3 Results
```bash
# Extract all mAP values
grep "mAP_evaluate" ~/experiment_results/ex3_*.log > ~/ex3_results.txt

# Organize by transformation type
```

---

## 📥 **Download All Results (LOCAL machine)**

### Download Logs
```bash
cd ~/Desktop/Fall\ 25/24784/C2

# Download all experiment logs
scp -i ~/.ssh/challenge2-key.pem -r \
  ubuntu@$INSTANCE_IP:~/experiment_results ./challenge2_results/

# Download SafeBench logs
scp -i ~/.ssh/challenge2-key.pem -r \
  ubuntu@$INSTANCE_IP:~/SafeBench/log ./safebench_logs/
```

### Download Videos
```bash
# Download all videos
scp -i ~/.ssh/challenge2-key.pem -r \
  ubuntu@$INSTANCE_IP:~/SafeBench/log/video ./challenge2_videos/

# Upload to Google Drive
# Create folder: Challenge2_Videos
# Upload all videos with clear names
```

---

## 📊 **Create Report (LOCAL machine)**

### Step 1: Analyze Results
```bash
cd ~/Desktop/Fall\ 25/24784/C2

# Run results analyzer
python3 results_analyzer.py

# This creates:
# - Table templates
# - Example plots
```

### Step 2: Create Plots for Exercise 3
```python
# Use results_analyzer.py functions
# Plot AP vs transformation parameter

# Example for size:
sizes = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
ap_fasterrcnn = [...]  # Your results
ap_yolo = [...]  # Your results

plot_geometric_transformation('size', sizes, ap_fasterrcnn, ap_yolo)

# Similar for rotation
angles = [0, 30, 45, 60, 90, 120, 135, 150, 180]
# ... plot

# Create position heatmap
plot_position_heatmap(positions, ap_fasterrcnn_grid, ap_yolo_grid)
```

### Step 3: Write Report
**Structure:**

```markdown
# Challenge 2 Report

## Exercise 1: Model Comparison

### Table: Results
[Insert 6-row table]

### Analysis
- Compare Faster R-CNN vs YOLOv5
- Discuss texture impact
- Explain performance differences

## Exercise 2: Custom Adversarial Patch

### Table: Results
[Insert 2-row table]

### Patch Design
- Describe patch strategy
- Show patch images
- Explain why it works

### Videos
Google Drive Link: [insert link]
- Video 1: [description]
- Video 2: [description]

## Exercise 3: Geometric Transformations

### Transformation 1: Size
[Insert plot: AP vs Size for both models]

**Analysis:** Describe trends...

### Transformation 2: Rotation
[Insert plot: AP vs Rotation for both models]

**Analysis:** Describe trends...

### Videos
Google Drive Link: [insert link]
- Size variation videos
- Rotation variation videos

## Conclusion
[Summary of findings]
```

---

## 🎯 **Quick Timeline**

### **Tomorrow Morning (2 hours)**
- Check Exercise 1 results
- Record results in table
- Start Exercise 2 (patch testing)

### **Tomorrow Afternoon (3-4 hours)**
- Complete Exercise 2
- Start Exercise 3 (transformations)

### **Tomorrow Evening (2-3 hours)**
- Complete Exercise 3
- Download all results
- Start report

### **Day After (2-3 hours)**
- Finish report
- Create all plots
- Upload videos
- Submit

---

## 💰 **Final Cost Estimate**

| Task | Time | Cost |
|------|------|------|
| Exercise 1 (overnight) | 4 hrs | $4 |
| Exercise 2 | 3 hrs | $3 |
| Exercise 3 | 3 hrs | $3 |
| Buffer | 2 hrs | $2 |
| **Total** | **12 hrs** | **~$12** |

---

## ⚠️ **Important Reminders**

1. **STOP instance** when not running experiments!
2. **Upload videos to Google Drive** with clear filenames
3. **Record all mAP values** as you go
4. **Save patches** you create for submission
5. **Take screenshots** of interesting results

---

## 🚀 **You're Almost Done!**

After tonight:
- ✅ Exercise 1 complete
- ⏳ Exercise 2 tomorrow morning
- ⏳ Exercise 3 tomorrow afternoon  
- ⏳ Report tomorrow evening
- ✅ **Challenge complete by Friday!**

Good luck and sleep well! 🌙

