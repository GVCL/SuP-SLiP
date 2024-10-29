""" 
M2: Point cloud normalisation and KD-Tree Generation.
"""

import numpy as np
import pandas as pd
import open3d.ml.torch as ml3d  
from scipy.spatial import KDTree
import sys
import random

"""
    @method normalise_point_cloud
        Normalise point cloud using mean and stddev and return normalised points
    @param data: Open3D-ML dataset object, format: {'data': ..., 'point' : ...} 
"""
def normalise_point_cloud(data):
    # Calculate mean and standard deviation values
    X = data["point"][:,0]
    Y = data["point"][:,1]
    Z = data["point"][:,2]
    df = pd.DataFrame({
        "x" : X,
        "y" : Y,
        "z" : Z
    })

    X_mean = df["x"].mean()
    X_sd = df["x"].std()
    Y_mean = df["y"].mean()
    Y_sd = df["y"].std()
    Z_mean = df["z"].mean()
    Z_sd = df["z"].std()

    # Perform normalisation
    all_xyz_points_norm = []
    for i in range(len(data["point"])):
        xyz = data["point"][i]
        x = (xyz[0] - X_mean)/X_sd
        y = (xyz[1] - Y_mean)/Y_sd 
        z = (xyz[2] - Z_mean)/Z_sd
        
        norm_xyz = np.array([x, y, z])
        all_xyz_points_norm.append(norm_xyz)

    assert len(all_xyz_points_norm) == len(data["point"])
    return all_xyz_points_norm


"""
    @method generate_kdtree_index
        Generate KDTree on the normalised points
    @param normalised_points: List containing normalised points
"""
def generate_kdtree_index(normalised_points):
    v = []
    for i in range(len(normalised_points)):
        v.append(normalised_points[i])
    kdtree = KDTree(data=v, leafsize=10)
    return kdtree


"""
    @method query_tree
        Wrapper to KDTree query operation
    @param kdtree: Constructed Scipy KDTree object
    @param point: [<x,y,z>] point to query for
    @param k: Number of nearest neighbours to return
"""
def query_tree(kdtree, point, k):
    distances, neighbours = kdtree.query(x=point, k=k)
    return distances, neighbours


if __name__ == "__main__":
    # Set recursion limit
    sys.setrecursionlimit(100_000)

    # Set random seeds
    random.seed(42)
    np.random.seed(42)


    # Load Toronto3D dataset
    dataset = ml3d.datasets.Toronto3D(dataset_path='/path/to/Toronto3D')
    test_split = dataset.get_split("test")
    data = test_split.get_data(0)

    # Get normalised point cloud
    all_points_xyz_norm = normalise_point_cloud(data=data)

    # Construct KD Tree
    kdtree = generate_kdtree_index(normalised_points=all_points_xyz_norm)

    # Query for a point
    sample_point = all_points_xyz_norm[0]
    k = 25
    distances, neighbours = query_tree(kdtree=kdtree, point=sample_point, k=k)
    for d, n in zip(distances, neighbours):
        print(f"Point {all_points_xyz_norm[n]} is at distance {d} from {sample_point}")
