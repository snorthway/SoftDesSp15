""" Exploring learning curves for classification of handwritten digits """

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import *
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA

data = load_digits()
num_trials = 15

# train_percentages looks like [5 5 5 5 5 10 10 10 10 15 15 15 etc]
train_percentages = [r for r in range(5, 95, 5) for n in range(num_trials)]
test_accuracies = []
averages = []
model = LogisticRegression(C=10**-10)  # still not totally sure what C does
# model2 = LogisticRegression()

for i in range(len(train_percentages)):
	for t in range(num_trials):
		x_train, x_test, y_train, y_test = train_test_split(data.data, data.target, train_size=0.01*train_percentages[i])
		model.fit(x_train, y_train)
	test_accuracies.append(model.score(x_test, y_test))
	# average the test accuracies for each train percentage
	if i != 0 and (i+1) % num_trials == 0:
		averages.append(sum(test_accuracies[i+1-num_trials:i+1])/num_trials)

plt.plot(train_percentages, test_accuracies, '.')
plt.plot(range(5, 95, 5), averages, 'r')
plt.xlabel('Percentage of Data Used for Training')
plt.ylabel('Accuracy on Test Set')
plt.show()

