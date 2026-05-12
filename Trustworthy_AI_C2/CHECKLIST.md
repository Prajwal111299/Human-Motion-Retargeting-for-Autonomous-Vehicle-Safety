# Challenge 2 - Execution Checklist

Use this checklist to track your progress through Challenge 2.

## 🔧 Phase 1: AWS Instance Setup

### Step 1: Launch Instance
- [ ] Log into AWS Console
- [ ] Navigate to EC2
- [ ] Click "Launch Instance"
- [ ] Select Ubuntu 22.04 LTS
- [ ] Select g5.xlarge instance type
- [ ] Create/select key pair (.pem file)
- [ ] Configure 100GB storage
- [ ] Launch instance
- [ ] Note public IP address: `_________________`

### Step 2: Initial SSH Connection
- [ ] `chmod 400 your-key.pem`
- [ ] `ssh -i your-key.pem ubuntu@<IP>`
- [ ] Successfully logged in

### Step 3: Install NVIDIA Driver
- [ ] `sudo apt-get update`
- [ ] `sudo apt-get install -y nvidia-driver-525`
- [ ] STOP instance from AWS Console
- [ ] START instance again
- [ ] Note NEW IP address: `_________________`
- [ ] SSH back in: `ssh -i your-key.pem ubuntu@<NEW-IP>`
- [ ] Run `nvidia-smi` and verify GPU detected

### Step 4: Install Ubuntu Desktop
- [ ] `sudo apt-get update`
- [ ] `sudo apt-get install -y ubuntu-desktop`
- [ ] Wait for installation (15-30 minutes)

### Step 5: Install TurboVNC
- [ ] `cd ~`
- [ ] `wget https://sourceforge.net/projects/turbovnc/files/3.0.3/turbovnc_3.0.3_amd64.deb/download`
- [ ] `sudo dpkg -i download`
- [ ] `vncserver` (set password)
- [ ] Install TurboVNC Viewer on local machine
- [ ] Connect to: `ubuntu@<IP>:1`
- [ ] VNC connection successful

### Step 6: Install Miniconda
- [ ] `cd ~`
- [ ] `wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`
- [ ] `bash Miniconda3-latest-Linux-x86_64.sh`
- [ ] Accept license and confirm installation
- [ ] `source ~/.bashrc`
- [ ] Verify: `conda --version`

### Step 7: Setup CARLA
- [ ] Download CARLA from Google Drive (on local machine)
- [ ] `scp CARLA_0.9.13.tar.gz ubuntu@<IP>:~/`
- [ ] On AWS: `mkdir ~/carla`
- [ ] `tar -xzvf CARLA_0.9.13.tar.gz -C ~/carla/`
- [ ] `vim ~/.bashrc` and add CARLA paths:
  ```bash
  export CARLA_ROOT=/home/ubuntu/carla
  export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg
  export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
  ```
- [ ] `source ~/.bashrc`
- [ ] Test CARLA in VNC: `cd ~/carla && ./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000`
- [ ] CARLA starts successfully (Ctrl+C to stop)

### Step 8: Install SafeBench
- [ ] `conda create -n safebench python=3.8 -y`
- [ ] `conda activate safebench`
- [ ] `cd ~`
- [ ] `git clone --branch 24784_s23 https://github.com/trust-ai/SafeBench.git`
- [ ] `cd SafeBench`
- [ ] `pip install -r requirements.txt`
- [ ] `pip install -e .`
- [ ] No errors during installation

---

## 💻 Phase 2: Implementation

### Step 9: Implement get_pr_ap Function
- [ ] `cd ~/SafeBench`
- [ ] `vim safebench/util/metric_util.py`
- [ ] Find `get_pr_ap` function (around line 177)
- [ ] Replace with implementation from `get_pr_ap_implementation.py`
- [ ] Save file

**Code to insert:**
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

---

## 🔬 Phase 3: Exercise 1 - Model Comparison

### Experiment Setup
- [ ] Terminal 1: Start CARLA
  ```bash
  cd ~/carla
  ./CarlaUE4.sh -prefernvidia -RenderOffScreen -carla-port=2000
  ```
- [ ] Terminal 2: Activate environment
  ```bash
  conda activate safebench
  cd ~/SafeBench
  ```

### Texture 1: stopsign.jpg
- [ ] Run Faster R-CNN:
  ```bash
  python scripts/run.py --mode=eval --agent_cfg faster_rcnn.yaml \
    --scenario_cfg object_detection_stopsign.yaml --num_scenario 4
  ```
- [ ] Record results: mAP = _______, Std = _______

- [ ] Run YOLOv5:
  ```bash
  python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
    --scenario_cfg object_detection_stopsign.yaml --num_scenario 4
  ```
- [ ] Record results: mAP = _______, Std = _______

### Texture 2: stopsign_1.jpg
- [ ] Edit config: `vim safebench/scenario/config/object_detection_stopsign.yaml`
- [ ] Change `texture_dir` to `stopsign_1.jpg`
- [ ] Run Faster R-CNN
- [ ] Record results: mAP = _______, Std = _______
- [ ] Run YOLOv5
- [ ] Record results: mAP = _______, Std = _______

### Texture 3: stopsign_2.jpg
- [ ] Edit config: Change `texture_dir` to `stopsign_2.jpg`
- [ ] Run Faster R-CNN
- [ ] Record results: mAP = _______, Std = _______
- [ ] Run YOLOv5
- [ ] Record results: mAP = _______, Std = _______

### Results Table
| Model | Texture | mAP | Std |
|-------|---------|-----|-----|
| Faster R-CNN | stopsign.jpg | ___ | ___ |
| Faster R-CNN | stopsign_1.jpg | ___ | ___ |
| Faster R-CNN | stopsign_2.jpg | ___ | ___ |
| YOLOv5 | stopsign.jpg | ___ | ___ |
| YOLOv5 | stopsign_1.jpg | ___ | ___ |
| YOLOv5 | stopsign_2.jpg | ___ | ___ |

---

## 🎨 Phase 4: Exercise 2 - Custom Patches

### Create Patches (on local machine)
- [ ] `python patch_generator.py`
- [ ] Review generated patches
- [ ] Select promising patches

### Upload Patches to AWS
- [ ] `scp stopsign_with_*.jpg ubuntu@<IP>:~/SafeBench/safebench/scenario/scenario_data/template_od/`

### Test Patch 1: _______________ (patch name)
- [ ] Update config with patch filename
- [ ] Run Faster R-CNN
- [ ] mAP = _______ (Target: < 0.5) ✅/❌
- [ ] Run YOLOv5 with video:
  ```bash
  python scripts/run.py --mode=eval --agent_cfg yolo.yaml \
    --scenario_cfg object_detection_stopsign.yaml --num_scenario 4 --save_video
  ```
- [ ] mAP = _______ (Target: < 0.8) ✅/❌
- [ ] Video saved

### Test Patch 2: _______________ (patch name)
- [ ] Update config with patch filename
- [ ] Run Faster R-CNN
- [ ] mAP = _______ (Target: < 0.5) ✅/❌
- [ ] Run YOLOv5 with video
- [ ] mAP = _______ (Target: < 0.8) ✅/❌
- [ ] Video saved

### Custom Patch Design (if needed)
- [ ] Create custom patch with your design
- [ ] Test and iterate until targets achieved
- [ ] Final patch achieves: Faster R-CNN < 0.5 ✅, YOLOv5 < 0.8 ✅

### Collect Videos
- [ ] Video 1 location: `___________________________`
- [ ] Video 2 location: `___________________________`
- [ ] Copy to local: `scp -r ubuntu@<IP>:~/SafeBench/log/video ./exercise2_videos/`

---

## 📐 Phase 5: Exercise 3 - Geometric Transformations

### Transformation Group 1: _____________ (e.g., Size)

#### Generate Variations (on local machine)
- [ ] `python geometric_transformation_tester.py`
- [ ] Review generated variations

#### Upload to AWS
- [ ] `scp -r size_variations ubuntu@<IP>:~/SafeBench/safebench/scenario/scenario_data/template_od/`

#### Test Each Variation
Variation 1: _______
- [ ] Faster R-CNN mAP = _______
- [ ] YOLOv5 mAP = _______

Variation 2: _______
- [ ] Faster R-CNN mAP = _______
- [ ] YOLOv5 mAP = _______

Variation 3: _______
- [ ] Faster R-CNN mAP = _______
- [ ] YOLOv5 mAP = _______

(Continue for all variations...)

- [ ] Record videos for some variations (YOLOv5 with `--save_video`)

### Transformation Group 2: _____________ (e.g., Rotation)

#### Generate Variations
- [ ] Generated variations

#### Upload to AWS
- [ ] Uploaded to AWS

#### Test Each Variation
Variation 1: _______
- [ ] Faster R-CNN mAP = _______
- [ ] YOLOv5 mAP = _______

(Continue...)

- [ ] Record videos

### Create Plots
- [ ] Copy results to local machine
- [ ] Use `results_analyzer.py` to create plots
- [ ] Plot 1: Transformation 1 vs AP (Faster R-CNN)
- [ ] Plot 2: Transformation 1 vs AP (YOLOv5)
- [ ] Plot 3: Transformation 2 vs AP (Faster R-CNN)
- [ ] Plot 4: Transformation 2 vs AP (YOLOv5)

---

## 📝 Phase 6: Report Writing

### Exercise 1 Section
- [ ] Insert results table
- [ ] Write analysis comparing models
- [ ] Discuss texture impact

### Exercise 2 Section
- [ ] Insert results table
- [ ] Describe patch design strategy
- [ ] Include patch images
- [ ] Upload videos to Google Drive
- [ ] Insert Google Drive link

### Exercise 3 Section
- [ ] Insert all plots
- [ ] Write analysis of transformation impact
- [ ] Explain trends observed
- [ ] Upload videos to Google Drive
- [ ] Insert Google Drive link

### Final Checks
- [ ] All tables included
- [ ] All plots included
- [ ] All analysis written
- [ ] Google Drive link works
- [ ] All videos accessible
- [ ] Report formatted properly
- [ ] Spell check and grammar check

---

## 📤 Phase 7: Submission

### Files to Submit
- [ ] PDF report
- [ ] Google Drive link in report (videos)
- [ ] Code (if bonus attempted)

### Pre-Submission Verification
- [ ] All exercises completed
- [ ] All videos uploaded and accessible
- [ ] Report answers all questions
- [ ] Tables have actual data (not placeholders)
- [ ] Plots are clear and labeled
- [ ] Analysis is thorough

### Submit
- [ ] Submit to course platform
- [ ] Verify submission received

---

## 🧹 Cleanup

### AWS Cleanup
- [ ] Copy all results to local machine
- [ ] STOP (not terminate) AWS instance
- [ ] Or TERMINATE if completely done

---

## 📊 Progress Summary

Total Tasks: ~100
Completed: _____
Remaining: _____

Estimated Time Remaining: _____ hours
Target Completion Date: ___________

---

**Good luck! You've got this! 🚀**

