
from flask import Flask, request, jsonify, send_file
app = Flask(__name__)
class LinearRegression:

    def __init__(self):
        self.slope = 0
        self.intercept = 0
        self.trained = False

    def fit(self, X, y):
        n = len(X)
        if n != len(y) or n < 2:
            raise ValueError("Provide at least two matching data points.")
        mean_x = sum(X) / n
        mean_y = sum(y) / n
        numerator = sum(
            (X[i] - mean_x) * (y[i] - mean_y)
            for i in range(n)
        )
        denominator = sum(
            (X[i] - mean_x) ** 2
            for i in range(n)
        )
        if denominator == 0:
            raise ValueError("All X values cannot be identical.")
        self.slope = numerator / denominator
        self.intercept = mean_y - self.slope * mean_x
        self.trained = True
    def predict(self, x):
        if not self.trained:
            raise ValueError("Model has not been trained.")
        return self.intercept + self.slope * x
    def score(self, X, y):
        predictions = [self.predict(x) for x in X]
        mean_y = sum(y) / len(y)
        ss_total = sum((actual - mean_y) ** 2 for actual in y)
        ss_residual = sum(
            (y[i] - predictions[i]) ** 2
            for i in range(len(y))
        )
        if ss_total == 0:
            return 1.0 if ss_residual == 0 else 0.0
        return 1 - (ss_residual / ss_total)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/fit", methods=["POST"])
def train():
    try:
        data = request.get_json()
        X = [float(value) for value in data["X"]]
        y = [float(value) for value in data["y"]]
        model = LinearRegression()
        model.fit(X, y)
        predictions = [model.predict(x) for x in X]
        return jsonify({
            "slope": model.slope,
            "intercept": model.intercept,
            "r2_score": model.score(X, y),
            "predictions": predictions,
            "status": "success"
        })
    except (ValueError, TypeError, KeyError) as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

if __name__ == "__main__":
    app.run(debug=True)
