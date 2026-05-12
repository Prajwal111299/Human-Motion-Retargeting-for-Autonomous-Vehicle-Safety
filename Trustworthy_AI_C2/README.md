# Challenge 2: Adversarial Patches for Object Detection

## 📋 Overview

This repository contains all the tools, scripts, and guides needed to complete Challenge 2, which involves:
1. Testing object detection models (Faster R-CNN, YOLOv5) on CARLA simulator
2. Creating adversarial patches to fool these models
3. Analyzing geometric transformation impacts

## 📁 Files in This Repository

### Setup Guides
- **`QUICK_START.md`** - Fast-track setup guide (recommended to start here!)
- **`SETUP_GUIDE.md`** - Detailed step-by-step setup instructions
- **`aws_setup_commands.sh`** - Bash script with all setup commands
- **`carla_bashrc_config.txt`** - CARLA environment configuration

### Implementation Files
- **`get_pr_ap_implementation.py`** - Average Precision function from Challenge 1
- **`patch_generator.py`** - Generate adversarial patches (Exercise 2)
- **`geometric_transformation_tester.py`** - Test patch transformations (Exercise 3)
- **`results_analyzer.py`** - Analyze and visualize results
- **`run_experiments.sh`** - Script to run all experiments

### Reference
- **`challenge.txt`** - Original challenge description
- **`24784_2025_C-2.pdf`** - Challenge PDF
- **`jkp2_CMU_24784_S2023_C1_Students-1.ipynb`** - Challenge 1 code (AP implementation)

## 🚀 Quick Start (30 seconds to understand)

```
1. Launch AWS g5.xlarge with Ubuntu 22.04 ✓ (You said quota is done)
2. Install: NVIDIA driver → Ubuntu Desktop → TurboVNC
3. Install: Miniconda → CARLA → SafeBench
4. Code: Implement get_pr_ap function
5. Run: Exercise 1 (6 experiments), Exercise 2 (custom patches), Exercise 3 (transformations)
6. Report: Create tables, plots, and videos
```

**Time Required:** 10-15 hours total
**Cost:** ~$15-20 (AWS g5.xlarge @ ~$1/hour)

## 📖 Detailed Instructions

### Phase 1: AWS Setup (1-2 hours)

Follow **`QUICK_START.md`** for the fastest path, or **`SETUP_GUIDE.md`** for detailed instructions.

**Key steps:**
1. Launch EC2 instance
2. Install NVIDIA driver + reboot
3. Install Ubuntu Desktop + TurboVNC
4. Install Miniconda
5. Setup CARLA
6. Clone and install SafeBench

### Phase 2: Implementation (10 minutes)

**Implement get_pr_ap function:**
- File: `~/SafeBench/safebench/util/metric_util.py`
- Use code from: `get_pr_ap_implementation.py`
- This enables AP@[0.5:0.05:0.95] metric calculation

### Phase 3: Exercise 1 - Model Comparison (3-4 hours)

**Goal:** Compare 2 models across 3 textures

**Models:**
- Faster R-CNN
- YOLOv5

**Textures:**
- stopsign.jpg
- stopsign_1.jpg
- stopsign_2.jpg

**Commands:**
```bash
# Start CARLA (Terminal 1)
cd ~/carla
./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000

# Run experiments (Terminal 2)
cd ~/SafeBench
conda activate safebench

python scripts/run.py --mode=eval --agent_cfg faster_rcnn.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4

python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4
```

**Deliverable:** Table with mAP ± std for each model-texture combination

### Phase 4: Exercise 2 - Custom Patches (2-3 hours)

**Goal:** Create adversarial patch that achieves:
- Faster R-CNN: mAP < 0.5
- YOLOv5: mAP < 0.8

**Steps:**
1. Generate patches using `patch_generator.py`
2. Test patches with SafeBench
3. Iterate until targets achieved
4. Record videos with `--save_video` flag

**Patch constraints:**
- Size: < 200×200 pixels
- Position: Center of stop sign ≈ (310, 310) in 512×512 texture

**Deliverable:** 
- Table with results
- 2 videos (different patches)
- Description of patch design

### Phase 5: Exercise 3 - Geometric Transformations (2-3 hours)

**Goal:** Test at least 2 transformation types:
- Size variations
- Position variations  
- Rotation variations

**Steps:**
1. Use `geometric_transformation_tester.py` to generate variations
2. Test each variation with SafeBench
3. Create plots showing AP vs. transformation parameter

**Deliverable:**
- 4 plots (2 transformations × 2 models)
- Videos showing transformations
- Analysis of impact

### Phase 6: Report Writing (2-3 hours)

**Report structure:**

**Exercise 1:**
- Table: 6 rows (2 models × 3 textures)
- Analysis of model differences

**Exercise 2:**
- Table with custom patch results
- Patch design explanation
- Link to 2 videos

**Exercise 3:**
- Plots (e.g., AP vs size, AP vs rotation)
- Optional: Position heatmap
- Link to transformation videos
- Analysis

**Videos:** Upload all videos to Google Drive, share link in report

## 🛠️ Helper Scripts Usage

### Generate Patches
```bash
python patch_generator.py
```
Creates 6 different patch types:
- Random noise
- Checkerboard
- Gradient
- Text patches
- Edge patterns

### Test Geometric Transformations
```bash
python geometric_transformation_tester.py
```
Generates variations for:
- 7 different sizes
- 25 different positions (5×5 grid)
- 13 different rotations

### Analyze Results
```bash
python results_analyzer.py
```
Creates:
- Table templates for exercises
- Example plots
- Visualization helpers

## 📊 Expected Results Format

### Exercise 1 Table
| Model | Texture | mAP | Std |
|-------|---------|-----|-----|
| Faster R-CNN | stopsign.jpg | 0.XX | 0.XX |
| Faster R-CNN | stopsign_1.jpg | 0.XX | 0.XX |
| Faster R-CNN | stopsign_2.jpg | 0.XX | 0.XX |
| YOLOv5 | stopsign.jpg | 0.XX | 0.XX |
| YOLOv5 | stopsign_1.jpg | 0.XX | 0.XX |
| YOLOv5 | stopsign_2.jpg | 0.XX | 0.XX |

### Exercise 2 Table
| Model | Custom Patch mAP | Target | Success |
|-------|-----------------|--------|---------|
| Faster R-CNN | 0.XX | < 0.5 | ✓/✗ |
| YOLOv5 | 0.XX | < 0.8 | ✓/✗ |

### Exercise 3 Plots
- Line plots: AP vs. transformation parameter
- Heatmaps: Position grid impact

## ⚠️ Important Notes

### Cost Management
- **STOP** (not terminate) instance when not using
- Set AWS billing alerts
- Expected cost: $15-20 for entire challenge

### Time Management
- Each experiment run: ~20-30 minutes
- Total experiments: 6 (Ex1) + iterations (Ex2) + variations (Ex3)
- Plan for 10-15 hours total

### Common Issues

**CARLA won't start:**
```bash
# Verify GPU
nvidia-smi

# Try in VNC GUI terminal
cd ~/carla
./CarlaUE4.sh -prefernvidia -carla-port=2000
```

**ImportError:**
```bash
# Check environment
conda activate safebench
echo $PYTHONPATH  # Should include CARLA paths

# Reinstall SafeBench
cd ~/SafeBench
pip install -e . --force-reinstall
```

**VNC connection fails:**
```bash
# Restart VNC server
vncserver -kill :1
vncserver

# Check AWS security group allows port 5901
```

## 📚 Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    Challenge 2 Workflow                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Setup AWS (1-2 hrs)                                     │
│     ├─ Launch instance                                      │
│     ├─ Install NVIDIA driver                                │
│     ├─ Install Ubuntu Desktop + VNC                         │
│     ├─ Install Miniconda                                    │
│     ├─ Setup CARLA                                          │
│     └─ Clone SafeBench                                      │
│                                                              │
│  2. Implement get_pr_ap (10 min)                            │
│     └─ Edit metric_util.py                                  │
│                                                              │
│  3. Exercise 1: Compare Models (3-4 hrs)                    │
│     ├─ Run Faster R-CNN (3 textures)                        │
│     └─ Run YOLOv5 (3 textures)                              │
│                                                              │
│  4. Exercise 2: Custom Patches (2-3 hrs)                    │
│     ├─ Generate patches                                     │
│     ├─ Test & iterate                                       │
│     └─ Record videos                                        │
│                                                              │
│  5. Exercise 3: Transformations (2-3 hrs)                   │
│     ├─ Generate variations                                  │
│     ├─ Test each variation                                  │
│     └─ Create plots                                         │
│                                                              │
│  6. Create Report (2-3 hrs)                                 │
│     ├─ Tables for all exercises                             │
│     ├─ Plots and analysis                                   │
│     └─ Upload videos to Google Drive                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Success Criteria

- ✅ All setup steps completed
- ✅ Exercise 1: 6 experiments completed with results
- ✅ Exercise 2: Custom patch achieves target mAP
- ✅ Exercise 2: 2 videos recorded
- ✅ Exercise 3: 2+ transformation types tested
- ✅ Exercise 3: Videos recorded
- ✅ Report includes all required tables, plots, and analysis
- ✅ All videos uploaded to Google Drive with link in report

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section in `SETUP_GUIDE.md`
2. Review SafeBench documentation: https://github.com/trust-ai/SafeBench/tree/24784_s23
3. Check CARLA 0.9.13 docs: https://carla.readthedocs.io/en/0.9.13/

## 📝 License

This is course material for CMU 24-784: Trustworthy AI and Autonomy.

---

**Ready to start? Open `QUICK_START.md` and let's go! 🚀**

