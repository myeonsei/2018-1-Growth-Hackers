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

## return predicted pic of simillar colors

import numpy as np

def replace_pred(model, pixels):
    pred = model.predict(pixels)
    di=dict(zip(range(pred.max()+1), model.cluster_centers_))
    for i in range(0,pred.max()+1):
        di[i]=list(map(int,(di[i])))
    rows, cols, channels = img.shape
    pred=pred.reshape(rows, cols).tolist()
    return np.array([[di[pixel] for pixel in row] for row in pred], dtype='uint8')

plt.imshow(replace_pred(model, pixels))
