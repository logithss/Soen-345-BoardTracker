import numpy as np
import cv2
import matplotlib.pyplot as plt

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread('sample.png')
pts1=np.float32([[0,200],[200,200],[200,0],[0,0]]) 
pts2=np.float32([[0,200],[200,200],[200,0],[0,0]])
matrix=cv2.getPerspectiveTransform(pts1,pts2)

# Draw the point
p = (50,100)
cv2.circle(image,p, 20, (255,0,0), -1)

# Put in perspective
result=cv2.warpPerspective(image,matrix,(1500,800))

# Show images
plt.imshow(image)
plt.title('Original')
plt.show()

plt.imshow(result)
plt.title('Distorced')
plt.show()

# Here you can transform your point
p = (50,100)
px = (matrix[0][0]*p[0] + matrix[0][1]*p[1] + matrix[0][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
py = (matrix[1][0]*p[0] + matrix[1][1]*p[1] + matrix[1][2]) / ((matrix[2][0]*p[0] + matrix[2][1]*p[1] + matrix[2][2]))
p_after = (int(px), int(py))
print(p_after)

# Draw the new point
cv2.circle(result,p_after, 20, (0,0,255), 12)

# Show the result
plt.imshow(result)
plt.title('Predicted position of your point in blue')
plt.show()