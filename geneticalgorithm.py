import numpy as np

from snake import Snake
import random
from typing import List, Tuple, Optional
from matrixoperations import *
from copy import deepcopy

'''
Genetic algorithm will find suitable weights to the neural network

Each snek has its own NN weights
'''


class GeneticAlgorithm:

    def mutate_snakes(self, dead_snakes: [Snake], top_n: int, children: int,
                      mutation_probability: float) -> (int, float):
        """
        Evolves the snakes
        :param dead_snakes: snakes of the previous generation
        :param top_n: Top n that will be used to crate new snakes
        :param children: number of children per pair of parents
        :param mutation_probability: Probability to a gene to be mutated
        :return: Nothing
        """
        print("evolving")
        ranked_snakes = sorted([(self.calculate_fitness(snek), snek) for snek in dead_snakes],
                               key=lambda tup: tup[0])

        ranked_snakes.reverse()
        parent_snakes = ranked_snakes[:top_n]
        child_snakes = ranked_snakes[top_n:top_n + children * top_n // 2]
        new_snakes = ranked_snakes[top_n + children * top_n // 2:]
        if len(parent_snakes) + len(child_snakes) + len(new_snakes) != len(dead_snakes):
            raise RuntimeError

        k = 0
        for i in range(0, top_n // 2, 2):
            _, parent1 = parent_snakes[i]
            _, parent2 = parent_snakes[i + 1]

            for j in range(children):
                self.crossover(parent1, parent2, child_snakes[j + k][1], mutation_probability)
                self.mutation_gaussian(child_snakes[j + k][1], 0.1)
                # print("Nüüd on ")
                # print(child_snakes[j+k][1].biases())
                # print()

            k += children

        self.create_new_snakes(new_snakes)

        # self.mutate(mutation_probability, dead_snakes)
        print("Longest snake " + str(ranked_snakes[0][0]))
        return ranked_snakes[0][0], sum([rank for rank, _ in ranked_snakes]) / len(ranked_snakes)

    def crossover(self, parent_snake1: Snake, parent_snake2: Snake, child: Snake, mutation_probability:float) -> Snake:
        """
        Creates new weights for two childs
        :param parent_snake1: First parent snake
        :param parent_snake2: Second parent snake
        :param child: Child that get some new genes
        :return: Nothing
        """

        parent_genes1 = mat_to_vector(parent_snake1.genes())
        parent_genes2 = mat_to_vector(parent_snake2.genes())
        child_genes = mat_to_vector(child.genes())
        # print("Using these parents")
        # print("parent 1")
        # print(parent_genes1)
        # print()
        # print("parent 2")
        # print(parent_genes2)

        # print()
        # print("childi oma")

        # print(child_genes)
        for i in range(len(parent_genes1[0])):
            m = 0
            if random.random() <mutation_probability:
                m = random.randint(-120,120)/1000


            choice = random.choice([1] * 45 + [2] * 45 + [3] * 10)
            if choice == 1:
                child_genes[0][i] = parent_genes2[0][i] + m
            if choice == 2:
                child_genes[0][i] = parent_genes1[0][i] + m
            else:
                child_genes[0][i] = random.uniform(-1, 1)
        # print("new genes")
        # print(child_genes)
        parent_biases1 = mat_to_vector(parent_snake1.biases())
        parent_biases2 = mat_to_vector(parent_snake2.biases())
        child_biases = mat_to_vector(child.biases())

        # print("parent 1 biases")
        # print(parent_biases1)
        # print()
        # print("parent 2")
        # print(parent_biases2)

        # print()
        # print("childi oma")

        # print(child_biases)

        for i in range(len(parent_biases1[0])):
            choice = random.choice([1] * 45 + [2] * 45 + [3] * 10)
            if choice == 1:
                child_biases[0][i] = parent_biases2[0][i]

            elif choice == 2:
                child_biases[0][i] = parent_biases1[0][i]

            else:
                child_biases[0][i] = random.uniform(-1, 1)
        # print()
        # print("New alue for biases:")
        # print(child_biases)
        child.setGenes(vector_to_mat(child_genes, parent_snake1.genes()),
                       vector_to_mat(child_biases, child.biases()))
        return child

    def crossover_uniform(self, parent_snake1: Snake, parent_snake2: Snake, child: Snake, mutationProp: float):
        """
        Creates new weights for two childs
        :param parent_snake1: First parent snake
        :param parent_snake2: Second parent snake
        :param child: Child that get some new genes
        :return: Nothing
        """
        eta = 0.3
        genes = mat_to_vector(parent_snake1.genes())
        random_parent = np.random.random((len(genes[0]),))

        gamma = np.empty((len(genes[0]),))
        gamma[random_parent <= 0.5] = (2 * random_parent[random_parent <= 0.5]) ** (
                1.0 / (eta + 1))  # First case of equation 9.11
        gamma[random_parent > 0.5] = (1.0 / (2.0 * (1.0 - random_parent[random_parent > 0.5]))) ** (1.0 / (eta + 1))
        parent2 = mat_to_vector(parent_snake1.genes())
        child_genes = 0.5 * ((1 + gamma) * genes[0] + (1 - gamma) * parent2[0])
        bias = mat_to_vector(parent_snake1.biases())
        eta = 0.3
        random_parent = np.random.random((len(bias[0]),))
        gamma = np.empty((len(bias[0]),))
        gamma[random_parent <= 0.5] = (2 * random_parent[random_parent <= 0.5]) ** (
                1.0 / (eta + 1))  # First case of equation 9.11
        gamma[random_parent > 0.5] = (1.0 / (2.0 * (1.0 - random_parent[random_parent > 0.5]))) ** (1.0 / (eta + 1))

        bias2 = mat_to_vector(parent_snake2.biases())
        child_biases = 0.5 * ((1 + gamma) * bias[0] + (1 - gamma) * bias2[0])

        child.setGenes(vector_to_mat([child_genes], parent_snake1.genes()),
                       vector_to_mat([child_biases], parent_snake1.biases()))

    def create_new_snakes(self, snakes: List[Tuple[int, Snake]]) -> None:

        for _, snake in snakes:
            genes = mat_to_vector(snake.genes())
            bias = mat_to_vector(snake.biases())

            for i in range(len(genes[0])):
                genes[0][i] = random.uniform(-1, 1)

            for i in range(len(bias[0])):
                bias[0][i] = random.uniform(-1, 1)
            snake.setGenes(vector_to_mat(genes, snake.genes()), vector_to_mat(bias, snake.biases()))

    def mutate_snakes1(self, top_n: int, keep_n: int, mutation_probability: float, population: List[Snake]) -> None:
        """
        :param population: Population of snakes
        :param top_n: top N snakes to create new childs
        :param keep_n: top N snakes to not modify
        :param mutation_probability: probability to a gene to not be mutated
        :return: Nothing
        """
        print("evolving")
        ranked_snakes = sorted([(self.calculate_fitness(snek), snek) for snek in population],
                               key=lambda tup: tup[0])
        ranked_snakes.reverse()
        snakes_to_keep = ranked_snakes[:keep_n]
        parent_snakes = ranked_snakes[:top_n]

        for _, parent_snake in parent_snakes:
            for i in range(int(len(population) / len(snakes_to_keep))):
                _, child = ranked_snakes[-1 - i]
                self.crossover2(parent_snake, child)

        self.mutate(mutation_probability, population)
        print("Pikim uss " + str(ranked_snakes[0][0]))

    def crossover1(self, parent_snake: Snake, child: Snake) -> None:
        """
        Uses parent snake to modify one child snake weights
        :param parent_snake: Parent snake
        :param child:  Child snake from parent snake
        :return:
        """
        x = np.random.normal(0, 1, size=660)
        parent_genes = mat_to_vector(parent_snake.genes())
        child_genes = parent_genes + ((x - x.mean()) / x.std() / 5)[random.randint(0, len(x)) - 1]

        parent_biases = mat_to_vector(parent_snake.biases())
        child_biases = parent_biases + ((x - x.mean()) / x.std() / 5)[random.randint(0, len(x)) - 1]

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

    def mutate(self, mutation_probability: float, population: List[Snake]) -> None:
        """
        Mutates all the snakes' brains in the population
        :param population: Population of snakes
        :param mutation_probability: Probability for a single gene to be mutated
        :return: Nothing
        """
        for snake in population:
            brain = snake.genes()
            vector_weights = mat_to_vector(brain)
            vector_bias = mat_to_vector(snake.biases())

            for i in range(len(vector_weights)):
                rand = random.random()
                if rand < mutation_probability:
                    vector_weights[i] = random.uniform(-1, 1)
                snake.setGenes(vector_to_mat(vector_weights, brain), snake.biases())

            for i in range(len(vector_bias) - 1):
                rand = random.random()
                if rand < mutation_probability:
                    vector_bias[i] = random.uniform(-1, 1)
                snake.setGenes(snake.genes(), vector_to_mat(vector_bias, snake.biases()))

    def mutation_gaussian(self, snake: Snake, prob_mutation: float,
                          scale: Optional[float] = None) -> None:

        # Determine which genes will be mutated
        weights = snake.genes()
        vw = mat_to_vector(weights)
        mutation_array_w = np.random.random((len(vw[0]),)) < prob_mutation
        # If mu and sigma are defined, create gaussian distribution around each one

        mutation_w = np.random.normal(size=(len(vw[0]),))

        bias = snake.biases()
        vb = mat_to_vector(bias)
        mutation_array_b = np.random.random((len(vb[0]),)) < prob_mutation
        mutation_b = np.random.normal(size=(len(vb[0]),))

        if scale:
            mutation_w[mutation_array_w] *= scale
            mutation_b[mutation_array_b] *= scale
        # Update
        vw[0][mutation_array_w] += mutation_w[mutation_array_w]
        vb[0][mutation_array_b] += mutation_b[mutation_array_b]

        mw = vector_to_mat(vw, snake.genes())
        mb = vector_to_mat(vb, snake.biases())

        snake.setGenes(mw, mb)

    def calculate_fitness(self, snek: Snake) -> int:
        """
        Calculates snek's fitness score
        :param snek: a snek instance
        :return: fitness score
        """
        return snek.size + round(snek.beenAlive/1000,3) - snek.deathPenalty
