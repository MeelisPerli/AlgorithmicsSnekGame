import unittest
import matrixoperations
import numpy as np
from snake import *
from copy import deepcopy
from geneticalgorithm import *

class TestGAMethods(unittest.TestCase):

    def testMatrixOperations(self):
        snake1 = Snake(1)
        a = deepcopy(snake1.genes())
        v = matrixoperations.mat_to_vector(a)
        b = matrixoperations.vector_to_mat(v, a)
        r = np.asarray(snake1.genes())
        self.assertEqual(b.shape, r.shape)
        for i in range(b.shape[0]):
            print(b[i].shape)
            self.assertEqual(b[i].shape, r[i].shape)
            for j in range(b[i].shape[0]):
                for k in range(b[i].shape[1]):
                    self.assertAlmostEqual(b[i][j][k], r[i][j][k], 4)

    def testCrossOver(self):
        s1 = Snake(1)
        s2 = Snake(1)
        c = Snake(1)
        GA = GeneticAlgorithm()
        GA.crossover(s1, s2, c, 0)
        g1 = np.asarray(s1.genes())
        g2 = np.asarray(s2.genes())
        g3 = np.asarray(c.genes())

        for i in range(g1.shape[0]):
            self.assertEqual(g1[i].shape, g3[i].shape)
            self.assertEqual(g1[i].shape, g2[i].shape)
            for j in range(g1[i].shape[0]):
                for k in range(g1[i].shape[1]):
                    v1 = g1[i][j][k]
                    v2 = g2[i][j][k]
                    v3 = g3[i][j][k]
                    if v3 == v1:
                        self.assertTrue(True)
                    elif v3 == v2:
                        self.assertTrue(True)
                    else:
                        print(v1, v2, v3)
                        self.assertAlmostEqual(v3, (v1 + v2) / 2, 3)


if __name__ == '__main__':
    unittest.main()
