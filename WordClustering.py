from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering

class KMeansWordClustering(KMeans):
    '''
    Perform a k-means clustering on the vocabulary from a word2vec model using
    scikitlearn's KMeans. Default values are used for everything but
    n_clusters when initializing KMeans.

    Parameters
    ----------

    n_clusters: int, optional, default: 10
    number of clusters

    model: str
    name of Word2Vec model

    Attributes
    ----------

    cluster_center_dict: dict
    number of cluster center : word most similar to corresponding vector

    labeled_words: dict
    word : center word of corresponding cluster

    sorted_words: dict
    center word : list of words in corresponding cluster
    '''
    def __init__(self, model, n_clusters=10):
        self.n_clusters = n_clusters
        self.loaded_model = Word2Vec.load(model)
        self.word_vec_mat = self.loaded_model[self.loaded_model.wv.vocab]
        super().__init__(n_clusters)
        self.fit(self.word_vec_mat)

    def cluster_center_dict(self):
        cluster_center_dict = {}
        for i in range(self.n_clusters):
            cluster_center_dict[i] = most_similar_word(self.cluster_centers_[i], self.loaded_model)

        return cluster_center_dict

    def labeled_words(self):
        labeled_words = {}
        labels = self.labels_
        cc_dict = self.cluster_center_dict()
        for i in range(self.word_vec_mat.shape[0]):
            labeled_words[most_similar_word(self.word_vec_mat[i,:], self.loaded_model)] = cc_dict[labels[i]]

        return labeled_words

    def sorted_words(self):
        sorted_words= {}
        cc_dict = self.cluster_center_dict()
        labeled_words = self.labeled_words()
        for i in range(self.n_clusters):
            words = [word for word in labeled_words if labeled_words[word] == cc_dict[i]]
            sorted_words[cc_dict[i]] = words

        return sorted_words

class SpectralWordClustering(SpectralClustering):
    '''
    Perform a spectral clustering on the vocabulary from a word2vec
    embedding using scikitlearn's SpectralClustering. Default values are used
    for everything except n_clusters, affinity, gamma, and n_neighbors when
    initializing SpectralClustering.

    Parameters
    __________

    n_clusters: int, default=10
    number of clusters

    affinity: str, 'rbf' or 'nearest_neighbors', default='rbf'
    affinity matrix to use for spectral clustering, restricted to Gaussian
    similarity or nearest neighbors.

    gamma: float, default=1.0
    scaling factor for RBF. ignored for nearest_neighbors.

    n_neighbors: int, default=10
    number of neighbors to use with nearest neighbors. ignored for RBF.

    model: str
    name of word2vec model to load

    Attributes
    __________

    labeled_words: dict
    word : corresponding cluster number

    sorted_words: dict
    cluster number : list of words in corresponding cluster

    '''

    def __init__(self, model, n_clusters=10, affinity='rbf', gamma=1.0, n_neighbors=10):
        self.n_clusters = n_clusters,
        self.loaded_model = Word2Vec.load(model)
        self.word_vec_mat = self.loaded_model[self.loaded_model.wv.vocab]
        super().__init__(n_clusters, affinity=affinity, gamma=gamma, n_neighbors=n_neighbors)
        self.labels = self.fit_predict(self.word_vec_mat)

    def labeled_words(self):
        labeled_words = {}
        for i in range(self.word_vec_mat.shape[0]):
            labeled_words[most_similar_word(self.word_vec_mat[i,:], self.loaded_model)] = self.labels[i]

        return labeled_words

    def sorted_words(self):
        sorted_words = {}
        labeled_words = self.labeled_words()
        for i in range(self.n_clusters):
            words = [word for word in labeled_words if labeled_words[word] == i]
            sorted_words[i] = words

        return sorted_words


def most_similar_word(vector, loaded_model):
    '''
    input--
    vector: array-like, shape(num_features of loaded_model)
    loaded_model: loaded word2vec model
    output--
    word: str, most similar word to vector in loaded_model
    '''
    return loaded_model.similar_by_vector(vector, topn=1)[0][0]
