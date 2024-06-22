import matplotlib.pyplot as plt
import numpy as np

# Given points
A = np.array([2, 3])
B = np.array([8, 7])
C = np.array([5, 6])  # Answer coordinates of point C

# Midpoint of AC lies on the line y = x + 1
midpoint_AC = (A + C) / 2

# Define lines
x = np.linspace(0, 10, 400)
y1 = x + 1
y2 = -2*x + 10

# Rotate point B 90 degrees clockwise around A
def rotate_point(point, angle, origin=(0, 0)):
    angle = np.deg2rad(angle)
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) + np.sin(angle) * (py - oy)
    qy = oy - np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return np.array([qx, qy])

# Points of new triangle after rotation
B_prime = rotate_point(B, -90, A)
C_prime = rotate_point(C, -90, A)

# Plot the triangle and lines
plt.figure(figsize=(8, 8))
plt.plot(x, y1, label='y = x + 1', linestyle='--')
plt.plot(x, y2, label='y = -2x + 10', linestyle='--')

# Plot original triangle
plt.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'b-', label='Original Triangle ABC')
plt.scatter([A[0], B[0], C[0]], [A[1], B[1], C[1]], color='b')

# Plot new triangle after rotation
plt.plot([A[0], B_prime[0], C_prime[0], A[0]], [A[1], B_prime[1], C_prime[1], A[1]], 'r-', label='Rotated Triangle A\'B\'C\'')
plt.scatter([A[0], B_prime[0], C_prime[0]], [A[1], B_prime[1], C_prime[1]], color='r')

# Labels
plt.text(A[0], A[1], 'A (2, 3)', fontsize=12, verticalalignment='bottom')
plt.text(B[0], B[1], 'B (8, 7)', fontsize=12, verticalalignment='bottom')
plt.text(C[0], C[1], 'C (5, 6)', fontsize=12, verticalalignment='bottom')
plt.text(B_prime[0], B_prime[1], 'B\'', fontsize=12, verticalalignment='bottom')
plt.text(C_prime[0], C_prime[1], 'C\'', fontsize=12, verticalalignment='bottom')

plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
plt.legend()
plt.title('Triangle Rotation and Lines')
plt.show()
