"""Streamlit page for relations, closures, and Hasse diagrams."""

import re

import matplotlib.patches as patches
import matplotlib.pyplot as plt
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
        raise ValueError(
            "Enter ordered pairs such as (1,2),(2,3)."
        )

    target = domain if codomain is None else codomain
    relation = set()

    for pair in pairs:
        parts = [part.strip() for part in pair.split(",")]

        if len(parts) != 2:
            raise ValueError(
                f"Invalid ordered pair: ({pair}). "
                "Each pair must contain exactly two values."
            )

        first, second = map(parse_scalar, parts)

        if first not in domain:
            raise ValueError(
                f"{first} is not present in the domain set."
            )

        if second not in target:
            raise ValueError(
                f"{second} is not present in the codomain set."
            )

        relation.add((first, second))

    return relation


def relation_domain(relation):
    return {first for first, _ in relation}


def relation_range(relation):
    return {second for _, second in relation}


def is_reflexive(relation, domain):
    return all(
        (value, value) in relation
        for value in domain
    )


def is_symmetric(relation):
    return all(
        (second, first) in relation
        for first, second in relation
    )


def is_antisymmetric(relation):
    return all(
        first == second
        or (second, first) not in relation
        for first, second in relation
    )


def is_transitive(relation):
    values = {
        value
        for pair in relation
        for value in pair
    }

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
    """Remove self-loops and transitive edges."""
    edges = {
        (first, second)
        for first, second in relation
        if first != second
    }

    return {
        (first, second)
        for first, second in edges
        if not any(
            (first, middle) in edges
            and (middle, second) in edges
            for middle in domain
            if middle not in {first, second}
        )
    }


def relation_diagram(domain, codomain, relation):
    """Draw a mapping diagram using only Matplotlib."""
    figure, axis = plt.subplots(figsize=(9, 5))

    left = sorted(domain, key=str)
    right = sorted(codomain, key=str)

    left_y = {
        value: 1.8 - index * 0.7
        for index, value in enumerate(left)
    }

    right_y = {
        value: 1.8 - index * 0.7
        for index, value in enumerate(right)
    }

    axis.add_patch(
        patches.Ellipse(
            (0, 0),
            2.5,
            5,
            fill=False,
            linewidth=2,
        )
    )

    axis.add_patch(
        patches.Ellipse(
            (6, 0),
            2.5,
            5,
            fill=False,
            linewidth=2,
        )
    )

    axis.text(
        0,
        2.8,
        "Domain",
        ha="center",
        fontsize=12,
    )

    axis.text(
        6,
        2.8,
        "Codomain",
        ha="center",
        fontsize=12,
    )

    for value, y_position in left_y.items():
        axis.text(
            0,
            y_position,
            str(value),
            ha="center",
            va="center",
            fontsize=12,
        )

    for value, y_position in right_y.items():
        axis.text(
            6,
            y_position,
            str(value),
            ha="center",
            va="center",
            fontsize=12,
        )

    for first, second in relation:
        axis.annotate(
            "",
            xy=(4.8, right_y[second]),
            xytext=(1.2, left_y[first]),
            arrowprops={
                "arrowstyle": "->",
                "color": "darkorange",
                "linewidth": 2,
            },
        )

    axis.set_xlim(-1.5, 7.5)
    axis.set_ylim(-2.5, 3.5)
    axis.axis("off")

    return figure


def hasse_diagram(relation, domain):
    """Draw a simple Hasse diagram using only Matplotlib."""
    values = sorted(domain, key=str)
    edges = hasse_edges(relation, domain)

    positions = {
        value: (index % 3, index // 3)
        for index, value in enumerate(values)
    }

    figure, axis = plt.subplots(figsize=(7, 5))

    for first, second in edges:
        first_x, first_y = positions[first]
        second_x, second_y = positions[second]

        axis.annotate(
            "",
            xy=(second_x, second_y),
            xytext=(first_x, first_y),
            arrowprops={
                "arrowstyle": "-",
                "color": "darkgreen",
                "linewidth": 2,
            },
        )

    for value, (x_position, y_position) in positions.items():
        axis.scatter(
            x_position,
            y_position,
            s=1400,
            color="lightblue",
            edgecolors="black",
            zorder=2,
        )

        axis.text(
            x_position,
            y_position,
            str(value),
            ha="center",
            va="center",
            fontsize=12,
            zorder=3,
        )

    axis.set_title("Hasse diagram")

    axis.set_xlim(
        -1,
        max(2, len(values) - 1) + 1,
    )

    axis.set_ylim(
        -1,
        max(1, len(values) // 3) + 1,
    )

    axis.axis("off")

    return figure


# Streamlit page layout
# Streamlit page layout
st.set_page_config(
    page_title="Relations & Functions",
    page_icon="↔",
    layout="wide",
)

st.markdown("""
<style>
.math-card {
    background-color: #ffffff;
    border: 1px solid #e2e5e8;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}
.math-card h4 {
    color: #0d1b2a !important;
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 1.2rem;
    font-weight: 700;
    border-bottom: 2px solid #f7e9e7;
    padding-bottom: 8px;
    text-transform: uppercase;
}
.set-display {
    font-family: monospace;
    font-size: 1.15rem;
    color: #9d1c14;
    background-color: #f7e9e7;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
}
.badge-yes {
    background-color: #e6f4ea;
    color: #137333;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    display: inline-block;
}
.badge-no {
    background-color: #fce8e6;
    color: #c5221f;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

st.title("RELATIONS & FUNCTIONS")
st.markdown("Analyze relations, relation properties, domain, range, transitive closure, partial orders and Hasse diagrams.")

with st.form("relation_input_form"):
    mode = st.radio(
        "Relation Type",
        [
            "Relation on a single set (A → A)",
            "Relation between two sets (A → B)",
        ],
    )

    col1, col2 = st.columns(2)
    with col1:
        domain_text = st.text_input(
            "Set A",
            value="1, 2, 3",
            help="Enter elements separated by commas. Example: 1, 2, 3"
        )

    with col2:
        codomain_text = st.text_input(
            "Set B",
            value="2, 3, 4",
            help="Only used if A → B is selected. Enter elements separated by commas."
        )

    relation_text = st.text_area(
        "Relation R",
        value="(1,2), (2,3), (3,3)",
        help="Enter ordered pairs separated by commas. Example: (1,2), (2,3), (3,3)"
    )

    analyze_btn = st.form_submit_button("ANALYZE RELATION", type="primary")

if analyze_btn:
    try:
        domain = parse_set_input(domain_text)
        if not domain:
            raise ValueError("Please enter at least one element in Set A.")

        if mode.startswith("Relation between"):
            codomain = parse_set_input(codomain_text)
            if not codomain:
                raise ValueError("Please enter at least one element in Set B.")
        else:
            codomain = domain

        relation = parse_relation_input(
            relation_text,
            domain,
            codomain,
        )
        if not relation:
            raise ValueError("Please enter at least one valid relation pair.")
            
    except ValueError as error:
        st.error(str(error))
        st.stop()

    def format_set(s):
        if not s:
            return "∅"
        return "{ " + ", ".join(map(str, sorted(s, key=str))) + " }"

    def format_relation(r):
        if not r:
            return "∅"
        pairs = sorted(r, key=str)
        return "{ " + ", ".join(f"({a},{b})" for a, b in pairs) + " }"

    # 1. RELATION SUMMARY
    st.markdown('<div class="math-card"><h4>RELATION SUMMARY</h4>', unsafe_allow_html=True)
    st.markdown(f"**Set A:** <span class='set-display'>A = {format_set(domain)}</span><br><br>", unsafe_allow_html=True)
    if mode.startswith("Relation between"):
        st.markdown(f"**Set B:** <span class='set-display'>B = {format_set(codomain)}</span><br><br>", unsafe_allow_html=True)
    st.markdown(f"**Relation R:** <span class='set-display'>R = {format_relation(relation)}</span><br><br>", unsafe_allow_html=True)
    st.write(f"**Number of elements in Set A:** {len(domain)}")
    st.write(f"**Number of ordered pairs in R:** {len(relation)}")
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. DOMAIN, CODOMAIN & RANGE
    st.markdown('<div class="math-card"><h4>DOMAIN, CODOMAIN & RANGE</h4>', unsafe_allow_html=True)
    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        st.markdown(f"**Domain**<br><span class='set-display'>{format_set(relation_domain(relation))}</span>", unsafe_allow_html=True)
    with dc2:
        st.markdown(f"**Codomain**<br><span class='set-display'>{format_set(codomain)}</span>", unsafe_allow_html=True)
    with dc3:
        st.markdown(f"**Range**<br><span class='set-display'>{format_set(relation_range(relation))}</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. RELATION PROPERTIES
    st.markdown('<div class="math-card"><h4>RELATION PROPERTIES</h4>', unsafe_allow_html=True)
    
    props = {
        "Reflexive": is_reflexive(relation, domain),
        "Symmetric": is_symmetric(relation),
        "Antisymmetric": is_antisymmetric(relation),
        "Transitive": is_transitive(relation),
    }

    def get_reflexive_explanation():
        for value in domain:
            if (value, value) not in relation:
                return f"Missing: ({value},{value})"
        return "All (a,a) present."

    def get_symmetric_explanation():
        for first, second in relation:
            if (second, first) not in relation:
                return f"Missing reverse pair: ({second},{first})"
        return "All pairs have reverse."

    def get_antisymmetric_explanation():
        for first, second in relation:
            if first != second and (second, first) in relation:
                return f"Found both ({first},{second}) and ({second},{first})"
        return "No symmetric pairs except (a,a)."

    def get_transitive_explanation():
        for first, middle in relation:
            for m2, last in relation:
                if middle == m2 and (first, last) not in relation:
                    return f"Contains ({first},{middle}) and ({middle},{last}) but missing ({first},{last})"
        return "All transitive paths exist."
        
    explanations = {
        "Reflexive": get_reflexive_explanation() if not props["Reflexive"] else "Satisfied",
        "Symmetric": get_symmetric_explanation() if not props["Symmetric"] else "Satisfied",
        "Antisymmetric": get_antisymmetric_explanation() if not props["Antisymmetric"] else "Satisfied",
        "Transitive": get_transitive_explanation() if not props["Transitive"] else "Satisfied",
    }
    
    st.markdown("""
    <table style="width: 100%; border-collapse: collapse;">
        <tr style="border-bottom: 2px solid #e2e5e8; color: #526173;">
            <th style="padding: 8px; text-align: left;">Property</th>
            <th style="padding: 8px; text-align: left;">Result</th>
            <th style="padding: 8px; text-align: left;">Explanation</th>
        </tr>
    """, unsafe_allow_html=True)
    
    for prop_name, is_satisfied in props.items():
        badge = "<span class='badge-yes'>✓ Yes</span>" if is_satisfied else "<span class='badge-no'>✗ No</span>"
        st.markdown(f"""
        <tr style="border-bottom: 1px solid #e2e5e8;">
            <td style="padding: 12px 8px; font-weight: 600;">{prop_name}</td>
            <td style="padding: 12px 8px;">{badge}</td>
            <td style="padding: 12px 8px; color: #526173;">{explanations[prop_name]}</td>
        </tr>
        """, unsafe_allow_html=True)
    st.markdown("</table></div>", unsafe_allow_html=True)

    # 4. TRANSITIVE CLOSURE
    closure = transitive_closure(relation, domain)
    st.markdown('<div class="math-card"><h4>TRANSITIVE CLOSURE</h4>', unsafe_allow_html=True)
    if len(closure) <= 12:
        st.markdown(f"**Original Relation**<br><span class='set-display'>R = {format_relation(relation)}</span><br><br>", unsafe_allow_html=True)
        st.markdown(f"**Transitive Closure**<br><span class='set-display'>R⁺ = {format_relation(closure)}</span>", unsafe_allow_html=True)
    else:
        st.markdown("**Transitive Closure (Table)**", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(sorted(closure, key=str), columns=["From", "To"]), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. PARTIAL ORDER / POSET
    partial_order = props["Reflexive"] and props["Antisymmetric"] and props["Transitive"]
    st.markdown('<div class="math-card"><h4>PARTIAL ORDER / POSET</h4>', unsafe_allow_html=True)
    if partial_order:
        st.markdown("<span class='badge-yes'>✓ Yes</span> This relation is a partial order.", unsafe_allow_html=True)
    else:
        failed = [name for name in ["Reflexive", "Antisymmetric", "Transitive"] if not props[name]]
        st.markdown(f"<span class='badge-no'>✗ No</span> This relation is not a partial order.<br><br><strong>Failed properties:</strong> {', '.join(failed)}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 6. RELATION DIAGRAM
    st.markdown('<div class="math-card"><h4>RELATION DIAGRAM</h4><p style="color: #526173;">Shows the relation pairs.</p>', unsafe_allow_html=True)
    st.pyplot(relation_diagram(domain, codomain, relation), width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. HASSE DIAGRAM
    st.markdown('<div class="math-card"><h4>HASSE DIAGRAM</h4>', unsafe_allow_html=True)
    if partial_order:
        st.markdown('<p style="color: #526173;">Shows the cover relations of a partial order.</p>', unsafe_allow_html=True)
        st.pyplot(hasse_diagram(relation, domain), width="stretch")
    else:
        st.info("A Hasse diagram is available only for a partial order. This relation does not satisfy the requirements of a partial order.")
    st.markdown('</div>', unsafe_allow_html=True)
