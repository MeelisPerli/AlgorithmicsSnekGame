from typing import List, Tuple
import numpy as np


def mat_to_vector(weights: List) -> np.ndarray:
    """
    Transform weights from list containing arrays to one vector
    :param weights: list containing weights
    :return: a numpy array
    """

    """
    weights = np.asmatrix(weights)
    weights_vec = []
    for sol_idx in range(weights.shape[0]):
        vector = []
        for layer_idx in range(weights.shape[1]):
            vector_weights = np.reshape(weights[sol_idx, layer_idx],
                                        newshape=(weights[sol_idx, layer_idx].size))
            vector.extend(vector_weights)
        weights_vec.append(vector)

    return np.array(weights_vec)
"""
    return np.asarray(weights).flatten()


def vector_to_mat(vector_weights, mat_weights):
    """
    Transforms vector back to its original shape
    :param vector_weights: Weights in vector format
    :param mat_weights: initial weights
    :return: Weights in matrix format
    """
    """
    mat_weights_new = []

    for sol_idx in range(len(mat_weights)):
        start = 0
        end = 0
        temp = []
        for layer_idx in range(len(mat_weights[sol_idx])):
            end = end + mat_weights[sol_idx][layer_idx].size

            curr_vector = vector_weights[0][start:end]
            mat_layer_weights = np.reshape(curr_vector, newshape=mat_weights[sol_idx][layer_idx].shape)
            start = end
            temp.append(mat_layer_weights)
        temp = np.reshape(temp, newshape=mat_weights[sol_idx].shape)
        mat_weights_new.append(temp)

    return mat_weights_new
    """
    shape = np.asarray(mat_weights).shape
    np.asarray(vector_weights).reshape(shape)
    return vector_weights
