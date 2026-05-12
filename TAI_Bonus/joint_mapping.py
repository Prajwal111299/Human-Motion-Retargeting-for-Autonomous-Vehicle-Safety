import numpy as np
from scipy.spatial.transform import Rotation as R

def get_mapping_matrix():
    mapping = {}
    identity = np.eye(3)
    
    # Root Adjustment: Rotate -90 degrees X (Z-up to Y-up)
    r_root = R.from_euler('x', -90, degrees=True).as_matrix()
    mapping[0] = r_root 

    # Arm Adjustments: Align T-pose
    r_l_arm = R.from_euler('z', 90, degrees=True).as_matrix()
    mapping[16] = r_l_arm 
    mapping[18] = r_l_arm 
    mapping[20] = r_l_arm 

    r_r_arm = R.from_euler('z', -90, degrees=True).as_matrix()
    mapping[17] = r_r_arm 
    mapping[19] = r_r_arm 
    mapping[21] = r_r_arm 

    # Legs: Identity
    mapping[1] = identity 
    mapping[2] = identity 
    mapping[4] = identity 
    mapping[5] = identity 
    mapping[7] = identity 
    mapping[8] = identity 

    return mapping

# --- Helper Functions required by custom_walker_controller.py ---

def apply_rotation(global_pitch, global_yaw, global_roll, mapping_matrix):
    target_pose = R.from_euler('ZYX', [global_yaw, global_pitch, global_roll], degrees=True)
    
    if mapping_matrix is not None:
        R_final = mapping_matrix @ target_pose.as_matrix() @ mapping_matrix.T
    else:
        R_final = target_pose.as_matrix()
        
    local_yaw, local_pitch, local_roll = R.from_matrix(R_final).as_euler('ZYX', degrees=True)
    return local_pitch, local_yaw, local_roll

def smpl_to_ue4(p, y, r, m=None, x=False, yo=False, z=False):
    return apply_rotation(p, y, r, m)

def global_to_ue4_left_arm(p, y, r, m=None):
    return apply_rotation(p, y, r, m)

def global_to_ue4_right_arm(p, y, r, m=None):
    return apply_rotation(p, y, r, m)

def smpl_to_ue4_left_arm(p, y, r, m=None, x=False, yo=False, z=False):
    return apply_rotation(p, y, r, m)

def smpl_to_ue4_right_arm(p, y, r, m=None, x=False, yo=False, z=False):
    return apply_rotation(p, y, r, m)

def smpl_to_ue4_left_forearm(p, y, r, m=None, x=False, yo=False, z=False):
    return apply_rotation(p, y, r, m)

def smpl_to_ue4_right_forearm(p, y, r, m=None, x=False, yo=False, z=False):
    return apply_rotation(p, y, r, m)
