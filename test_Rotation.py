from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math as m
def get_Rotationmatrix(theta, arg):
    cx = m.cos(theta)
    sx = m.sin(theta)
    if arg == 'x':
        R = np.array([[1.,0.,0.],[0.,cx,-sx],[0.,sx,cx]])
    elif arg == 'y':
        R = np.array([[cx, 0., sx], [0., 1., 0.], [-sx,0., cx]])
    elif arg == 'z':
        R = np.array([[cx, -sx, 0.], [sx, cx, 0.], [0.,0.,1.]])

    return R

fig = plt.figure()
ax = fig.gca(projection='3d')

# Make the grid
x, y, z = np.meshgrid(np.array([1]),
                      np.array([1]),
                      np.array([1]))

# Make the direction data for the arrows
T = np.eye(3)
u = T[:,0]
v = T[:,1]
w = T[:,2]

Rx = get_Rotationmatrix(np.pi/2,'x')
Ry = get_Rotationmatrix(np.pi/2,'y')
print(np.dot(Rx, Ry))
theta = [np.pi/3, np.pi/3, np.pi/3]
ax.quiver(x, y, z, u, v, w, length=0.05, normalize=True,color='r')
u = np.dot(get_Rotationmatrix(theta[0], 'z'),u)
v = np.dot(get_Rotationmatrix(theta[0], 'z'),v)
w = np.dot(get_Rotationmatrix(theta[0], 'z'),w)
ax.quiver(x, y, z, u, v, w, length=0.05, normalize=True,color='g')
u = np.dot(get_Rotationmatrix(theta[0], 'y'),u)
v = np.dot(get_Rotationmatrix(theta[0], 'y'),v)
w = np.dot(get_Rotationmatrix(theta[0], 'y'),w)
ax.quiver(x, y, z, u, v, w, length=0.05, normalize=True,color='b')



ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# ax1 = fig.gca(projection='3d')
# theta = [np.pi/3, np.pi/3, np.pi/3]
# ax1.quiver(x, y, z, u, v, w, length=0.05, normalize=True,color='b')
# u = np.dot(get_Rotationmatrix(theta[0], 'x'),u)
# v = np.dot(get_Rotationmatrix(theta[0], 'x'),v)
# w = np.dot(get_Rotationmatrix(theta[0], 'x'),w)
# ax1.quiver(x, y, z, u, v, w, length=0.05, normalize=True,color='r')
# u = np.dot(get_Rotationmatrix(theta[0], 'z'),u)
# v = np.dot(get_Rotationmatrix(theta[0], 'z'),v)
# w = np.dot(get_Rotationmatrix(theta[0], 'z'),w)

plt.show()