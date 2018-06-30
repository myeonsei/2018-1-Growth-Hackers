from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from scipy.misc import imread, imsave

#def recolor_image(input_file, k=5):
    
input_file = 'C:\\Users\\myeon\\Desktop\\Data Science\\0602 클러스터링\\sample.png'; k=5
#recolor_image(path)

img = imread(input_file)
pixels = [pixel for row in img for pixel in row]

model = KMeans(n_clusters = k, algorithm = 'auto')
model.fit(pixels)

def recolor(pixel):
    return model.predict(pixel)

new_img = [recolor(row) for row in img]

plt.imshow(new_img)
plt.axis('off')
plt.show()
