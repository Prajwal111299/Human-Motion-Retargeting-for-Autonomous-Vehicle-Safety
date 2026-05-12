# 🚀 Challenge 2 - START HERE

## What I've Prepared for You

I've analyzed your Challenge 1 code and created a complete toolkit to help you solve Challenge 2. Here's everything you need:

### 📚 Documentation (READ THESE FIRST!)
1. **`README.md`** - Complete overview of the entire challenge
2. **`QUICK_START.md`** ⭐ **START HERE** - Fastest path to completion
3. **`SETUP_GUIDE.md`** - Detailed setup instructions
4. **`CHECKLIST.md`** - Track your progress through every step

### 🔧 Setup Scripts
- **`aws_setup_commands.sh`** - All AWS setup commands in one place
- **`carla_bashrc_config.txt`** - Environment configuration for CARLA

### 💻 Implementation Code
- **`get_pr_ap_implementation.py`** - Your Challenge 1 AP code adapted for SafeBench
- **`run_experiments.sh`** - Commands to run all experiments

### 🎨 Exercise Helper Scripts
- **`patch_generator.py`** - Generate adversarial patches (Exercise 2)
- **`geometric_transformation_tester.py`** - Test transformations (Exercise 3)
- **`results_analyzer.py`** - Analyze and visualize results

### 📊 Your Challenge 1 Code
- **`jkp2_CMU_24784_S2023_C1_Students-1.ipynb`** - Your working AP implementation

---

## 🎯 What You Need to Do

### Right Now (Next 10 minutes)
1. **Read `QUICK_START.md`** - This gives you the complete roadmap
2. **Open `CHECKLIST.md`** - This is your execution tracker

### Today/Tomorrow (2-3 hours)
3. **Setup AWS Instance** - Follow QUICK_START.md Steps 1-6
   - Launch g5.xlarge
   - Install NVIDIA driver (requires reboot)
   - Install Ubuntu Desktop + TurboVNC
   - Install Miniconda
   - Setup CARLA
   - Clone SafeBench

### Implementation (10 minutes)
4. **Add get_pr_ap function** - Copy code from `get_pr_ap_implementation.py`

### Run Experiments (Rest of the week)
5. **Exercise 1** - Test 2 models × 3 textures = 6 experiments (~3-4 hours)
6. **Exercise 2** - Create adversarial patches (~2-3 hours)
7. **Exercise 3** - Test geometric transformations (~2-3 hours)
8. **Report** - Write up results (~2-3 hours)

**Total Time:** 10-15 hours
**Total Cost:** ~$15-20 (AWS)

---

## 📖 How to Use This Repository

### Step 1: Read the Guides
```
Start with QUICK_START.md (fastest)
  ↓
Use CHECKLIST.md to track progress
  ↓
Reference SETUP_GUIDE.md if you need details
  ↓
Check README.md for overall understanding
```

### Step 2: Follow the Workflow
```
AWS Setup → Implementation → Exercise 1 → Exercise 2 → Exercise 3 → Report
```

### Step 3: Use the Helper Scripts

**On AWS (during exercises):**
```bash
# Generate adversarial patches
python patch_generator.py

# Test geometric transformations
python geometric_transformation_tester.py

# Analyze results
python results_analyzer.py
```

**On Local Machine:**
You can also run the patch/transformation generators locally, then upload to AWS.

---

## 🎓 Key Information from Challenge 1

I extracted your AP calculation code from Challenge 1. Here's what I found:

### Your Implementation (Working ✅)

**`box_iou` function:** Calculates IoU between predicted and ground truth boxes
- Handles intersection and union correctly
- Uses epsilon for numerical stability

**`interp_ap` function:** Computes Average Precision
- Appends sentinel values (0.0, 1.0 for recall; 1.0, 0.0 for precision)
- Creates precision envelope
- Uses 101-point interpolation (COCO standard)

**`compute_ap` function:** Main AP calculation
- Sorts by confidence scores
- Computes cumulative TP
- Calculates precision and recall curves
- Returns AP using interpolation

### Your Challenge 1 Results
```
AP@0.5 = 0.7983
AP@0.6 = 0.7983
AP@0.7 = 0.7800
AP@0.8 = 0.7398
AP@0.9 = 0.5873
```

This code is now adapted for SafeBench in `get_pr_ap_implementation.py`!

---

## 🔥 Quick Commands Reference

### AWS Setup
```bash
# Initial connection
ssh -i your-key.pem ubuntu@<IP>

# After NVIDIA install and reboot (NEW IP!)
ssh -i your-key.pem ubuntu@<NEW-IP>
```

### Start Working
```bash
# Activate environment
conda activate safebench

# Terminal 1: Start CARLA
cd ~/carla
./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000

# Terminal 2: Run experiments
cd ~/SafeBench
python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
  --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 --save_video
```

### Copy Results Back
```bash
# From local machine
scp -r ubuntu@<IP>:~/SafeBench/log ./challenge2_results/
```

### Save Money!
```bash
# When done for the day: Go to AWS Console → STOP instance
# Don't terminate - you'll lose everything!
```

---

## ✅ Success Checklist

- [ ] AWS instance running and accessible
- [ ] CARLA and SafeBench installed
- [ ] `get_pr_ap` function implemented
- [ ] Exercise 1: 6 experiments completed
- [ ] Exercise 2: Custom patch achieves targets (mAP < 0.5 and < 0.8)
- [ ] Exercise 2: 2 videos recorded
- [ ] Exercise 3: 2+ transformation types tested
- [ ] Exercise 3: Videos recorded
- [ ] Report written with all tables and plots
- [ ] Videos uploaded to Google Drive
- [ ] Submission complete!

---

## 🆘 If You Get Stuck

### Common Issues

**CARLA won't start:**
- Check `nvidia-smi` works
- Try running in VNC GUI terminal
- Remove `-RenderOffScreen` flag

**SafeBench import errors:**
- Make sure `conda activate safebench` is run
- Check `echo $PYTHONPATH` includes CARLA
- Try `pip install -e . --force-reinstall`

**VNC won't connect:**
- Check `vncserver -list` shows server running
- Restart: `vncserver -kill :1` then `vncserver`
- Check AWS security group

### Need Help?
1. Check Troubleshooting in `SETUP_GUIDE.md`
2. Review SafeBench docs: https://github.com/trust-ai/SafeBench/tree/24784_s23
3. Check CARLA docs: https://carla.readthedocs.io/en/0.9.13/

---

## 💡 Pro Tips

1. **Use tmux/screen** for long-running processes on AWS
2. **Test with `--num_scenario 2`** first to verify everything works
3. **Save instance state** - STOP (don't terminate) when not using
4. **Generate patches locally first** - faster iteration
5. **Keep notes** - Document your AP results as you go
6. **Start early** - Some experiments take 30+ minutes

---

## 📂 File Organization Suggestion

```
C2/
├── Documentation (provided)
│   ├── README.md
│   ├── QUICK_START.md
│   ├── SETUP_GUIDE.md
│   └── CHECKLIST.md
│
├── Scripts (provided)
│   ├── patch_generator.py
│   ├── geometric_transformation_tester.py
│   └── results_analyzer.py
│
├── Results (you create)
│   ├── exercise1_results/
│   ├── exercise2_videos/
│   ├── exercise3_plots/
│   └── final_report.pdf
│
└── Patches (you create)
    ├── custom_patches/
    └── transformations/
```

---

## 🎯 Your Next Action

**Right now, open two files:**

1. **`QUICK_START.md`** - Read this to understand the workflow
2. **`CHECKLIST.md`** - Use this to track your progress

Then launch your AWS instance and start Step 1!

---

## 📊 Time Allocation Suggestion

| Day | Task | Hours |
|-----|------|-------|
| Day 1 | AWS Setup | 2-3 |
| Day 2 | Exercise 1 | 3-4 |
| Day 3 | Exercise 2 | 2-3 |
| Day 4 | Exercise 3 | 2-3 |
| Day 5 | Report | 2-3 |

**Start today, finish by end of week!**

---

## 🌟 You've Got This!

I've prepared everything you need. The code from Challenge 1 is working great, and I've adapted it for Challenge 2. All the helper scripts are ready. Just follow the guides, work through the checklist, and you'll complete this challenge successfully!

**Remember:**
- Follow `QUICK_START.md` for the main workflow
- Use `CHECKLIST.md` to track progress
- Refer to helper scripts when needed
- Ask if you get stuck!

**Now go launch that AWS instance and let's get started! 🚀**

---

*Good luck with Challenge 2! - AI Assistant*

