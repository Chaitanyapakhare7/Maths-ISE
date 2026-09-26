"""Streamlit page for relations, closures, and Hasse diagrams."""

import re

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st


def parse_scalar(value):
    value = value.strip()
    try:
        return float(value) if "." in value else int(value)
    except ValueError:
        return value


def parse_set_input(text):
    if not text or not text.strip():
        return set()
    text = text.replace("{", " ").replace("}", " ")
    return {
        parse_scalar(token)
        for token in re.split(r"[\s,;]+", text)
        if token.strip()
    }


def parse_relation_input(text, domain, codomain=None):
    if not text or not text.strip():
        return set()
    if "=" in text:
        text = text.split("=", 1)[1]
    pairs = re.findall(r"\(([^()]*)\)", text)
    if not pairs:
        raise ValueError("Enter pairs such as (1,2),(2,3).")

    target = domain if codomain is None else codomain
    relation = set()
    for pair in pairs:
        parts = [part.strip() for part in pair.split(",")]
        if len(parts) != 2:
            raise ValueError(f"Invalid ordered pair: ({pair}).")
        first, second = map(parse_scalar, parts)
        if first not in domain or second not in target:
            raise ValueError(f"({first}, {second}) is outside the selected sets.")
        relation.add((first, second))
    return relation


def relation_domain(relation):
    return {first for first, _ in relation}


def relation_range(relation):
    return {second for _, second in relation}


def is_reflexive(relation, domain):
    return all((value, value) in relation for value in domain)


def is_symmetric(relation):
    return all((second, first) in relation for first, second in relation)


def is_antisymmetric(relation):
    return all(
        first == second or (second, first) not in relation
        for first, second in relation
    )


def is_transitive(relation):
    values = {value for pair in relation for value in pair}
    return all(
        (first, middle) not in relation
        or (middle, last) not in relation
        or (first, last) in relation
        for first in values
        for middle in values
        for last in values
    )


def transitive_closure(relation, domain):
    closure = set(relation)
    changed = True
    while changed:
        changed = False
        for first in domain:
            for middle in domain:
                for last in domain:
                    if (
                        (first, middle) in closure
                        and (middle, last) in closure
                        and (first, last) not in closure
                    ):
                        closure.add((first, last))
                        changed = True
    return closure


def hasse_edges(relation, domain):
    edges = {(first, second) for first, second in relation if first != second}
    return {
        (first, second)
        for first, second in edges
        if not any(
            (first, middle) in edges and (middle, second) in edges
            for middle in domain
            if middle not in {first, second}
        )
    }


def relation_diagram(domain, codomain, relation):
    figure, axis = plt.subplots(figsize=(9, 5))
    left = sorted(domain, key=str)
    right = sorted(codomain, key=str)
    left_y = {value: 1.8 - index * 0.7 for index, value in enumerate(left)}
    right_y = {value: 1.8 - index * 0.7 for index, value in enumerate(right)}

    axis.add_patch(plt.Ellipse((0, 0), 2.5, 5, fill=False, linewidth=2))
    axis.add_patch(plt.Ellipse((6, 0), 2.5, 5, fill=False, linewidth=2))
    axis.text(0, 2.8, "Domain", ha="center")
    axis.text(6, 2.8, "Codomain", ha="center")

    for value, y in left_y.items():
        axis.text(0, y, str(value), ha="center")
    for value, y in right_y.items():
        axis.text(6, y, str(value), ha="center")
    for first, second in relation:
        axis.annotate(
            "",
            xy=(4.8, right_y[second]),
            xytext=(1.2, left_y[first]),
            arrowprops={"arrowstyle": "->", "color": "darkorange", "linewidth": 2},
        )

    axis.set_xlim(-1.5, 7.5)
    axis.set_ylim(-2.5, 3.5)
    axis.axis("off")
    return figure


def hasse_diagram(relation, domain):
    graph = nx.DiGraph()
    graph.add_nodes_from(domain)
    graph.add_edges_from(hasse_edges(relation, domain))
    figure, axis = plt.subplots(figsize=(7, 5))
    nx.draw_networkx(
        graph,
        nx.spring_layout(graph, seed=42),
        ax=axis,
        with_labels=True,
        node_color="lightblue",
        edge_color="darkgreen",
        node_size=1400,
    )
    axis.set_title("Hasse diagram")
    axis.axis("off")
    return figure


st.set_page_config(page_title="Relations", page_icon="↔", layout="wide")
st.title("Relations")
st.write("Analyze relation diagrams, properties, transitive closure, and partial orders.")

mode = st.radio("Relation type", ["One set: A to A", "Two sets: A to B"])
domain = parse_set_input(st.text_input("Set A", "1,2,3"))

if mode.startswith("Two"):
    codomain = parse_set_input(st.text_input("Set B", "2,3,4"))
else:
    codomain = domain

relation_text = st.text_area("Relation R", "(1,2),(2,3),(3,3)")

try:
    relation = parse_relation_input(
        relation_text,
        domain,
        None if mode.startswith("One") else codomain,
    )
except ValueError as error:
    st.error(str(error))
    st.stop()

st.header("Relation diagram")
st.pyplot(relation_diagram(domain, codomain, relation), width="stretch")

st.header("Domain, range, and codomain")
st.dataframe(
    pd.DataFrame(
        [
            {
                "Relation": sorted(relation, key=str),
                "Domain": sorted(relation_domain(relation), key=str),
                "Codomain": sorted(codomain, key=str),
                "Range": sorted(relation_range(relation), key=str),
            }
        ]
    ),
    width="stretch",
)

st.header("Relation properties")
properties = {
    "Reflexive": is_reflexive(relation, domain),
    "Symmetric": is_symmetric(relation),
    "Antisymmetric": is_antisymmetric(relation),
    "Transitive": is_transitive(relation),
}
for name, value in properties.items():
    if value:
        st.success(f"✓ {name}: satisfies the property")
    else:
        st.error(f"✗ {name}: does not satisfy the property")

st.header("Transitive closure")
closure = transitive_closure(relation, domain)
st.write("Original relation:", sorted(relation, key=str))
st.write("Transitive closure R⁺:", sorted(closure, key=str))

st.header("Hasse diagram")
partial_order = (
    properties["Reflexive"]
    and properties["Antisymmetric"]
    and properties["Transitive"]
)
if partial_order:
    st.success("This relation is a partial order.")
    st.pyplot(hasse_diagram(relation, domain), width="stretch")
else:
    failed = [name for name in ["Reflexive", "Antisymmetric", "Transitive"] if not properties[name]]
    st.warning("This relation is not a partial order. Failed: " + ", ".join(failed))
