"""Web UI for the calculator."""

from __future__ import annotations
from typing import Callable, Dict
from flask import Flask, render_template, request, jsonify
from calculator import add, subtract, multiply, divide, power, minimum, maximum


app = Flask(__name__)

OperationFunc = Callable[[float, float], float]

OPERATIONS: Dict[str, OperationFunc] = {
    "add": add,
    "sub": subtract,
    "mul": multiply,
    "div": divide,
    "pow": power,
    "max": maximum,
    "min": minimum,
}


@app.route("/", methods=["GET"])
def index() -> str:
    """
    Render the calculator form.
    """
    return render_template(
        "calculator.html",
        result=None,
        error=None,
        selected_op="add",
        a_value="",
        b_value="",
    )


@app.route("/calculate", methods=["POST"])
def calculate() -> str:
    """
    Handle form submission from the calculator UI.
    """
    op = request.form.get("operation", "add")
    a_raw = request.form.get("a", "")
    b_raw = request.form.get("b", "")

    error = None
    result = None

    try:
        a = float(a_raw)
        b = float(b_raw)
    except ValueError:
        error = "Both inputs must be numbers."
        a = b = 0.0  # dummy values, not used if error

    if error is None:
        func = OPERATIONS.get(op)
        if func is None:
            error = "Unknown operation."
        else:
            try:
                result = func(a, b)
            except ValueError as exc:
                # divide by zero
                error = str(exc)

    return render_template(
        "calculator.html",
        result=result,
        error=error,
        selected_op=op,
        a_value=a_raw,
        b_value=b_raw,
    )


@app.route("/api/calculate", methods=["GET"])
def api_calculate():
    """
    Simple HTTP API endpoint for JMeter etc.
    Example: /api/calculate?op=add&a=1&b=2
    """
    op = request.args.get("op", "add")
    a_raw = request.args.get("a", "")
    b_raw = request.args.get("b", "")

    try:
        a = float(a_raw)
        b = float(b_raw)
    except ValueError:
        return jsonify({"error": "Both a and b must be numbers."}), 400

    func = OPERATIONS.get(op)
    if func is None:
        return jsonify({"error": f"Unsupported operation '{op}'"}), 400

    try:
        result = func(a, b)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "operation": op,
            "a": a,
            "b": b,
            "result": result,
        }
    )


if __name__ == "__main__":
    # For local
    app.run(host="0.0.0.0", port=8000, debug=True)
