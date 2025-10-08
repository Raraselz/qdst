from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

SIZE = (256, 192)

def dominant_color(image_path, k=5):
    image = Image.open(image_path)
    image = image.resize(SIZE)  # bigger SIZE takes longer to process
    pixels = np.array(image).reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=0).fit(pixels)
    counts = np.bincount(kmeans.labels_)
    dominant = kmeans.cluster_centers_[np.argmax(counts)]
    
    return tuple(map(int, dominant))

if __name__=="__main__":
    print(dominant_color('top.png'))  