"""Streamlit page for propositional logic."""

import re
from itertools import product

import pandas as pd
import streamlit as st


KEYWORDS = {"AND", "OR", "NOT", "XOR"}


def normalize_expression(expression):
    """Convert supported symbols into readable logical keywords."""
    replacements = {
        "∧": " AND ",
        "∨": " OR ",
        "¬": " NOT ",
        "~": " NOT ",
        "⊕": " XOR ",
    }

    result = str(expression).upper().strip()

    for old, new in replacements.items():
        result = result.replace(old, new)

    return " ".join(result.split())


def tokenize(expression):
    """Convert an expression into safe parser tokens."""
    normalized = normalize_expression(expression)

    tokens = re.findall(
        r"\(|\)|AND|OR|NOT|XOR|[A-Z_][A-Z0-9_]*",
        normalized,
    )

    if not tokens:
        raise ValueError("No valid logical expression was entered.")

    return tokens


def variables_in(expression):
    """Return variables used in an expression."""
    return sorted(
        {
            token
            for token in tokenize(expression)
            if token not in KEYWORDS
            and token not in {"(", ")"}
        }
    )


def parse_expression(expression):
    """
    Parse an expression without using eval().

    Operator precedence:
    1. NOT
    2. XOR
    3. AND
    4. OR
    """
    tokens = tokenize(expression)
    position = 0

    def parse_or():
        nonlocal position

        node = parse_and()

        while position < len(tokens) and tokens[position] == "OR":
            position += 1
            node = ("OR", node, parse_and())

        return node

    def parse_and():
        nonlocal position

        node = parse_xor()

        while position < len(tokens) and tokens[position] == "AND":
            position += 1
            node = ("AND", node, parse_xor())

        return node

    def parse_xor():
        nonlocal position

        node = parse_not()

        while position < len(tokens) and tokens[position] == "XOR":
            position += 1
            node = ("XOR", node, parse_not())

        return node

    def parse_not():
        nonlocal position

        if position < len(tokens) and tokens[position] == "NOT":
            position += 1
            return ("NOT", parse_not())

        return parse_primary()

    def parse_primary():
        nonlocal position

        if position >= len(tokens):
            raise ValueError("Unexpected end of expression.")

        token = tokens[position]

        if token == "(":
            position += 1
            node = parse_or()

            if position >= len(tokens) or tokens[position] != ")":
                raise ValueError("Missing closing parenthesis.")

            position += 1
            return node

        if token not in KEYWORDS and token != ")":
            position += 1
            return ("VARIABLE", token)

        raise ValueError(f"Unexpected token: {token}")

    tree = parse_or()

    if position != len(tokens):
        raise ValueError(
            "The expression could not be parsed completely."
        )

    return tree


def evaluate_tree(node, values):
    """Evaluate a parsed logical expression."""
    operation = node[0]

    if operation == "VARIABLE":
        return bool(values[node[1]])

    if operation == "NOT":
        return not evaluate_tree(node[1], values)

    left = evaluate_tree(node[1], values)
    right = evaluate_tree(node[2], values)

    if operation == "AND":
        return left and right

    if operation == "OR":
        return left or right

    if operation == "XOR":
        return left != right

    raise ValueError(f"Unknown operation: {operation}")


def evaluate_expression(expression, values):
    """Parse and evaluate a logical expression."""
    tree = parse_expression(expression)
    return evaluate_tree(tree, values)


def classify(results):
    """Classify truth-table results."""
    results = list(results)

    if all(results):
        return "Tautology"

    if not any(results):
        return "Contradiction"

    return "Contingency"


def results_for_operation(operation, a, b):
    """Calculate a binary logical operation."""
    operations = {
        "AND": a and b,
        "OR": a or b,
        "NAND": not (a and b),
        "NOR": not (a or b),
        "XOR": a != b,
        "XNOR": a == b,
    }

    if operation not in operations:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    return operations[operation]


def implication(p, q):
    """Evaluate P → Q."""
    return (not p) or q


def as_bit(value):
    """Represent a logical value as 1 or 0 for table display."""
    return int(bool(value))


def truth_table(expression):
    """Generate the complete truth table for an expression."""
    variables = variables_in(expression)

    if not variables:
        raise ValueError(
            "Use at least one variable, such as A AND B."
        )

    rows = []

    for combination in product([False, True], repeat=len(variables)):
        values = dict(zip(variables, combination))

        row = {
            variable: as_bit(value)
            for variable, value in values.items()
        }

        row["Result"] = as_bit(
            evaluate_expression(
                expression,
                values,
            )
        )

        rows.append(row)

    return pd.DataFrame(rows), variables


def create_basic_truth_table(operation):
    """Create a truth table for a basic logical operation."""
    if operation == "NOT":
        return pd.DataFrame(
            [
                {
                    "A": as_bit(value),
                    "Result": as_bit(not value),
                }
                for value in [False, True]
            ]
        )

    rows = []

    for a, b in product([False, True], repeat=2):
        rows.append(
            {
                "A": as_bit(a),
                "B": as_bit(b),
                "Result": as_bit(
                    results_for_operation(
                        operation,
                        a,
                        b,
                    )
                ),
            }
        )

    return pd.DataFrame(rows)


# Page configuration
st.set_page_config(
    page_title="Logic",
    page_icon="¬",
    layout="wide",
)

st.title("Logic")

st.write(
    "Explore Boolean operations, truth tables, "
    "logical expressions, and conditional propositions."
)


# Basic logical operations
st.header("Basic logical operations")

operation_names = [
    "AND",
    "OR",
    "NOT",
    "NAND",
    "NOR",
    "XOR",
    "XNOR",
]

tabs = st.tabs(operation_names)

for tab, operation in zip(tabs, operation_names):
    with tab:
        st.subheader(operation)

        if operation == "NOT":
            a = st.toggle(
                "A",
                value=True,
                key="not_a",
            )

            result = not a

            st.write("Result:", as_bit(result))

            selected_result = pd.DataFrame(
                [
                    {
                        "A": as_bit(a),
                        "Result": as_bit(result),
                    }
                ]
            )

            st.dataframe(
                selected_result,
                width="stretch",
            )

        else:
            left_column, right_column = st.columns(2)

            with left_column:
                a = st.toggle(
                    "A",
                    value=True,
                    key=f"{operation}_a",
                )

            with right_column:
                b = st.toggle(
                    "B",
                    value=False,
                    key=f"{operation}_b",
                )

            result = results_for_operation(
                operation,
                a,
                b,
            )

            st.write("Result:", as_bit(result))

            selected_result = pd.DataFrame(
                [
                    {
                        "A": as_bit(a),
                        "B": as_bit(b),
                        "Result": as_bit(result),
                    }
                ]
            )

            st.dataframe(
                selected_result,
                width="stretch",
            )

        st.write("Complete truth table")

        st.dataframe(
            create_basic_truth_table(operation),
            width="stretch",
        )


# User-defined logical expression
st.header("User-defined logical expression")

st.write(
    "Supported operators: AND, OR, NOT, XOR, and parentheses."
)

expression = st.text_input(
    "Enter logical expression",
    value="(A AND B) OR NOT C",
    help="Example: (A AND B) OR NOT C",
)

try:
    table, variables = truth_table(expression)

    st.write(
        "Variables:",
        ", ".join(variables),
    )

    st.dataframe(
        table,
        width="stretch",
    )

    category = classify(table["Result"])

    if category == "Tautology":
        st.success(
            "🟢 Tautology — the expression is always true."
        )

    elif category == "Contradiction":
        st.error(
            "🔴 Contradiction — the expression is always false."
        )

    else:
        st.warning(
            "🟡 Contingency — the expression is true in "
            "some cases and false in others."
        )

except ValueError as error:
    st.error(f"Invalid expression: {error}")


# Conditional propositions
st.header("Conditional propositions")

st.write(
    "For P → Q, generate the original, converse, "
    "inverse, and contrapositive."
)

left_column, right_column = st.columns(2)

with left_column:
    p = st.toggle(
        "P",
        value=True,
        key="conditional_p",
    )

with right_column:
    q = st.toggle(
        "Q",
        value=False,
        key="conditional_q",
    )

conditional_rows = [
    {
        "Statement": "Original",
        "Formula": "P → Q",
        "Result": as_bit(implication(p, q)),
    },
    {
        "Statement": "Converse",
        "Formula": "Q → P",
        "Result": as_bit(implication(q, p)),
    },
    {
        "Statement": "Inverse",
        "Formula": "¬P → ¬Q",
        "Result": as_bit(implication(not p, not q)),
    },
    {
        "Statement": "Contrapositive",
        "Formula": "¬Q → ¬P",
        "Result": as_bit(implication(not q, not p)),
    },
]

st.dataframe(
    pd.DataFrame(conditional_rows),
    width="stretch",
)

st.info(
    "An implication is false only when P is true and Q is false. "
    "The original statement and its contrapositive have the same "
    "truth value."
)