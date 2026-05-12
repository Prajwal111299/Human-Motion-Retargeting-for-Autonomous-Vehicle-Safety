# Human-Motion-Retargeting-for-Autonomous-Vehicle-Safety
Engineered a SMPL-to-CARLA skeletal joint mapping (scipy, Euler rotation matrices) to render WHAM-reconstructed human motion in CARLA simulator, enabling diverse realistic pedestrian simulation for autonomous vehicle safety-critical testing.

Human Motion Retargeting for Autonomous Vehicle Safety
This project implements an end-to-end pipeline for generating realistic human pedestrian motion in the CARLA autonomous driving simulator using state-of-the-art human motion reconstruction.
Overview
Autonomous vehicle safety testing requires diverse, realistic pedestrian behavior. This pipeline bridges the gap between real-world human motion capture and simulation environments by retargeting WHAM-reconstructed SMPL-H skeletal data into CARLA's UE4 skeleton system.
Pipeline

Motion Extraction — Run WHAM (CVPR 2024 SOTA) on real-world video to extract SMPL-H pose parameters (joint rotations, body shape betas)
Coordinate Transformation — Custom joint mapping (joint_mapping.py) converts SMPL-H global rotations to CARLA/UE4 local bone space using Euler rotation matrices via scipy
Skeleton Retargeting — Per-joint rotation matrices handle root Z-up to Y-up conversion, T-pose arm alignment, and leg identity mappings
CARLA Rendering — Retargeted motion drives pedestrian walkers in CARLA simulation for safety-critical AV testing scenarios

Key Technical Contributions

Custom SMPL-to-UE4 joint mapping with per-bone rotation correction
Root coordinate system transformation (Z-up → Y-up)
T-pose arm alignment for left/right limbs
Compatible with any WHAM-extracted motion sequence

Tech Stack: Python, CARLA, WHAM, scipy, NumPy, UE4 skeleton system
