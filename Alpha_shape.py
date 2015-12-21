import time
t = time.time()
import numpy as np
# seed 1234 nb poinnt 1500 alpha -30
# seed 1234 nb point 15 alpha -2  
# seed 1234 nb point 15 alpha -1
np.random.seed(1234)
nombre_de_point = 15
points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]])
points = np.array( [[np.random.rand(),np.random.rand()]for i in range(nombre_de_point)])
from scipy.spatial import Voronoi, voronoi_plot_2d
# vor = Voronoi(points,furthest_site =True)
# vor1 = Voronoi(points,furthest_site =False)
import matplotlib.pyplot as plt
import math 

from collections import namedtuple
from math import sqrt
import itertools
 
Pt = namedtuple('Pt', 'x, y')
Circle = Cir = namedtuple('Circle', 'x, y, r')
 
def circles_from_p1p2r(p1, p2, r):
    'Following explanation at http://mathforum.org/library/drmath/view/53027.html'
    if r == 0.0:
        raise ValueError('radius of zero')
#     (x1, y1), (x2, y2) = p1, p2
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    if x1 == x2 and y1 == y2:
        raise ValueError('coincident points gives infinite number of Circles')
    # delta x, delta y between points
    dx, dy = x2 - x1, y2 - y1
    # dist between points
#     q = sqrt(dx**2 + dy**2)
    q = dist(p1,p2)
    if q > 2.0*r:
        print q,2.0*r,r
        raise ValueError('separation of points > diameter')
    # halfway point
    x3, y3 = (x1+x2)/2, (y1+y2)/2
    # distance along the mirror line
    d = sqrt(r**2-(q/2)**2)
    # One answer
    c1 = Cir(x = x3 - d*dy/q,
             y = y3 + d*dx/q,
             r = abs(r))
    # The other answer
    c2 = Cir(x = x3 + d*dy/q,
             y = y3 - d*dx/q,
             r = abs(r))
    return c1, c2

def dist(p,p1):
    return math.sqrt( (p[0]-p1[0])*(p[0]-p1[0]) + (p[1]-p1[1])*(p[1]-p1[1]))
print "begin..."
list_extrem = []
alpha = 1


if alpha < 0 :
    vor1 = Voronoi(points,furthest_site =False)

    for nb_point in range(len(points)):
        numero_region_point = vor1.point_region[nb_point]
        distance_max = -1
        list_max = []
        if -1 not in vor1.regions[numero_region_point]:
    
            for numero_vertices_region in vor1.regions[numero_region_point]:
                    distance_vertice_min_temp = dist(vor1.points[nb_point], vor1.vertices[numero_vertices_region])
                    list_max.append(distance_vertice_min_temp)
#           
            if  alpha <= - 1.0/max(list_max):
                list_extrem.append(list(points[nb_point]))
        else :
            if alpha <= 0:
                list_extrem.append(list(points[nb_point]))
            else:
                print " not possible, but algo says stuff"
                

else : 
    vor1 = Voronoi(points,furthest_site =True)

    for nb_point in range(len(points)):
        numero_region_point = vor1.point_region[nb_point]
        list_dist_min = []
        if vor1.regions[numero_region_point] != []:
            if vor1.regions[numero_region_point][0]==-1 and len(vor1.regions[numero_region_point]) ==1:
                if alpha ==0 :
                    list_extrem.append(list(points[nb_point])) 
                    print "not supposed to happenned but never too careful..."
            else :    
                for numero_vertices_region in vor1.regions[numero_region_point]:                    
                    if numero_vertices_region !=-1:
                        distance_vertice_min_temp = dist(vor1.points[nb_point], vor1.vertices[numero_vertices_region])
                        list_dist_min.append(distance_vertice_min_temp)
                if alpha <= 1.0/min(list_dist_min):
                    list_extrem.append(list(points[nb_point]))
                        

for a, b in itertools.combinations(list_extrem, 2):
    try :
        c1,c2 = circles_from_p1p2r(a, b,1.0/abs(alpha))    
        list_extrem_temp = list_extrem[:]
        list_extrem_temp.remove(a)
        list_extrem_temp.remove(b)
        list_distance_centre1 = []
        list_distance_centre2 = []
        for extrem in list_extrem_temp:
            list_distance_centre1.append(dist(c1, extrem))
            list_distance_centre2.append(dist(c2, extrem))
        if alpha < 0:
            if min(list_distance_centre1) >= -1.0/alpha or min(list_distance_centre2) >=- 1.0/alpha:
                plt.plot([a[0],b[0]],[a[1],b[1]],marker='o')
        else : 
            if max(list_distance_centre1) <= 1.0/alpha or max(list_distance_centre2) <= 1.0/alpha:
                plt.plot([a[0],b[0]],[a[1],b[1]],marker='o')      
    except ValueError as v:
        pass
#         print v, str(v) == "separation of points > diameter"
#         if str(v) == "coincident points gives infinite number of Circles":
#             pass
#             print "error"
#         elif str(v) == "separation of points > diameter":
#             
#             print('  ERROR: %s\n' % (v.args[0],))  
#             print  1.0/alpha,dist(a, b)      

# print list_extrem
list_extrem.sort()
a = list(list_extrem for list_extrem,_ in itertools.groupby(list_extrem))

# voronoi_plot_2d(vor1)
# print "vertices ",vor1.vertices
# print "point",vor1.points
# print vor1.ridge_vertices
# print "point region",vor1.point_region
# print "regions", vor1.regions

for i in points:
    plt.plot(i[0],i[1],color='blue',marker='o')
for i in a: 
#     print "list_extrem",i 
    plt.plot(i[0],i[1],color='red',marker = 'o')
        

    
    

"""
  
    points : ndarray of double, shape (npoints, ndim)
    Coordinates of input points.
    vertices : ndarray of double, shape (nvertices, ndim)
    Coordinates of the Voronoi vertices.
    ridge_points : ndarray of ints, shape (nridges, 2)
    Indices of the points between which each Voronoi ridge lies.
    ridge_vertices : list of list of ints, shape (nridges, *)
    Indices of the Voronoi vertices forming each Voronoi ridge.
    regions : list of list of ints, shape (nregions, *)
    Indices of the Voronoi vertices forming each Voronoi region.
    -1 indicates vertex outside the Voronoi diagram.
    point_region : list of ints, shape (npoints)
    Index of the Voronoi region for each input point.
    If qhull option "Qc" was not specified, the list will contain -1
    for points that are not associated with a Voronoi region.
"""
# for p in points:
#     for j in points:
#         plt.plot( (p[0]+j[0])/2, (p[1]+j[1])/2, color ='pink',marker='o')
#         print (p[0]+j[0])/2, (p[1]+j[1])/2
print time.time()-t
print "...end"
plt.show()
