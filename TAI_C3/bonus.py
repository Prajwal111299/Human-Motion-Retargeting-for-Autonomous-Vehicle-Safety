'''
Date: 2023-01-31 22:23:17
Description: Bonus Agent for Trustworthy AI Challenge
'''

import numpy as np
import math
import carla 

from safebench.agent.base_policy import BasePolicy
from agents.navigation.basic_agent import BasicAgent  

class CarlaBonusAgent(BasePolicy):
    name = 'bonus'
    type = 'unlearnable'

    def __init__(self, config, logger):
        self.logger = logger
        self.num_scenario = config['num_scenario']
        self.ego_action_dim = config['ego_action_dim']
        self.model_path = config['model_path']
        self.mode = 'train'
        self.continue_episode = 0
        self.route = None
        self.controller_list = []

        self.target_speed = config['target_speed']
        dt = config['dt']
        lateral_KP = config['lateral_KP']
        lateral_KI = config['lateral_KI']
        lateral_KD = config['lateral_KD']
        longitudinal_KP = config['longitudinal_KP']
        longitudinal_KI = config['longitudinal_KI']
        longitudinal_KD = config['longitudinal_KD']
        max_steering = config['max_steering']
        max_throttle = config['max_throttle']

        self.opt_dict = {
            'lateral_control_dict': {'K_P': lateral_KP, 'K_I': lateral_KI, 'K_D': lateral_KD, 'dt': dt},
            'longitudinal_control_dict': {'K_P': longitudinal_KP, 'K_I': longitudinal_KI, 'K_D': longitudinal_KD, 'dt': dt},
            'max_steering': max_steering,
            'max_throttle': max_throttle,
        }

    def set_ego_and_route(self, ego_vehicles, info):
        self.ego_vehicles = ego_vehicles
        self.controller_list = []
        for e_i in range(len(ego_vehicles)):
            controller = BasicAgent(self.ego_vehicles[e_i], target_speed=self.target_speed, opt_dict=self.opt_dict)
            dest_waypoint = info[e_i]['route_waypoints'][-1]
            location = dest_waypoint.transform.location
            controller.set_destination(location)
            self.controller_list.append(controller)

    def train(self, replay_buffer):
        pass

    def set_mode(self, mode):
        self.mode = mode

    def get_action(self, obs, infos, deterministic=False):
        actions = []
        for i, info_item in enumerate(infos):
            scenario_id = info_item['scenario_id']
            controller = self.controller_list[scenario_id]
            ego_vehicle = self.ego_vehicles[scenario_id]
            
            world = ego_vehicle.get_world()
            actors = world.get_actors()
            walkers = actors.filter('walker.pedestrian.*')
            
            ego_loc = ego_vehicle.get_location()
            min_dist = 9999.0
            
            for w in walkers:
                w_loc = w.get_location()
                dist = math.sqrt((w_loc.x - ego_loc.x)**2 + (w_loc.y - ego_loc.y)**2)
                if dist < min_dist:
                    min_dist = dist
            
            if min_dist < 8.0:
                controller.set_target_speed(0.0)
            elif min_dist < 15.0:
                controller.set_target_speed(10.0)
            else:
                controller.set_target_speed(self.target_speed)

            control = controller.run_step()
            throttle = control.throttle
            steer = control.steer
            
            if min_dist < 8.0:
                throttle = 0.0
                
            actions.append([throttle, steer]) 
            
        actions = np.array(actions, dtype=np.float32)
        return actions

    def load_model(self):
        pass

    def save_model(self):
        pass
