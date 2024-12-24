import math

def reward_function(params):
    '''
    Enhanced reward function to balance staying near the center, maintaining speed, 
    minimizing unnecessary steering, and avoiding obstacles.
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    speed = params['speed']
    steering = abs(params['steering_angle'])  # Absolute value of the steering angle
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    
    # Initialize the reward
    reward = 1e-3
    
    # Marker distances for center line proximity
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Reward for staying close to the center line
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely off-track

    # Reward for staying on track
    if not all_wheels_on_track:
        return reward  # Immediate penalty if off-track

    # Encourage higher speeds with a reward factor
    SPEED_THRESHOLD = 2.0  # Adjust this threshold based on your specific needs
    if speed > SPEED_THRESHOLD:
        reward += 0.5

    # Penalize excessive steering to prevent zig-zagging
    ABS_STEERING_THRESHOLD = 15  # Degrees, adjust based on action space
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    # Reward progress to encourage completion and avoid getting stuck
    reward += 1e-2 * progress

    # Optional: Add a penalty for proximity to obstacles (if using objects in your environment)
    if 'objects_location' in params and 'closest_objects' in params:
        objects_location = params['objects_location']
        agent_x = params['x']
        agent_y = params['y']
        _, next_object_index = params['closest_objects']
        next_object_loc = objects_location[next_object_index]
        
        # Calculate distance to the next object
        distance_to_object = math.sqrt((agent_x - next_object_loc[0])**2 + (agent_y - next_object_loc[1])**2)
        
        # Penalize if too close to an object
        if distance_to_object < 0.3:
            reward = 1e-3  # Likely to crash, apply a harsh penalty
        elif distance_to_object < 0.5:
            reward *= 0.5
        elif distance_to_object < 0.8:
            reward *= 0.8

    return float(reward)
