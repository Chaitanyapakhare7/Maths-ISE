"""Streamlit page for exploring sets.

Optional dependency for Venn diagrams:
    pip install matplotlib-venn
"""

import re

import matplotlib.pyplot as plt
import streamlit as st
from theme import apply_theme

try:
    from matplotlib_venn import venn2, venn3
except ImportError:
    venn2 = venn3 = None


def parse_set_input(text):
    """Parse comma-separated numbers or words into a set."""
    if not text or not text.strip():
        return set()

    text = text.replace("{", "").replace("}", "")
    values = []
    for token in re.split(r"[\s,;]+", text):
        token = token.strip()
        if not token:
            continue
        try:
            values.append(float(token) if "." in token else int(token))
        except ValueError:
            values.append(token)
    return set(values)


def union(*sets):
    result = set()
    for current in sets:
        result |= set(current)
    return result


def intersection(*sets):
    if not sets:
        return set()
    result = set(sets[0])
    for current in sets[1:]:
        result &= set(current)
    return result


def calculate_operation(sets, operation):
    if len(sets) == 2:
        a, b = sets
        operations = {
            "A ∪ B": (union(a, b), "Elements in A or B."),
            "A ∩ B": (intersection(a, b), "Elements present in both A and B."),
            "A − B": (a - b, "Elements in A but not in B."),
            "B − A": (b - a, "Elements in B but not in A."),
            "A Δ B": (a ^ b, "Elements in exactly one of A and B."),
            "A'": (union(a, b) - a, "Elements in the chosen universe that are not in A."),
        }
        return operations[operation]

    if operation.endswith("union"):
        return union(*sets), "Elements present in at least one selected set."
    return intersection(*sets), "Elements common to every selected set."


def operation_concept(operation, sets, result):
    """Explain the selected operation in set-builder language."""
    set_names = ", ".join(
        f"{label} = {{{', '.join(map(str, sorted(values, key=str)))}}}"
        for label, values in zip(["A", "B", "C", "D", "E"], sets)
    )

    concepts = {
        "A ∪ B": (
            "Union combines both sets. An element belongs to A ∪ B when it "
            "appears in A, in B, or in both.",
            "A ∪ B = {x | x ∈ A or x ∈ B}",
            "Think of this as putting both collections into one collection "
            "and removing duplicates.",
        ),
        "A ∩ B": (
            "Intersection keeps only the shared elements. An element belongs "
            "to A ∩ B when it appears in both A and B.",
            "A ∩ B = {x | x ∈ A and x ∈ B}",
            "The overlap in the Venn diagram is the part that remains.",
        ),
        "A − B": (
            "Difference removes every element of B from A. The order matters: "
            "A − B is not generally the same as B − A.",
            "A − B = {x | x ∈ A and x ∉ B}",
            "Read it as 'A without the elements shared with B.'",
        ),
        "B − A": (
            "Difference removes every element of A from B. The order matters: "
            "B − A is not generally the same as A − B.",
            "B − A = {x | x ∈ B and x ∉ A}",
            "This selects the part of B outside the overlap.",
        ),
        "A Δ B": (
            "Symmetric difference keeps elements that belong to exactly one "
            "of the two sets, but not to both.",
            "A Δ B = (A − B) ∪ (B − A)",
            "The shared middle is excluded; only the two outer regions remain.",
        ),
        "A'": (
            "The complement of A contains the elements in the chosen universe "
            "that are not in A.",
            "A' = U − A, where U = A ∪ B",
            "Here the app uses A ∪ B as the working universe.",
        ),
    }

    if operation in concepts:
        meaning, notation, intuition = concepts[operation]
    elif operation.endswith("union"):
        meaning = (
            "The union collects every element found in at least one of the "
            "selected sets."
        )
        notation = f"{operation} = {{{', '.join(map(str, sorted(result, key=str)))}}}"
        intuition = "The Venn diagram highlights all occupied regions."
    else:
        meaning = (
            "The intersection keeps only elements shared by every selected "
            "set."
        )
        notation = f"{operation} = {{{', '.join(map(str, sorted(result, key=str)))}}}"
        intuition = "The Venn diagram highlights the common overlap."

    return set_names, meaning, notation, intuition


def venn_figure(sets, labels):
    figure, axis = plt.subplots(figsize=(4.4, 3.4))
    figure.patch.set_facecolor("#fff9f5")
    axis.set_facecolor("#fff9f5")

    if len(sets) == 2 and venn2 is not None:
        a, b = sets
        diagram = venn2(
            (len(a - b), len(b - a), len(a & b)),
            set_labels=labels,
            ax=axis,
        )
        if diagram:
            for patch, color in zip(
                diagram.patches,
                ["#c4b5fd", "#a5f3fc", "#f9a8d4"],
            ):
                if patch:
                    patch.set_color(color)
                    patch.set_alpha(0.78)
    elif len(sets) == 3 and venn3 is not None:
        a, b, c = sets
        diagram = venn3(
            (
                len(a - (b | c)),
                len(b - (a | c)),
                len(c - (a | b)),
                len((a & b) - c),
                len((a & c) - b),
                len((b & c) - a),
                len(a & b & c),
            ),
            set_labels=labels,
            ax=axis,
        )
        if diagram:
            for patch, color in zip(
                diagram.patches,
                [
                    "#c4b5fd",
                    "#a5f3fc",
                    "#f9a8d4",
                    "#99f6e4",
                    "#fde68a",
                    "#fdba74",
                    "#ddd6fe",
                ],
            ):
                if patch:
                    patch.set_color(color)
                    patch.set_alpha(0.78)
    else:
        axis.text(
            0.5,
            0.5,
            "Install matplotlib-venn for a Venn diagram.\n"
            "Venn diagrams are supported for two or three sets.",
            ha="center",
            va="center",
        )
    axis.set_title(
        "Venn diagram",
        color="#4c1d95",
        fontweight="bold",
        fontsize=11,
        pad=8,
    )
    figure.tight_layout(pad=1.2)
    return figure


st.set_page_config(
    page_title="Sets",
    page_icon="∪",
    layout="wide",
)
apply_theme()
st.title("Sets")
st.write("Enter sets, choose an operation, and inspect the result visually.")

number_of_sets = st.selectbox("Number of sets", [2, 3, 4, 5])
labels = ["A", "B", "C", "D", "E"]
defaults = ["1,2,3,4", "3,4,5,6", "2,4,6,8", "1,3,5,7", "2,3,4,5"]

entered_sets = []
for index in range(number_of_sets):
    entered = st.text_input(
        f"Set {labels[index]}",
        value=defaults[index],
        key=f"set_input_{index}",
        help="Enter values separated by commas.",
    )
    entered_sets.append(parse_set_input(entered))

if not any(entered_sets):
    st.warning("Enter at least one value in a set.")
    st.stop()

if number_of_sets == 2:
    operation = st.selectbox(
        "Operation",
        ["A ∪ B", "A ∩ B", "A − B", "B − A", "A Δ B", "A'"],
    )
else:
    names = " ∪ ".join(labels[:number_of_sets])
    intersection_name = " ∩ ".join(labels[:number_of_sets])
    operation = st.selectbox("Operation", [f"{names} union", f"{intersection_name} intersection"])

result, explanation = calculate_operation(entered_sets, operation)
set_summary, concept, notation, intuition = operation_concept(
    operation,
    entered_sets,
    result,
)

st.header("Your result")
with st.container(border=True):
    st.markdown(
        '<div class="step-label">INPUT → OPERATION → ANSWER</div>',
        unsafe_allow_html=True,
    )
    st.write(f"**Input sets:** {set_summary}")
    st.write(f"**Selected operation:** `{operation}`")
    st.latex(notation)

    result_col, diagram_col = st.columns([1, 1.35], vertical_alignment="center")
    with result_col:
        st.subheader("Answer")
        st.metric("Number of elements", len(result))
        if result:
            st.success(
                f"The answer contains {len(result)} "
                f"{'element' if len(result) == 1 else 'elements'}."
            )
            st.code(
                "{ " + ", ".join(map(str, sorted(result, key=str))) + " }",
                language="text",
            )
        else:
            st.info("The answer is the empty set: ∅")
        st.caption(explanation)

    with diagram_col:
        st.subheader("See it visually")
        st.caption(
            "The shaded regions show which parts of the sets produce the answer."
        )
        st.pyplot(
            venn_figure(
                entered_sets[:3],
                labels[: min(number_of_sets, 3)],
            ),
            width="content",
        )
        if number_of_sets > 3:
            st.caption("The diagram visualizes the first three sets.")

    with st.expander("Why does this work?"):
        st.write(concept)
        st.caption(intuition)
