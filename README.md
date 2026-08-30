# Perceptron

A simple working model of a single neuron (Perceptron) built without external libraries, featuring an interactive HTML5 Canvas visualizer.

## Live Demo
[Try the Visualizer Live](https://rishabganesh2-bot.github.io/Perceptron/)

## Preview
![Perceptron Visualizer](<img width="607" height="665" alt="image" src="https://github.com/user-attachments/assets/8918fcdb-f1bb-4dfa-8a07-9baa72c95276" />
)

## What It Does
* **OR Logic Gate:** Learns to separate $(0,0) \to 0$ from $(0,1), (1,0), (1,1) \to 1$.
* **Zero Libraries:** Implements forward pass, Sigmoid activation, loss calculation, and gradient descent in pure math.
* **Interactive Visualizer:** Shows the linear decision boundary ($w_1x_1 + w_2x_2 + b = 0$) rotating and shifting in real time.

## How to Run

**Python Engine:**
```bash
python engine.py
