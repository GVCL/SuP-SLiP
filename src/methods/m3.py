""" 
M3: Annotation suggestion based on majority classification, Bit-flipping attack.
"""

import numpy as np
import random

"""
    @method bitflipping_attack
        Perform randomised bit-flipping on a binary list of numbers
    @param original_vector: Input binary list
    @param fraction: Fraction of points to flip 
"""
def bitflipping_attack(original_vector, fraction=0.10):
    new_vector = original_vector.copy()
    N = len(original_vector)
    
    # Get a list of indices to flip
    all_indices = list(range(N))
    selected_indices = random.sample(all_indices, int(fraction * N))
    
    # Propagate the changes to the new vector
    for idx in selected_indices:
        if original_vector[idx] == 0:
            new_vector[idx] = 1
        elif original_vector[idx] == 1:
            new_vector[idx] = 0
        else:
            new_vector[idx] = original_vector[idx]
    
    return new_vector

"""
    @method get_majority_output
        Perform majority classification to find the computed label for a masked point
    @param candiate_labels: List of binary candidate labels, the length of which is K
    @param eta: Majority confidence threshold (default: 0.5)
"""
def get_majority_output(candidate_labels, eta=0.5):    
    # Get outputs
    maj_sum = sum(candidate_labels)
    K = len(candidate_labels)
    
    # Threshold
    if float(maj_sum) >= eta * (K//2):
        return 1
    else:
        return 0
    

if __name__ == "__main__":
    # Set random seeds
    random.seed(42)
    np.random.seed(42)

    # Generate a sample binary vector
    vector_size=100
    original_input = np.random.randint(2, size=vector_size)

    # Choose first value as query value
    gt_label = original_input[0]

    # Perform bit-flipping
    K = 5
    random_candidate_labels = np.random.randint(2, size=K)
    flip_chance = 0.05
    polluted_candiate_labels = bitflipping_attack(
        original_vector=random_candidate_labels,
        fraction=flip_chance
    )

    # Emulate majority classification
    eta = 0.5
    comp_label = get_majority_output(polluted_candiate_labels, eta=0.5)
