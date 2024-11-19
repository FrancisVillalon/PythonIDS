import numpy as np
import matplotlib.pyplot as plt

# Parameters for the log-normal distribution
mean = 150
sigma = 0.75  # Standard deviation of the underlying normal distribution
size = 100_000  # Number of data points

# Generate a log-normal distribution
data = np.random.lognormal(mean=np.log(mean), sigma=sigma, size=size)

# Apply truncation to ensure values are between 0 and 1440
data = np.clip(data, 0, 1440)

# Plotting the truncated log-normal distribution
plt.hist(data, bins=100, density=True, alpha=0.6, color='b')

# Add labels and title
plt.title('Log-Normal Distribution (Truncated at Min = 0, Max = 1440)')
plt.xlabel('Value')
plt.ylabel('Density')

# Show
plt.show()