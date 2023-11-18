import random
import pandas as pd
from deap import base, creator, tools, algorithms
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
import numpy as np

# Load your dataset
df = pd.read_csv('train_data.csv')  # Adjust the path to your dataset

# Define your heuristic evaluation function with cross-validation
def heuristic_evaluation(individual):
    # Decode individual into a set of thresholds
    jitter_rel_threshold, shim_loc_threshold, shim_db_threshold, hnr_threshold, rpde_threshold, dfa_threshold, ppe_threshold = individual

    # Define the heuristic function using these thresholds
    def apply_heuristic(row):
        jitter_condition = row['Jitter_rel'] > jitter_rel_threshold
        shim_condition = row['Shim_loc'] > shim_loc_threshold or row['Shim_dB'] > shim_db_threshold
        hnr_condition = row['HNR05'] < hnr_threshold
        rpde_condition = row['RPDE'] > rpde_threshold
        dfa_condition = row['DFA'] > dfa_threshold
        ppe_condition = row['PPE'] > ppe_threshold

        if jitter_condition and shim_condition and (hnr_condition or rpde_condition or dfa_condition or ppe_condition):
            return 1  # Indicative of Parkinson's
        else:
            return 0  # Not indicative of Parkinson's

    # Cross-validation
    kf = KFold(n_splits=5)  # 5-fold cross-validation
    accuracies = []
    for train_index, test_index in kf.split(df):
        train, test = df.iloc[train_index], df.iloc[test_index]
        predictions = test.apply(apply_heuristic, axis=1)
        accuracy = accuracy_score(test['Status'], predictions)
        accuracies.append(accuracy)

    return np.mean(accuracies),

# Set up the genetic algorithm
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 1)  # Adjust range if necessary
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=7)  # n=7 for the number of thresholds
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", heuristic_evaluation)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)  # Adjust mutation probability
toolbox.register("select", tools.selTournament, tournsize=3)

def optimizeHeuristic():
    population = toolbox.population(n=200)  # Increased population size
    ngen = 200  # Increased number of generations
    cxpb = 0.8  # Higher crossover probability
    mutpb = 0.4  # Higher mutation probability

    algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, verbose=True)

    best_ind = tools.selBest(population, 1)[0]
    return best_ind

# Run the optimization
best_heuristic = optimizeHeuristic()
print(f"Best Heuristic Thresholds: {best_heuristic}")

# Apply the best heuristic to the entire dataset
def ga_optimized_parkinsons_heuristic(row, thresholds):
    jitter_rel_threshold, shim_loc_threshold, shim_db_threshold, hnr_threshold, rpde_threshold, dfa_threshold, ppe_threshold = thresholds

    jitter_condition = row['Jitter_rel'] > jitter_rel_threshold
    shim_condition = row['Shim_loc'] > shim_loc_threshold or row['Shim_dB'] > shim_db_threshold
    hnr_condition = row['HNR05'] < hnr_threshold
    rpde_condition = row['RPDE'] > rpde_threshold
    dfa_condition = row['DFA'] > dfa_threshold
    ppe_condition = row['PPE'] > ppe_threshold

    if jitter_condition and shim_condition and (hnr_condition or rpde_condition or dfa_condition or ppe_condition):
        return 1  # Indicative of Parkinson's
    else:
        return 0  # Not indicative of Parkinson's

df['Predicted_GA'] = df.apply(ga_optimized_parkinsons_heuristic, thresholds=best_heuristic, axis=1)
accuracy_ga = accuracy_score(df['Status'], df['Predicted_GA'])
print(f"Accuracy with GA Optimized Heuristic: {accuracy_ga}")