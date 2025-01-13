from sklearn.cluster import KMeans
import numpy as np

def cluster_pois(pois, number_of_days):
    """
    Clusters a list of POIs into groups based on the number of days.
    
    Args:
        pois (list): A list of POI dictionaries, each containing 'lat' and 'lon'.
        number_of_days (int): The number of days to cluster POIs into.

    Returns:
        list of lists
    """
    if not pois or number_of_days <= 0:
        raise ValueError("POIs list must not be empty, and number_of_days must be greater than 0.")
    
    # Extract latitude and longitude as features for clustering
    coordinates = np.array([[poi['lat'], poi['lon']] for poi in pois])

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=number_of_days, random_state=42)
    kmeans.fit(coordinates)
    labels = kmeans.labels_

    # Organize POIs into clusters based on labels
    clustered_pois = [[] for _ in range(number_of_days)]
    for poi, label in zip(pois, labels):
        clustered_pois[label].append(poi)

    return clustered_pois

