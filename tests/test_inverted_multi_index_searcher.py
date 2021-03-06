import unittest

import numpy as np
from core.quantization import pq_quantizer

from core.search import inverted_multi_index_searcher as imis


class InvertedMultiIndexSearcherTest(unittest.TestCase):
    def test_inverted_multi_index_searcher_build_from_vectors(self):
        base_vectors = np.array([
            [0, 2, 4, 5],
            [0, 5, 4, 10],
            [10, 2, 60, 5],
            [10, 5, 60, 10]
        ], dtype=np.float32)
        ids_ndarray = np.array([10, 20, 30, 40], dtype=np.int32)

        query_vectors = np.array([
            [0, 2, 4, 5],
            [10, 2, 60, 5]
        ], dtype=np.float32)

        pq = pq_quantizer.PQQuantizer(n_clusters=2, n_quantizers=2)
        pq.fit(base_vectors)
        cluster_centers = pq.get_cluster_centers()
        searcher_ = imis.InvertedMultiIndexSearcher(x=base_vectors, x_ids=ids_ndarray,
                                                    cluster_centers=cluster_centers)

        subspaced_indices_T = pq.predict_subspace_indices(base_vectors)
        print(subspaced_indices_T)

        nearest_ids_ndarray = searcher_.find_nearest_ids(query_vectors, n_nearest=4)
        print(nearest_ids_ndarray)

        self.assertEqual(set(nearest_ids_ndarray[0, 0:2]), {10, 20})
        self.assertEqual(set(nearest_ids_ndarray[0, 2:5]), {30, 40})

        self.assertEqual(set(nearest_ids_ndarray[1, 0:2]), {30, 40})
        self.assertEqual(set(nearest_ids_ndarray[1, 2:5]), {10, 20})

    def test_inverted_multi_index_searcher(self):
        base_vectors = np.array([
            [0, 2, 4, 5],
            [0, 5, 4, 10],
            [10, 2, 60, 5],
            [10, 5, 60, 10]
        ], dtype=np.float32)

        ids_ndarray = np.array([10, 20, 30, 40], dtype=np.int32)

        query_vectors = np.array([
            [0, 2, 4, 5],
            [10, 2, 60, 5]
        ], dtype=np.float32)

        pq = pq_quantizer.PQQuantizer(n_clusters=2, n_quantizers=2)
        pq.fit(base_vectors)
        cluster_centers = pq.get_cluster_centers()

        base_vectors_subspaced_centroid_indices_T = pq.predict_subspace_indices(base_vectors)
        base_vectors_subspaced_centroid_indices = base_vectors_subspaced_centroid_indices_T.transpose().astype(dtype='int32',
            order='C')

        searcher_ = imis.InvertedMultiIndexSearcher(x_ids=ids_ndarray,
                                                    cluster_centers=cluster_centers,
                                                    x_pqcodes=base_vectors_subspaced_centroid_indices)

        nearest_ids_ndarray = searcher_.find_nearest_ids(query_vectors, n_nearest=4)
        print(nearest_ids_ndarray)

        self.assertEqual(set(nearest_ids_ndarray[0, 0:2]), {10, 20})
        self.assertEqual(set(nearest_ids_ndarray[0, 2:5]), {30, 40})

        self.assertEqual(set(nearest_ids_ndarray[1, 0:2]), {30, 40})
        self.assertEqual(set(nearest_ids_ndarray[1, 2:5]), {10, 20})


if __name__ == '__main__':
    unittest.main()
