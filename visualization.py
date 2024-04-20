import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import numpy as np
import torch
from pytorch3d.structures.meshes import (
    Meshes,
    join_meshes_as_batch,
    join_meshes_as_scene
)
from pytorch3d.vis.plotly_vis import plot_scene
import plotly.graph_objects as go 

def plot_3d(points_list, color = 'b', sample = False, sampling_percent = 0.05):
  color = ['r','b','g','y','#000']
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  # ax = Axes3D(fig)
  for i, points in enumerate(points_list):
    if sample:
      points_idx = np.random.choice(range(0, len(points)), size = int(len(points) * sampling_percent), replace = False)
      points = points[points_idx]
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, c=color[i], marker='o')

  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')

  plt.show()

def scatter_plot(mask, grid):
    fig = go.Figure(data=[go.Scatter3d(
    x=grid[mask][:,0],
    y=grid[mask][:, 1],
    z=grid[mask][:,2],
    mode='markers',
    marker=dict(
        size=1,
        color='blue',
        opacity=0.8
    )
    )])

    fig.update_layout(scene=dict(
                        xaxis_title='X',
                        yaxis_title='Y',
                        zaxis_title='Z'),
                        margin=dict(l=0, r=0, b=0, t=0))
    fig.show()

def create_mesh(src_verts, src_faces):
  src_verts = torch.tensor(src_verts, dtype=torch.float32, device='cuda')
  src_faces = torch.tensor(src_faces, dtype=torch.int64, device='cuda')
  custom_mesh = Meshes(verts=[src_verts], faces=[src_faces])

  return custom_mesh

def combine_meshes(meshes_list):              # input is a list of meshes
  scene = join_meshes_as_scene(meshes_list)   # scene is also a mesh

  return scene

def show_scene(final_mesh, plot_name="subplot1"):
  fig = plot_scene({
      plot_name: {                           # change the name of the plot from here
          "mesh": final_mesh
      }
  })
  fig.show()

def scatter_plot(mask, grid, color = 'blue'):
  fig = go.Figure(data=[go.Scatter3d(
  x=grid[mask][:,0],
  y=grid[mask][:, 1],
  z=grid[mask][:,2],
  mode='markers',
  marker=dict(
      size=1,
      color=color,
      opacity=0.8
  )
  )])

  fig.update_layout(scene=dict(
                      xaxis_title='X',
                      yaxis_title='Y',
                      zaxis_title='Z'),
                      margin=dict(l=0, r=0, b=0, t=0))
  fig.show()