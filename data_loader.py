import trimesh
import os
import numpy as np

def normalize_vertices(coords, target_range=(-1,1)):

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

def list_obj(dir_path):
    # list to store files
    res = []

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        # if os.path.isfile(os.path.join(dir_path, path)):
        res.append(os.path.join(dir_path, path))
    return res
def load_mesh(path, normalize = False, target_range = (-1,1)):
    scene = trimesh.load_mesh(path)
    if isinstance(scene, trimesh.Scene):
        geometries = list(scene.geometry.values())
        obj = geometries[0]
        if normalize:
            obj.vertices = normalize_vertices(obj.vertices, target_range=target_range)
        return obj
    else:
        if normalize:
            scene.vertices = normalize_vertices(scene.vertices)
        return scene
def load_meshes(path_list, normalize =False, target_range = (-1,1)):
    obj_list = []
    for path in path_list:
        o1 = load_mesh(path, normalize, target_range = target_range)
        obj_list.append(o1)
    
    return obj_list

# if __name__ == '__main__':
#     data_dir = 'D:\Projects\Shadow Art\data/02808440/02808440'
#     path_list = list_obj(data_dir)
#     print(path_list)