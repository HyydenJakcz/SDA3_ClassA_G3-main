import numpy as np
position = (114, 122)
theta = np.radians(-90)
c,s = np.cos(theta), np.sin(theta)
result = np.array(((c,-s), (s,c)))
resultant_point = np.dot(position, result)
pointX, pointY = resultant_point

print(resultant_point)

rotationMatrix = np.array(((1, 0), (0, -1)))
result = np.dot(position, rotationMatrix)

print(result)