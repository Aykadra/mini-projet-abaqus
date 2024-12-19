from meshio import read, write

mesh_coque = read(".\\MeshCoque.med", "med")
write(".\\MeshCoque.imp", mesh_coque, "abaqus")
