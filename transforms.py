import numpy as np

def rotate(vertices, theta):
    R = np.array([[np.cos(theta[1])*np.cos(theta[2]),       np.sin(theta[0])*np.sin(theta[1])*np.cos(theta[2]) - np.sin(theta[2])*np.cos(theta[0]),      np.sin(theta[1])*np.cos(theta[0])*np.cos(theta[2]) + np.sin(theta[0])*np.sin(theta[2])],
                  [np.sin(theta[2])*np.cos(theta[1]),       np.sin(theta[0])*np.sin(theta[1])*np.sin(theta[2]) + np.cos(theta[0])*np.cos(theta[2]),      np.sin(theta[1])*np.sin(theta[2])*np.cos(theta[0]) - np.sin(theta[0])*np.cos(theta[2])],
                  [-np.sin(theta[1]),                        np.sin(theta[0])*np.cos(theta[1]),                                                           np.cos(theta[0])*np.cos(theta[1])]])
    
    return np.matmul(vertices, R.T)

def round_to_interval(number, a, b, k):
    # Calculate the interval size
    interval_size = (b - a) / k
    clipped_coordinates = np.clip(number, a, b)
    # Find the closest interval and round to its midpoint
    closest_interval = np.round((clipped_coordinates - a) / interval_size)
    rounded_value = a + closest_interval * interval_size
    
    return rounded_value

def flatten_index(num, a, b, k):
    interval_size = (b - a) / k
    num = (num - a) / interval_size
    # k = k+1
    return np.round((num[:,1] * k *k) + (num[:,0] * k) + num[:,2]).astype(np.int32)

#SDF tranforming function 
def SDF_transform(SDF_list,R, T, grid):
    '''SDF_list: list of vertices 
        T: Transform [1*3]
        R: Euler angles [1*3]
        a: minimum of the grid
        b: maximum of the grid
        k: number interval
        returns: list of transformed sdf 
    '''
    
    d = grid[1][2] -  grid[0][0]
    k = int(np.cbrt(len(grid)))
    a = grid[0][0]
    b = grid[-1][0] + d

    num_meshes = len(SDF_list)

    new_vertices = []
    old_vertices = []
    MAX = k ** 3
    new_SDF = np.zeros((num_meshes,MAX ), dtype= bool)

    for s in SDF_list:
        old_vertices.append(grid[s])
        
    for i in range(num_meshes):
        vertices = rotate(old_vertices[i], R)
        vertices = vertices + T 
        vertices = round_to_interval(vertices, a, b, k)
        new_vertices.append(vertices)
        mask = flatten_index(vertices, a, b,k )
        mask = mask[mask < MAX]
        new_SDF[i][mask] = True
        
    return new_SDF