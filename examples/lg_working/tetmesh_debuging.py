import numpy as np
from LoopStructural.supports.structured_tetra import TetMesh
from LoopStructural.datasets import load_noddy_single_fold
from LoopStructural.visualisation.model_visualisation import LavaVuModelViewer
from LoopStructural.utils.helper import strike_dip_vector, plunge_and_plunge_dir_to_vector

mesh = TetMesh(nsteps=[4,3,3])
tetra_index = np.arange(0,mesh.ntetra)
neighbours = np.zeros((mesh.ntetra,4)).astype(int)
neighbours[tetra_index%5 == 0,:] = tetra_index[tetra_index%5 == 0,None]  + np.arange(1,5)[None,:] # first tetra is the centre one so all of its neighbours are in the same cell
neighbours[tetra_index%5 != 0,0] = np.tile(tetra_index[tetra_index%5 == 0],(4,1)).flatten(order='F') # add first tetra to other neighbours

# now create masks for the different tetra indexes
one_mask = tetra_index%5 ==1
two_mask = tetra_index%5==2
three_mask = tetra_index%5 ==3
four_mask = tetra_index%5 ==4

even_mask = np.sum(mesh.global_index_to_cell_index(tetra_index//5),axis=0) // 2
odd_mask = ~even_mask

neighbours[np.logical_and(one_mask,even_mask)] = 0 #x+1, t = 4 and z-1 t=2, y+1 t3
c_xi, c_yi, c_zi = mesh.global_index_to_cell_index(tetra_index[np.logical_and(one_mask,even_mask)]//5)
mask = np.array([[1,0,0,4],[0,0,-1,2],[0,1,0,3]])
neigh_cell = np.zeros((c_xi.shape[0],3,3)).astype(int)
print(mask[0,:])
neigh_cell[:,:,0] = c_xi[:,None]+mask[:,0]
neigh_cell[:,:,1] = c_yi[:,None]+mask[:,1]
neigh_cell[:,:,2] = c_zi[:,None]+mask[:,2]
inside = neigh_cell[:,:,0] >= 0
inside = np.logical_and(inside,neigh_cell[:,:,1]>=0)
inside = np.logical_and(inside,neigh_cell[:,:,2]>=0)
inside = np.logical_and(inside,neigh_cell[:,:,0] < mesh.n_cell_x)
inside = np.logical_and(inside,neigh_cell[:,:,1] < mesh.n_cell_y)
inside = np.logical_and(inside,neigh_cell[:,:,2] < mesh.n_cell_z)
# print(neigh_cell)
# print(mesh.n_cell_x,mesh.n_cell_y,mesh.n_cell_z)
# raise BaseException
global_neighbour_idx = np.zeros((c_xi.shape[0],4)).astype(int)
global_neighbour_idx[:] = -1
print(neigh_cell)
print(mesh.global_cell_indicies(neigh_cell.T).shape)
global_neighbour_idx = mesh.global_cell_indicies(neigh_cell.T)#*5+mask[:,3]
global_neighbour_idx[inside] = -1
print(global_neighbour_idx)
neighbours[np.logical_and(two_mask,even_mask)] = 0 #x-1 t=3, y-1 t=4, z-1 t=1
neighbours[np.logical_and(three_mask,even_mask)] = 0 #x-1 t=2, y+1 t=1, z+1 t=4
neighbours[np.logical_and(four_mask,even_mask)] = 0 #x+1 t=1, y-1 t=2, z+1 t=3

neighbours[np.logical_and(one_mask,odd_mask)] = 0 #x-1 t=2, y-1 t=3, z+1 t=2
neighbours[np.logical_and(two_mask,odd_mask)] = 0 #x+1 t=3, y+1 t=4, z+1 t=2
neighbours[np.logical_and(three_mask,odd_mask)] = 0 #x+1 t=2, y-1 t=1, z-1 t=4
neighbours[np.logical_and(four_mask,odd_mask)] = 0 #x-1 t=1, y+1 t=2, z-1 t=3


neighbours[tetra_index%5 == 1,: ]
# print(neighbours)
# print(np.tile(tetra_index[tetra_index%5 == 0],(4,1)).flatten(order='F'))
# print(tetra_index)
# print('els',mesh.get_elements())
# neighbours2 = mesh.get_neighbours()
# # print('mask1',mesh.tetra_mask)
# # print('mask2',mesh.tetra_mask_even)
# # print(mesh.n_cell_x,mesh.n_cell_y,mesh.n_cell_z)
# neighbours = np.zeros((mesh.n_elements,4)).astype(int)
# neighbours[:] = -1
# elements = mesh.get_elements()
# print('ee',elements)
# for ie, e in enumerate(elements):
#     nn = 0
#     for iin, ne in enumerate(elements):
#         n = 0
#         for i in range(4):
#             for j in range(4):
#                 if e[i] == ne[j]:
#                     n+=1
#         if n == 3:
#             neighbours[ie,nn] = iin
#             nn+=1
# for i in range(neighbours.shape[0]):
#     for j in range(4):
#         if neighbours[i,j] not in neighbours2[i,:]:
#             print(neighbours[i,:],neighbours2[i,:])
    #   print(neighbours[i,:],neighbours2[i,:])