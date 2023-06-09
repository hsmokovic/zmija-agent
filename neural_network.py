from snake_app import config, actions, max_index
import numpy as np
import random

neural = {
    'architecture': [6, 20, 3],
    'mutation_prob': 0.1,
    'K': 0.2,
    'elitism': 5,
    'generation_size': 50
}

class NeuralNetwork:
    def __init__(self, weights=None, bias=None):
        self.fitness = 0

        if weights is None and bias is None:
            self.weights = []
            self.bias = []
            # inicijalno stvaranje weightova za jedinku
            for i in range(len(neural['architecture']) - 1):
                input_size = neural['architecture'][i]
                output_size = neural['architecture'][i + 1]
                # parametri su: loc(mean)=0, scale(std_deviation)=0.01, size
                norm1 = np.random.normal(0, 0.1, (output_size, input_size))
                self.weights.append(norm1)

            for i in range(1, len(neural['architecture'])):
                layer_size = neural['architecture'][i]
                norm2 = np.random.normal(0, 0.1, layer_size)
                self.bias.append(norm2)
        else:
            self.weights = weights
            self.bias = bias

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def forwad_propagation(self, network_input):
        output = network_input
        for i in range(len(self.weights)):
            weights = self.weights[i]
            bias = self.bias[i]
            output = self.sigmoid(np.dot(output, weights.T) + bias)
        ind = max_index(output)
        action = actions[ind]
        return action

    # funkcija koja izvršava mutaciju jedinke
    def mutate(self):
        # mutacija težina
        for i in range(len(self.weights)):
            weight = self.weights[i]
            for j in range(weight.shape[0]):
                for k in range(weight.shape[1]):
                    # ako je random vr. manja od zadane vjerojatnosti mutation_prob -> mutacija
                    if np.random.uniform(0, 1) < neural['mutation_prob']:
                        # težinama se pribraja Gaussov šum
                        self.weights[i][j][k] += np.random.normal(0, neural['K'])

        # mutacija biasa
        for i in range(len(self.bias)):
            bias = self.weights[i]
            for j in range(bias.shape[0]):
                # ako je random vr. manja od zadane vjerojatnosti mutation_prob -> mutacija
                if np.random.uniform(0, 1) < neural['mutation_prob']:
                    # biasima se pribraja Gaussov šum
                    self.bias[i][j] += np.random.normal(0, neural['K'])


# funckija koja vraća listu najboljih jedinki
# koje se nepromijenjene prenose u iduću generaciju
def elitism(population):
    return population[0:neural['elitism']]


# troturnirska selekcija, od 3 jedinke vraća se ona s najvećim fitnessom
def selection(population):
    # generira se lista 3 nasumična indeka jedinki u populaciji
    selected = random.sample(range(0, neural['generation_size']), 3)
    # kao trenutno najbolja izabire se prva
    best = population[selected[0]]
    # iteriranje po listi nasumičnih indeksa
    for ind in selected:
        # ako je neka od ostalih jedinki iz turnira bolja od najbolje, ona postaje najbolja
        if population[ind].fitness > best.fitness:
            best = population[ind]
    return best


# funkcija uniformnog križanja kojoj predajemo 2 roditelja kao argumente
def crossover(parent1, parent2):
    w, b = [], []
    # određivanje težina djeteta
    for i in range(len(parent1.weights)):
        parent1_w = parent1.weights[i]
        parent2_w = parent2.weights[i]
        shape = parent1_w.shape
        # inicijalizacija matrice težina na nule
        child_w = np.zeros(shape)
        for j in range(shape[0]):
            for k in range(shape[1]):
                # ako je random manje od 0.5, dijete preuzima težinu parenta1
                if np.random.uniform(0, 1) < 0.5:
                    child_w[j, k] = parent1_w[j, k]
                # inače dobiva težinu parenta2
                else:
                    child_w[j, k] = parent2_w[j, k]
        w.append(child_w)

    # određivanje biasa djeteta
    for i in range(len(parent1.bias)):
        parent1_b = parent1.bias[i]
        parent2_b = parent2.bias[i]
        shape = parent1_b.shape
        # inicijalizacija bias vektora na nule
        child_vector = np.zeros(shape)
        for j in range(shape[0]):
            # ako je random manje od 0.5, dijete preuzima bias parenta1
            if np.random.uniform(0, 1) < 0.5:
                child_vector[j] = parent1_b[j]
            # inače dobiva bias parenta2
            else:
                child_vector[j] = parent2_b[j]
        b.append(child_vector)

    return NeuralNetwork(w, b)
