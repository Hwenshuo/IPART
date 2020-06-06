"""
The Ramer-Douglas-Peucker algorithm roughly ported from the pseudo-code provided
by http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
"""

from math import sqrt
from .funcs import greatCircle, getCrossTrackDistance
import numpy as np

def distance(a, b):
    return  sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def point_line_distance(point, start, end):
    if (start == end):
        return distance(point, start)
    else:
        n = abs((end[0]-start[0])*(start[1]-point[1])-\
                (start[0]-point[0])*(end[1]-start[1]))
        d = sqrt((end[0]-start[0])**2+(end[1]-start[1])**2)

        return n / d

def rdp(points, epsilon):
    """
    Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon:
        results = rdp(points[:index+1], epsilon)[:-1] + rdp(points[index:], epsilon)
    else:
        results=[points[0],points[-1]]

    return results

def distanceGC(a,b):
    '''Great circle distance
    <a>, <b>: (lat, lon)
    '''
    return greatCircle(a[0],a[1],b[0],b[1],r=1)

def point_line_distanceGC(point,start,end):
    if (start == end):
        return distanceGC(point, start)/np.pi*180.
    else:
        dxt=getCrossTrackDistance(start[0],start[1],
                end[0],end[1],
                point[0],point[1],
                r=1)

        dxt=abs(dxt/np.pi*180)
        return dxt

def rdpGC(points, epsilon):
    """
    Geodesic version of rdp.

    Points are using lat, lon coordinates.
    Distances are measured in great circle distance on a unit sphere, then
    converted to degree.

    epsilon is in unit degree latitude/longitude
    """

    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distanceGC(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon:
        results = rdpGC(points[:index+1], epsilon)[:-1] + rdpGC(points[index:], epsilon)
    else:
        results=[points[0],points[-1]]

    return results


if __name__=='__main__':

    points=[(0,0), (10,10), (20,20), (40,25), (41,26), (30,30), (32,40)]
    points=[(-10,0), (0,10), (10,0)]
    p2=rdp(points,2)
    p3=rdpGC(points,5)

    #-------------------Plot------------------------
    import matplotlib.pyplot as plt
    figure=plt.figure(figsize=(12,10),dpi=100)
    ax=figure.add_subplot(111)

    ps=np.array(points)
    p2s=np.array(p2)
    p3s=np.array(p3)
    ax.plot(ps[:,1], ps[:,0], 'b-o')
    ax.plot(p2s[:,1], p2s[:,0], 'ro')
    ax.plot(p3s[:,1], p3s[:,0], 'k^')
    ax.set_aspect('equal')
    ax.grid(which='both')

    plt.show(block=False)
