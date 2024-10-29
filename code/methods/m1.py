""" 
M1: Biased binary search that makes use of the radius sampling 
algorithm accounting for annotation budgets.
"""

import numpy as np
import random
import open3d as o3d

"""
    @method mod_diff
        Helper function to perform |x-y| for inputs x and y
    @param x: First input value
    @param y: Second input value
"""
def mod_diff(x,y):
    diff = x-y
    if diff >= 0:
        return diff
    else:
        return -1.0 * diff


"""
    @method l1_metric
        Metric to evaluate the performance of Radius sampling
    @param current: Query value
    @param target: Target value
"""
def l1_metric(current, target):
    return mod_diff(current, target)


"""
    @method l2_metric
        Metric to evaluate the performance of Radius sampling
    @param current: Query value
    @param target: Target value
"""
def l2_metric(current, target):
    return mod_diff(current, target)**2



"""
    @method sla_metric
        SLA Metric to evaluate the performance of Radius sampling
    @param current: Query value
    @param target: Target value
"""
def sla_metric(current, target):
    return 1.0 - mod_diff(current, target)/target


"""
    @method radius_sampling_api
        Perform radius sampling and return the number of candidate points
    @param pcd: Open3D Point cloud object
    @param r: Query radius value
"""
def radius_sampling_api(pcd, r):
    _, ind = pcd.remove_radius_oulier(nb_points=100, radius=r)
    num_output = len(ind)
    return num_output


"""
    @method biased_bsearch
        Biased binary search algorithm that accounts for point annotation budgets
    @param pcd: Open3D Point cloud object
    @param target_n_points: Number of requested points
    @param global_n_points: Total number of points in the point cloud
    @param min_r: Lower bound of search (default: 0.0)
    @param max_r: Upper bound of search (defailt: 1.0)
    @param max_n_trials: Maximum number of queries possible (default: 15)
    @param verbose: Toggle verbosity mode (default: False)
"""
def biased_bsearch(pcd, target_n_points, global_num_points, min_r=0.0, max_r=1.0, max_n_trials=15, verbose=False):
    # Keep track of number of trials
    current_num_trials = 0
    
    # Low and high values
    low = min_r
    high = max_r
    
    # Linear Bias BSearch
    fraction = (target_n_points)/global_num_points
    mid = low + (high-low)*fraction
    
    # Failsafe threshold (-1.0)
    failsafe_value = -1.0
    
    while low < high:
        # Call API at mid
        if verbose:
            print(f"[QUERYING {mid}]")
        query_points = radius_sampling_api(pcd=pcd, r=mid)

        if query_points == target_n_points:
            # Exact match found
            if verbose:
                print(f"[EXACT MATCH FOUND IN {current_num_trials} TRIALS]")
            return mid
        # Update number of trials and check for termination
        current_num_trials += 1
        if current_num_trials >= max_n_trials:
            # Timeout
            if verbose:
                print(f"[TIMEOUT] of {max_n_trials} REACHED")
            return mid
        
        if query_points > target_n_points:
            high = mid
        if query_points < target_n_points:
            low = mid
        
        mid = (low + high)/2
        
    if verbose:
        print("FAILSAFE CONDITION")
    return failsafe_value


if __name__ == "__main__":
    # Set random seeds
    random.seed(42)
    np.random.seed(42)

    # Load point cloud
    pcd = o3d.io.read_point_cloud('/path/to/L002.ply')
    print(pcd)
    
    # Load inputs
    global_num_points = 10283800
    target_n_points = int(0.10 * global_num_points)
    max_n_trials = 10
    
    # Perform biased binary search
    threshold = biased_bsearch(pcd=pcd,
        target_n_points=target_n_points,
        global_num_points=global_num_points,
        max_n_trials=max_n_trials,
        verbose=False
    )
    print(f"Selected parameter value: {threshold}")

    # Compute metrics
    selected_value = threshold
    comp_value = radius_sampling_api(pcd=pcd, r=threshold)
    l1 = l1_metric(current=comp_value, target=target_n_points)
    l2 = l2_metric(current=comp_value, target=target_n_points)
    sla = sla_metric(current=comp_value, target=target_n_points)
    print(f"Metrics: L1: {l1}, L2: {l2}, SLA: {sla}")

