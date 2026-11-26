import math
import random

# Data
dataset = [
    ([0, 0], 0),
    ([0, 1], 1),
    ([1, 0], 1),
    ([1, 1], 1),
]

# Weights
w1 = random.uniform(-1, 1)
w2 = random.uniform(-1, 1)

# Bias
b = random.uniform(-1, 1)

# Rate
lr = 0.1


# Sigmoid
def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


# Derivative
def d_sigmoid(y):
    return y * (1.0 - y)


# Train
for epoch in range(2000):
    for (x1, x2), target in dataset:
        # Forward
        z = (x1 * w1) + (x2 * w2) + b
        pred = sigmoid(z)

        # Error
        err = target - pred

        # Gradient
        grad = -err * d_sigmoid(pred)

        # Update
        w1 -= lr * grad * x1
        w2 -= lr * grad * x2
        b -= lr * grad * 1.0

# Predict
for (x1, x2), target in dataset:
    out = sigmoid((x1 * w1) + (x2 * w2) + b)
    print(f"Input: [{x1}, {x2}] -> Target: {target} | Pred: {out:.4f}")