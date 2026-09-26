"""Streamlit page for propositional logic."""

import re
from itertools import product

import pandas as pd
import streamlit as st


KEYWORDS = {"AND", "OR", "NOT", "XOR"}


def normalize_expression(expression):
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
    tokens = re.findall(
        r"\(|\)|AND|OR|NOT|XOR|[A-Z_][A-Z0-9_]*",
        normalize_expression(expression),
    )
    if not tokens:
        raise ValueError("No valid expression was entered.")
    return tokens


def variables_in(expression):
    return sorted(
        {
            token
            for token in tokenize(expression)
            if token not in KEYWORDS and token not in {"(", ")"}
        }
    )


def parse_expression(expression):
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
        raise ValueError("The expression could not be parsed completely.")
    return tree


def evaluate_tree(node, values):
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


def truth_table(expression):
    variables = variables_in(expression)
    if not variables:
        raise ValueError("Use at least one variable, such as A AND B.")
    rows = []
    for combination in product([False, True], repeat=len(variables)):
        values = dict(zip(variables, combination))
        rows.append({**values, "Result": evaluate_tree(parse_expression(expression), values)})
    return pd.DataFrame(rows), variables


def classify(results):
    results = list(results)
    if all(results):
        return "Tautology"
    if not any(results):
        return "Contradiction"
    return "Contingency"


def implication(p, q):
    return (not p) or q


def results_for_operation(operation, a, b):
    return {
        "AND": a and b,
        "OR": a or b,
        "NAND": not (a and b),
        "NOR": not (a or b),
        "XOR": a != b,
        "XNOR": a == b,
    }[operation]


st.set_page_config(page_title="Logic", page_icon="¬", layout="wide")
st.title("Logic")
st.write("Explore Boolean operations, truth tables, and conditional propositions.")

st.header("Basic logical operations")
tabs = st.tabs(["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"])

for tab, operation in zip(tabs, ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"]):
    with tab:
        a = st.toggle("A", value=True, key=f"{operation}_a")
        if operation == "NOT":
            result = not a
            st.dataframe(pd.DataFrame([{"A": a, "Result": result}]), width="stretch")
        else:
            b = st.toggle("B", value=False, key=f"{operation}_b")
            results = {
                "AND": a and b,
                "OR": a or b,
                "NAND": not (a and b),
                "NOR": not (a or b),
                "XOR": a != b,
                "XNOR": a == b,
            }
            st.write("Result:", results[operation])
            rows = [
                {"A": x, "B": y, "Result": results_for_operation(operation, x, y)}
                for x, y in product([False, True], repeat=2)
            ]
            st.dataframe(pd.DataFrame(rows), width="stretch")

st.header("User-defined logical expression")
expression = st.text_input("Enter logical expression", "(A AND B) OR NOT C")

try:
    table, variables = truth_table(expression)
    st.write("Variables:", ", ".join(variables))
    st.dataframe(table, width="stretch")
    category = classify(table["Result"])
    if category == "Tautology":
        st.success("🟢 Tautology — always true.")
    elif category == "Contradiction":
        st.error("🔴 Contradiction — always false.")
    else:
        st.warning("🟡 Contingency — true in some cases and false in others.")
except ValueError as error:
    st.error(str(error))

st.header("Conditional propositions")
p = st.toggle("P", value=True, key="conditional_p")
q = st.toggle("Q", value=False, key="conditional_q")

conditional_rows = [
    {"Statement": "Original", "Formula": "P → Q", "Result": implication(p, q)},
    {"Statement": "Converse", "Formula": "Q → P", "Result": implication(q, p)},
    {"Statement": "Inverse", "Formula": "¬P → ¬Q", "Result": implication(not p, not q)},
    {"Statement": "Contrapositive", "Formula": "¬Q → ¬P", "Result": implication(not q, not p)},
]
st.dataframe(pd.DataFrame(conditional_rows), width="stretch")
st.info("An implication is false only when P is true and Q is false.")
