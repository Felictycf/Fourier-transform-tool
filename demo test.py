import matplotlib.pyplot as plt

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


sizes1 = [posterior_positive, 1 - posterior_positive]
sizes2 = [p_positive, p_negative]
sizes3 = [posterior_negative, posterior_healthy_negative]
sizes_gender_specific = [male_posterior_positive, female_posterior_positive]

labels1 = ['P(D+|T+)', 'P(D-|T+)']
labels2 = ['P(T+)', 'P(T-)']
labels3 = ['P(D+|T-)', 'P(D-|T-)']
labels_gender_specific = ['Male P(D+|T+)', 'Female P(D+|T+)']

colors1 = ['lightcoral', 'lightskyblue']
colors2 = ['gold', 'lightgreen']
colors3 = ['lightpink', 'lightblue']
colors_gender_specific = ['blue', 'pink']

explode = (0.1, 0)


fig, ax = plt.subplots(1, 3, figsize=(24, 6))  # 1行4列布局


ax[0].pie(sizes1, explode=explode, labels=labels1, colors=colors1, autopct='%1.1f%%', shadow=True, startangle=140)
ax[1].pie(sizes2, explode=explode, labels=labels2, colors=colors2, autopct='%1.1f%%', shadow=True, startangle=140)
ax[2].pie(sizes3, explode=explode, labels=labels3, colors=colors3, autopct='%1.1f%%', shadow=True, startangle=140)

ax[0].set_title('Posterior Probability Given Positive Test')
ax[1].set_title('Overall Test Result Probability')
ax[2].set_title('Posterior Probability Given Negative Test')

plt.axis('equal')
plt.show()
