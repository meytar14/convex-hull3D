import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits import mplot3d

plt.axes(projection='3d')

z1=[1,2]
x1 = [1,2]
y1 =[1,2]

x2 = [3,1]
y2 = [3,1]
z2=[3,2]

# x3 = 0.8 * z
# y3 = 2.1 * x3
# z3=[]


plt.plot(x1, y1, z1, 'r', linewidth=2, label='Line 1')
plt.plot(x2, y2, z2, 'g', linewidth=2, label='Line 2')
#plt.plot(x3, y3, z, 'b', linewidth=2, label='Line 3')

plt.title('Plot multiple lines in 3D')
plt.legend()

plt.show()
