
import numpy as np
from matplotlib import pyplot as plt


population_size = 1000

def calculate_all_probabilities(prior_prob, true_positive_rate, false_positive_rate):
    p_positive = (true_positive_rate * prior_prob) + (false_positive_rate * (1 - prior_prob))
    posterior_positive = (true_positive_rate * prior_prob) / p_positive
    p_negative = 1 - p_positive
    true_negative_rate = 1 - false_positive_rate
    posterior_negative = ((1 - true_positive_rate) * prior_prob) / p_negative
    posterior_healthy_negative = true_negative_rate * (1 - prior_prob) / p_negative
    return posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative

def calculate_gender_specific_probabilities(prior_prob, true_positive_rate, false_positive_rate, male_ratio):
    female_ratio = 1 - male_ratio
    posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative = calculate_all_probabilities(
        prior_prob, true_positive_rate, false_positive_rate)
    male_posterior_positive = posterior_positive * male_ratio
    female_posterior_positive = posterior_positive * female_ratio
    return male_posterior_positive, female_posterior_positive


prior_prob = 0.02
true_positive_rate = 0.8
false_positive_rate = 0.1


posterior_positive, p_positive, p_negative, posterior_negative, posterior_healthy_negative = calculate_all_probabilities(
    prior_prob, true_positive_rate, false_positive_rate)


male_ratio = 0.6
male_posterior_positive, female_posterior_positive = calculate_gender_specific_probabilities(
    prior_prob, true_positive_rate, false_positive_rate, male_ratio)


expected_counts_positive_test = np.array([posterior_positive, 1 - posterior_positive]) * population_size
expected_counts_test_result = np.array([p_positive, p_negative]) * population_size
expected_counts_negative_test = np.array([posterior_negative, posterior_healthy_negative]) * population_size
expected_counts_gender_specific = np.array([male_posterior_positive, female_posterior_positive]) * population_size


data = [expected_counts_positive_test, expected_counts_test_result, expected_counts_negative_test, expected_counts_gender_specific]
labels = ['Posterior Probability\nGiven Positive Test', 'Overall Test Result Probability',
          'Posterior Probability\nGiven Negative Test', 'Gender Specific Posterior Probability\nGiven Positive Test']
x_ticks_labels = ['P(D+|T+)', 'P(D-|T+)', 'P(T+)', 'P(T-)', 'P(D+|T-)', 'P(D-|T-)', 'Male', 'Female']


fig, axs = plt.subplots(1, 4, figsize=(24, 6))

for i, ax in enumerate(axs.flat):
    ax.bar(x_ticks_labels[i*2:i*2+2], data[i], color=['red', 'green'] if i < 3 else ['blue', 'pink'])
    ax.set_title(labels[i])
    ax.set_xticklabels(x_ticks_labels[i*2:i*2+2], rotation=45)
    ax.set_ylabel('Expected Count')


