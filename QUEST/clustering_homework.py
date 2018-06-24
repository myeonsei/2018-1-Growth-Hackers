from sklearn.cluster import KMeans

def recolor_image(input_file, k=5):

    img = mpimg.imread(path_to_png_file)
    pixels = [pixel for row in img for pixel in row]
    
    model = KMeans(n_clusters = k, algorithm = 'auto')
    model.fit(pixels)
    
    def recolor(pixel):
         return model.predict(pixel)

    new_img = [[recolor(pixel) for pixel in row]
               for row in img]

    plt.imshow(new_img)
    plt.axis('off')
    plt.show()