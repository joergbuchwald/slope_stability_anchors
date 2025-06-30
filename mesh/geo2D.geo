//+ Parameters
thickness_fault_h = 0.0233;
dip_angle  = 65. * Pi / 180.;
dip_anglep = 90. * Pi / 180. - dip_angle;
thickness_fault = thickness_fault_h * Sin(dip_angle);
dx = (thickness_fault / 2.) * Sin(dip_angle) * Sin(dip_angle);
dy = (thickness_fault / 2.) * Sin(dip_angle) * Cos(dip_angle);
dx_i = 0.5 * Cos(dip_angle);
dy_i = 0.5 * Sin(dip_angle);
x_center = 10.;
y_center = 10.;
x_0 = x_center - Tan(dip_anglep) * 10. - thickness_fault_h / 2.;
y_0 = 0;
x_1 = x_center - Tan(dip_anglep) * 10. + thickness_fault_h / 2.;
y_1 = 0;
x_2 = x_center + Tan(dip_anglep) * 10. - thickness_fault_h / 2.;
y_2 = 20;
x_3 = x_center + Tan(dip_anglep) * 10. + thickness_fault_h / 2.;
y_3 = 20;
//
minitoring_pt_x = 10. - Cos(dip_angle) * 1.5;
minitoring_pt_y = 10. - Sin(dip_angle) * 1.5;
//
lc = 1.0;
fc = 0.5;
hc = 1.0;
//+ Nodal Coordinates
Point(1) = {0.,    0.,    0., lc * hc};
Point(2) = {x_0,   y_0,   0., lc * fc};
Point(3) = {x_1,   y_1,   0., lc * fc};
Point(4) = {20.,   0.,    0., lc * hc};
Point(5) = {20.,   20.,   0., lc * hc};
Point(6) = {x_2,   y_2,   0., lc * fc};
Point(7) = {x_3,   y_3,   0., lc * fc};
Point(8) = {0.,    20.,   0., lc * hc};
Point(9) = {x_0 - thickness_fault_h, y_0,  0.,  lc * hc};
Point(10)= {x_1 + thickness_fault_h, y_1,  0.,  lc * hc};
Point(11)= {x_2 - thickness_fault_h, 20.,  0.,  lc * hc};
Point(12)= {x_3 + thickness_fault_h, 20.,  0.,  lc * hc};
//+ Lines
Line(1) = {1,  9};
Line(2) = {9, 11};
Line(3) = {11, 8};
Line(4) = {8,  1};
Line(5) = {9,  2};
Line(6) = {2,  6};
Line(7) = {6, 11};
Line(8) = {2,  3};
Line(9) = {3,  7};
Line(10)= {7,  6};
Line(11)= {3, 10};
Line(12)= {10,12};
Line(13)= {12, 7};
Line(14)= {10, 4};
Line(15)= {4,  5};
Line(16)= {5, 12};
//+ Surfaces
Curve Loop(1) = {4, 1, 2, 3};
Plane Surface(1) = {1};
//+
Curve Loop(2) = {-2, 7, 6, 5};
Plane Surface(2) = {2};
//+
Curve Loop(3) = {-6, 10, 9, 8};
Plane Surface(3) = {3};
//+
Curve Loop(4) = {-9, 13, 12, 11};
Plane Surface(4) = {4};
//+
Curve Loop(5) = {-12, 14, 15, 16};
Plane Surface(5) = {5};
//+
Recombine Surface{1, 2, 3, 4, 5};
//+
// Define a MathEval field for mesh refinement
Field[1] = MathEval;
Field[1].F = "0.005 + 0.1*sqrt((x-10.)*(x-10.)+(y-10.)*(y-10.))";

// Set the background mesh field to the MathEval field
Background Field = 1;

// Set up the mesh options (optional, for finer control)
Mesh.Algorithm = 4; // Frontal-Delaunay for 2D
Mesh.CharacteristicLengthMin = 0.3;
Mesh.CharacteristicLengthMax = 0.9;
//+
Physical Surface("HostRock", 100) = {1, 2, 4, 5};
Physical Surface("Fault",    101) = {3};

// Generate the mesh
Mesh 2;





