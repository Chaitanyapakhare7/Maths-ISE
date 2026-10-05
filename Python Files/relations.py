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


# Streamlit page layout# Streamlit page layout
st.set_page_config(
    page_title="Relations & Functions",
    page_icon="↔",
    layout="wide",
)

if "relation_pairs" not in st.session_state:
    st.session_state.relation_pairs = set()

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
.step-label {
    color: #9d1c14;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 1px;
    margin-bottom: 12px;
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
st.markdown("Analyze mathematical relations effortlessly. Build relations, test properties, find closures, and generate Hasse diagrams without writing complex syntax.")

def format_set(s):
    if not s:
        return "∅"
    return "{ " + ", ".join(map(str, sorted(s, key=str))) + " }"

def format_relation(r):
    if not r:
        return "∅"
    pairs = sorted(r, key=str)
    return "{ " + ", ".join(f"({a},{b})" for a, b in pairs) + " }"

# --- 01 DEFINE SETS ---
st.markdown('<div class="math-card"><div class="step-label">01 — DEFINE SETS</div>', unsafe_allow_html=True)
mode = st.radio("Relation Type", ["Relation on a single set (A → A)", "Relation between two sets (A → B)"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    domain_text = st.text_input("Set A", value="1, 2, 3", help="Example: 1, 2, 3")
with col2:
    if mode.startswith("Relation between"):
        codomain_text = st.text_input("Set B", value="a, b, c", help="Example: a, b, c")
    else:
        codomain_text = ""
st.markdown('</div>', unsafe_allow_html=True)

try:
    domain = parse_set_input(domain_text)
    if mode.startswith("Relation between"):
        codomain = parse_set_input(codomain_text)
    else:
        codomain = domain
except ValueError as e:
    st.error(str(e))
    domain, codomain = set(), set()

valid_pairs = set()
for a, b in st.session_state.relation_pairs:
    if a in domain and b in codomain:
        valid_pairs.add((a, b))
if len(valid_pairs) != len(st.session_state.relation_pairs):
    st.session_state.relation_pairs = valid_pairs

# --- 02 BUILD RELATION ---
st.markdown('<div class="math-card"><div class="step-label">02 — BUILD RELATION</div>', unsafe_allow_html=True)
st.markdown("Select an element from the domain and its corresponding element from the codomain.")

build_col1, build_col2, build_col3 = st.columns([2, 2, 1])
domain_sorted = sorted(domain, key=str) if domain else [""]
codomain_sorted = sorted(codomain, key=str) if codomain else [""]

with build_col1:
    from_val = st.selectbox("FROM", domain_sorted)
with build_col2:
    to_val = st.selectbox("TO", codomain_sorted)
with build_col3:
    st.write("") 
    st.write("") 
    if st.button("➕ ADD PAIR", type="primary", use_container_width=True):
        if not domain or (mode.startswith("Relation between") and not codomain):
            st.error("Sets cannot be empty.")
        elif from_val == "" or to_val == "":
            st.error("Please select valid elements.")
        else:
            try:
                pair = (parse_scalar(str(from_val)), parse_scalar(str(to_val)))
                if pair in st.session_state.relation_pairs:
                    st.warning(f"Pair {pair} is already in the relation.")
                else:
                    st.session_state.relation_pairs.add(pair)
                    st.rerun()
            except ValueError:
                pass

st.markdown("---")
st.markdown("**CURRENT RELATION**")

if not st.session_state.relation_pairs:
    st.info("No ordered pairs added yet. Select From and To values above and click Add Pair.")
else:
    cols = st.columns(4)
    for idx, pair in enumerate(sorted(st.session_state.relation_pairs, key=str)):
        with cols[idx % 4]:
            if st.button(f"({pair[0]}, {pair[1]})  ❌", key=f"remove_{pair}"):
                st.session_state.relation_pairs.remove(pair)
                st.rerun()

    st.markdown(f"<br><span class='set-display'>R = {format_relation(st.session_state.relation_pairs)}</span>", unsafe_allow_html=True)
    
    if st.button("CLEAR RELATION"):
        st.session_state.relation_pairs.clear()
        st.rerun()

with st.expander("Advanced / Quick Input"):
    quick_rel = st.text_input("Quick enter relation", placeholder="(1,2), (2,3)")
    if st.button("APPLY QUICK INPUT"):
        try:
            rel = parse_relation_input(quick_rel, domain, codomain)
            st.session_state.relation_pairs.update(rel)
            st.rerun()
        except ValueError as e:
            st.error(str(e))

st.markdown('</div>', unsafe_allow_html=True)

# --- 03 ANALYZE ---
st.markdown('<div class="math-card"><div class="step-label">03 — ANALYZE</div>', unsafe_allow_html=True)
analyze_btn = st.button("ANALYZE RELATION", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

if analyze_btn:
    relation = st.session_state.relation_pairs
    if not domain:
        st.error("Set A is empty.")
        st.stop()
    if mode.startswith("Relation between") and not codomain:
        st.error("Set B is empty.")
        st.stop()
    if not relation:
        st.error("Relation R is empty. Please add at least one pair.")
        st.stop()

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
