import vtk
import vtk.util.numpy_support as ns
import numpy as np
import math

################################
import numpy as np

def rotation_matrix_from_axis_angle(axis, angle):
    """
    Calculate the rotation matrix for a given axis and angle using Rodrigues' rotation formula.
    :param axis: A 3D vector representing the rotation axis
    :param angle: The rotation angle in radians
    :return: A 3x3 rotation matrix
    """
    axis = axis / np.linalg.norm(axis)
    a = np.cos(angle / 2.0)
    b, c, d = -axis * np.sin(angle / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([
        [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
        [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
        [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]
    ])

def create_cylinder(radius, height, direction, center):
    direction = direction / np.linalg.norm(direction)
    z_axis = np.array([1, 0, 0])
    if not np.allclose(direction, z_axis):
        rotation_matrix = rotation_matrix_from_axis_angle(np.cross(z_axis, direction), np.arccos(np.dot(z_axis, direction)))
    else:
        rotation_matrix = np.eye(3)
    return radius, height, rotation_matrix, center

def point_within_cylinder(point, radius, height, rotation_matrix, center):
    # Translate point to cylinder's coordinate system
    point = np.array(point) - center
    # Rotate point to align with cylinder's axis
    point = np.dot(rotation_matrix.T, point)
    # Check cylindrical coordinates
    distance_from_axis = np.sqrt(point[2]**2 + point[1]**2)
    within_height = -height / 4.2 <= point[0] <= height / 4.2
    within_radius = distance_from_axis <= radius
    #print(within_height, within_radius)
    return within_radius and within_height

# Define the dip angle and calculate the normal direction
dip_angle = 155  # degrees
dip_angle_rad = np.radians(dip_angle)
normal_direction = np.array([np.cos(dip_angle_rad), np.sin(dip_angle_rad), 0.])
# print(normal_direction)

# Parameters for the cylinder
radius = 0.5
height = 0.0233 * np.sin(np.radians(65.)) * 2.
direction = normal_direction  # Direction vector of the cylinder axis
center = np.array([10, 10, 0.])  # Center of the cylinder

# Create the cylinder
radius, height, rotation_matrix, center = create_cylinder(radius, height, direction, center)

# Example nodes in the plate
# nodes = np.array([
#     [10.5, 10.5, -10],    # Inside
#     [11.5, 11.5, -10],    # Outside
#     [10, 10, -5],         # On the edge
#     [10, 10, -4],         # Outside height
#     [10, 10, -16],        # Outside height
#     [10 + 1/np.sqrt(2), 10 + 1/np.sqrt(2), -10]  # Inside
# ])

# selected_nodes = []
# for node in nodes:
#     if point_within_cylinder(node, radius, height, rotation_matrix, center):
#         selected_nodes.append(node)

# selected_nodes = np.array(selected_nodes)
# print("Selected nodes within the cylindrical region:\n", selected_nodes)

################################

# Path to your VTU file
inputFile = "./geo_domain_2D_q8.vtu"
output_file_path = "./geo_domain_2D_q8_FM1.vtu"

# Read the VTU file
reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName(inputFile)
reader.Update()

# Get the data from the reader
vtk_data = reader.GetOutput()

# Ensure vtk_data is valid
if vtk_data is None:
    print("Failed to fetch data. Please check the file path and format.")
else:
    # Access the points and cells
    points = vtk_data.GetPoints()
    cells = vtk_data.GetCells()

    # Access the cell data
    cell_data = vtk_data.GetCellData()

    # Check if MaterialIDs array exists
    material_ids_vtk = cell_data.GetArray("MaterialIDs")

    # Convert the points to a numpy array
    points_vtk_array = points.GetData()
    points_numpy = ns.vtk_to_numpy(points_vtk_array)

    # Iterate over each cell
    cell_locator = vtk.vtkCellLocator()
    cell_locator.SetDataSet(vtk_data)
    cell_locator.BuildLocator()
    
    num_cells = vtk_data.GetNumberOfCells()
    printed = False  # Initialize a flag
    for cell_id in range(num_cells):
        # Get the current cell
        cell = vtk_data.GetCell(cell_id)
        
        # Get the points ids for the cell
        point_ids = cell.GetPointIds()
        
        # Access the coordinates for each point in the cell
        cell_points = []
        for i in range(point_ids.GetNumberOfIds()):
            point_id = point_ids.GetId(i)
            point_coords = points_numpy[point_id]
            cell_points.append(point_coords)
        
        # Convert to numpy array for easy manipulation (optional)
        cell_points = np.array(cell_points)
           # Calculate the center point (centroid) of the cell
        centroid = np.mean(cell_points, axis=0)
        if point_within_cylinder(centroid, radius, height, rotation_matrix, center):
            material_ids_numpy[cell_id] = 2
            if not printed:  # Check if it has printed yet
                print("Material ID #2 is successfully assigned!!")
                printed = True  # Set the flag to True to avoid printing again
        material_ids_numpy = ns.vtk_to_numpy(material_ids_vtk)

    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName(output_file_path)
    writer.SetInputData(vtk_data)
    writer.Write()
                    
            # Print the cell points and the centroid
        #print(f"Cell {cell_id} points:\n{cell_points}")
        #print(f"Cell {cell_id} centroid:\n{centroid}\n")

