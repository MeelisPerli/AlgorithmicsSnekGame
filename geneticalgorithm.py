import numpy as np

from snake import Snake
import random
from typing import List, Tuple

'''
Genetic algorithm will find suitable weights to the neural network

Each snek has its own NN weights
'''


class GeneticAlgorithm:

    def __init__(self, population):
        self.population = population

    def mutate_snakes(self, top_n: int, keep_n: int, new_n: int, mutation_probability: float) -> None:
        """
        Evolves the snakes
        :param top_n: Top n that will be used to crate new snakes
        :param keep_n: Top n snakes that will not be modified
        :param mutation_probability: Probability to a gene to be mutated
        :return: Nothing
        """
        print("evolving")
        ranked_snakes = sorted([(self.calculate_fitness(snek), snek) for snek in self.population],
                               key=lambda tup: tup[0])
        ranked_snakes.reverse()
        snakes_to_keep = ranked_snakes[:keep_n]
        parent_snakes = ranked_snakes[:top_n]
        child_snakes = ranked_snakes[keep_n:len(ranked_snakes)-new_n]
        new_snakes = ranked_snakes[len(ranked_snakes)-keep_n-new_n:]
        i = 0
        j = 0

        for _ in range(int(top_n/2)):
            _, parent1 = parent_snakes[i]
            _, parent2 = parent_snakes[i+1]

            for _ in range(int(len(child_snakes)/len(parent_snakes))):

                _, child1 = child_snakes[j]
                _, child2 = child_snakes[j+1]
                j += 2
                self.crossover(parent1, child1, parent2, child2)
            i += 2

        self.create_new_snakes(new_snakes)

        self.mutate(mutation_probability)
        print("Longest snake " + str(ranked_snakes[0][0]))

    def crossover(self, parent_snake1: Snake,  child1: Snake, parent_snake2: Snake, child2: Snake) -> None:
        """
        Creates new weights for two childs
        :param parent_snake1: First parent snake
        :param child1: Child that gets some new genes
        :param parent_snake2: Second parent snake
        :param child2: Child that gets some new genes
        :return: Nothing
        """
        parent_genes1 = mat_to_vector(parent_snake1.genes())
        child_genes1 = mat_to_vector(child1.genes())
        parent_genes2 = mat_to_vector(parent_snake2.genes())
        child_genes2 = mat_to_vector(child2.genes())

        for i in range(len(parent_genes1[0])):

            choice = random.choice([1] * 45 + [2] * 45 + [3] * 10)
            if choice == 1:
                child_genes1[0][i] = parent_genes2[0][i]
                child_genes2[0][i] = parent_genes1[0][i]
            if choice == 2:
                child_genes1[0][i] = parent_genes1[0][i]
                child_genes2[0][i] = parent_genes2[0][i]
            else:
                child_genes1[0][i] = random.uniform(-1, 1)
                child_genes2[0][i] = random.uniform(-1, 1)

        parent_biases1 = mat_to_vector(parent_snake1.biases())
        child_biases1 = mat_to_vector(child1.biases())
        parent_biases2 = mat_to_vector(parent_snake2.biases())
        child_biases2 = mat_to_vector(child2.biases())

        for i in range(len(parent_biases1[0])):
            choice = random.choice([1] * 45 + [2] * 45 + [3] * 20)

            if choice == 1:
                child_biases1[0][i] = parent_biases2[0][i]
                child_biases2[0][i] = parent_biases2[0][i]
            elif choice == 2:
                child_biases1[0][i] = parent_biases1[0][i]
                child_biases2[0][i] = parent_biases2[0][i]
            else:
                child_biases1[0][i] = random.uniform(-1, 1)
                child_biases2[0][i] = random.uniform(-1, 1)

        child1.setGenes(vector_to_mat(child_genes1, parent_snake1.genes()),
                                   vector_to_mat(child_biases1, child1.biases()))
        child2.setGenes(vector_to_mat(child_genes2, parent_snake2.genes()),
                                   vector_to_mat(child_biases2, child2.biases()))

    def create_new_snakes(self, snakes: List[Tuple[int, Snake]]) -> None:

        for _, snake in snakes:
            genes = mat_to_vector(snake.genes())
            bias = mat_to_vector(snake.biases())

            for i in range(len(genes[0])):
                genes[0][i] = random.uniform(-1, 1)

            for i in range(len(bias[0])):
                bias[0][i] = random.uniform(-1, 1)
            snake.setGenes(vector_to_mat(genes, snake.genes()), vector_to_mat(bias, snake.biases()))




    def mutate_snakes1(self, top_n: int, keep_n: int, mutation_probability: float) -> None:
        """
        :param top_n: top N snakes to create new childs
        :param keep_n: top N snakes to not modify
        :param mutation_probability: probability to a gene to not be mutated
        :return: Nothing
        """
        print("evolving")
        ranked_snakes = sorted([(self.calculate_fitness(snek), snek) for snek in self.population],
                               key=lambda tup: tup[0])
        ranked_snakes.reverse()
        snakes_to_keep = ranked_snakes[:keep_n]
        parent_snakes = ranked_snakes[:top_n]

        for _, parent_snake in parent_snakes:
            for i in range(int(len(self.population)/len(snakes_to_keep))):
                _, child = ranked_snakes[-1-i]
                self.crossover2(parent_snake, child)

        self.mutate(mutation_probability)
        print("Pikim uss " + str(ranked_snakes[0][0]))



    def crossover1(self, parent_snake: Snake, child: Snake)-> None:
        """
        Uses parent snake to modify one child snake weights
        :param parent_snake: Parent snake
        :param child:  Child snake from parent snake
        :return:
        """
        x = np.random.normal(0, 1, size=660)
        parent_genes = mat_to_vector(parent_snake.genes())
        child_genes = parent_genes+((x-x.mean())/x.std()/5)[random.randint(0, len(x))-1]

        parent_biases = mat_to_vector(parent_snake.biases())
        child_biases = parent_biases+((x-x.mean())/x.std()/5)[random.randint(0, len(x))-1]

        child.setGenes(vector_to_mat(child_genes, parent_snake.genes()),
                                   vector_to_mat(child_biases, child.biases()))



    def crossover2(self, parent_snake: Snake, child: Snake) -> None:
        """
        Takes some genes from parent snake and gives them to a child
        :param parent_snake: Parent from who to take some genes
        :param child: Child, who gets some new genes
        :return: Nothing
        """
        parent_genes = mat_to_vector(parent_snake.genes())
        length = len(parent_genes[0])
        random_number1 = random.randint(0, length)
        random_number2 = random.randint(random_number1, length)

        child_genes = mat_to_vector(child.genes())
        for random_number1 in range(random_number2):

            child_genes[0][random_number1] = parent_genes[0][random_number1]

        parent_biases = mat_to_vector(parent_snake.biases())
        child_biases = mat_to_vector(parent_snake.biases())

        random_number1 = random.randint(0, len(parent_biases))
        random_number2 = random.randint(random_number1, len(parent_biases))
        for random_number1 in range(random_number2):

            child_biases[0][random_number1] = parent_biases[0][random_number1]

        child.setGenes(vector_to_mat(child_genes, parent_snake.genes()), child.biases())

    def mutate(self, mutation_probability: float) -> None:
        """
        Mutates all the snakes' brains in the population
        :param mutation_probability: Probability for a single gene to be mutated
        :return: Nothing
        """
        for snake in self.population:
            brain = snake.genes()
            vector_weights = mat_to_vector(brain)
            vector_bias = mat_to_vector(snake.biases())

            for i in range(len(vector_weights)):
                rand = random.random()
                if rand < mutation_probability:
                    vector_weights[i] = random.uniform(-1, 1)
                snake.setGenes(vector_to_mat(vector_weights, brain), snake.biases())

            for i in range(len(vector_bias)-1):
                rand = random.random()
                if rand < mutation_probability:

                    vector_bias[i] = random.uniform(-1, 1)
                snake.setGenes(snake.genes(),vector_to_mat(vector_bias, snake.biases()))

    def calculate_fitness(self, snek: Snake) -> int:
        """
        Calculates snek's fitness score
        :param snek: a snek instance
        :return: fitness score
        """
        return snek.size


def mat_to_vector(weights: List) -> np.ndarray:
    """
    Transform weights from list containing arrays to one vector
    :param weights: list containing weights
    :return: a numpy array
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


def vector_to_mat(vector_weights, mat_weights):
    """
    Transforms vector back to its original shape
    :param vector_weights: Weights in vector format
    :param mat_weights: initial weights
    :return: Weights in matrix format
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
