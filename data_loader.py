import trimesh
import os
import numpy as np

def normalize_vertices(coords, target_range=(100,150)):
    """
    Normalizes a list of 3D coordinates to fit within a given target range.

    Args:
        coords (list): A list of 3D coordinates, each represented as a tuple or list of (x, y, z).
        target_range (tuple): The desired target range for the normalized coordinates, default is (0, 1).

    Returns:
        list: A list of normalized 3D coordinates.
    """
    # Extract the minimum and maximum values for each dimension
    min_x = min(coord[0] for coord in coords)
    max_x = max(coord[0] for coord in coords)
    min_y = min(coord[1] for coord in coords)
    max_y = max(coord[1] for coord in coords)
    min_z = min(coord[2] for coord in coords)
    max_z = max(coord[2] for coord in coords)

    # Calculate the target range for each dimension
    target_min_x, target_max_x = target_range
    target_min_y, target_max_y = target_range
    target_min_z, target_max_z = target_range 

    # Normalize the coordinates to the target range
    normalized_coords = []
    for x, y, z in coords:
        normalized_x = (x - min_x) / (max_x - min_x) * (target_max_x - target_min_x) + target_min_x
        normalized_y = (y - min_y) / (max_y - min_y) * (target_max_y - target_min_y) + target_min_y
        normalized_z = (z - min_z) / (max_z - min_z) * (target_max_z - target_min_z) + target_min_z
        normalized_coords.append((normalized_x, normalized_y, normalized_z))

    return normalized_coords
    
def load_mesh(path):
    scene = trimesh.load_mesh(path)
    if isinstance(scene, trimesh.Scene):
        geometries = list(scene.geometry.values())
        obj = geometries[0]
        obj.vertices = normalize_vertices(obj.vertices)
        return obj
    else:
        scene.vertices = normalize_vertices(scene.vertices)
        return scene


def list_obj(dir_path):
    # list to store files
    res = []

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(os.path.join(dir_path, path))
    return res

def load_meshes(path_list):
    obj_list = []
    for path in path_list:
        o1 = load_mesh(path)
        obj_list.append(o1)
    
    return obj_list
# dir_path = 'D:/Projects/Shadow Art/data/sparse'
# res  = list_obj(dir_path)
# print(len(res))

if __name__ == '__main__':
    data_dir = 'D:/Projects/Shadow Art/data/sparse'
    path_list = list_obj(data_dir)

    import random 
    from data_loader import load_mesh
    random_sample = random.sample(path_list, 5)
    obj  = load_meshes(random_sample)

    print(np.min(obj[0].vertices))