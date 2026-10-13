"""Shared visual theme for the Maths ISE Streamlit pages."""

import streamlit as st


def apply_theme() -> None:
    """Apply the shared animated glassmorphism interface."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --ink: #201a2b;
            --muted: #665b78;
            --violet: #7c3aed;
            --violet-dark: #4c1d95;
            --cyan: #06b6d4;
            --pink: #ec4899;
            --card: rgba(255, 255, 255, 0.78);
            --line: rgba(124, 58, 237, 0.16);
        }

        .stApp {
            background:
                radial-gradient(circle at 5% 5%, rgba(192, 132, 252, 0.24), transparent 28rem),
                radial-gradient(circle at 96% 12%, rgba(34, 211, 238, 0.18), transparent 25rem),
                linear-gradient(135deg, #fff9f5 0%, #faf5ff 48%, #effcff 100%);
            color: var(--ink);
            font-family: 'DM Sans', sans-serif;
        }

        .stApp::before,
        .stApp::after {
            content: "";
            position: fixed;
            width: 18rem;
            height: 18rem;
            border-radius: 999px;
            pointer-events: none;
            filter: blur(2px);
            opacity: 0.18;
            z-index: 0;
            animation: drift 14s ease-in-out infinite alternate;
        }

        .stApp::before {
            background: #ec4899;
            left: -10rem;
            bottom: 8%;
        }

        .stApp::after {
            background: #06b6d4;
            right: -10rem;
            top: 42%;
            animation-delay: -5s;
        }

        [data-testid="stHeader"] {
            background: rgba(255, 249, 245, 0.72);
            backdrop-filter: blur(14px);
        }

        [data-testid="stMainBlockContainer"] {
            position: relative;
            z-index: 1;
            max-width: 1320px;
            padding-top: 3.5rem;
            padding-bottom: 5rem;
        }

        h1, h2, h3, h4 {
            font-family: 'Space Grotesk', sans-serif !important;
            color: var(--ink) !important;
            letter-spacing: -0.035em;
        }

        h1 {
            font-size: clamp(2.4rem, 5vw, 4.6rem) !important;
            line-height: 1 !important;
            background: linear-gradient(100deg, var(--violet-dark), var(--pink) 52%, var(--cyan));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
            animation: title-in 0.7s ease both;
        }

        h2, h3 {
            margin-top: 1.5rem !important;
        }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {
            color: var(--muted);
        }

        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stMetric"],
        [data-testid="stExpander"] {
            border: 1px solid var(--line);
            border-radius: 22px;
            background: var(--card);
            box-shadow: 0 16px 45px rgba(76, 29, 149, 0.09);
            backdrop-filter: blur(18px);
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover,
        [data-testid="stMetric"]:hover,
        [data-testid="stExpander"]:hover {
            transform: translateY(-3px);
            border-color: rgba(236, 72, 153, 0.34);
            box-shadow: 0 20px 55px rgba(124, 58, 237, 0.16);
        }

        [data-testid="stMetric"] {
            padding: 1rem 1.2rem;
        }

        [data-testid="stMetricValue"] {
            color: var(--violet-dark);
            font-family: 'Space Grotesk', sans-serif;
        }

        .stButton > button,
        [data-testid="stFormSubmitButton"] > button {
            border: 0;
            border-radius: 999px;
            color: white;
            font-weight: 700;
            background: linear-gradient(100deg, var(--violet), var(--pink));
            box-shadow: 0 8px 20px rgba(124, 58, 237, 0.24);
            transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
        }

        .stButton > button:hover,
        [data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-2px) scale(1.02);
            filter: saturate(1.2);
            box-shadow: 0 12px 26px rgba(236, 72, 153, 0.3);
        }

        input, textarea, [data-baseweb="select"] > div {
            border-radius: 14px !important;
            border-color: rgba(124, 58, 237, 0.2) !important;
            background: rgba(255, 255, 255, 0.74) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        input:focus, textarea:focus, [data-baseweb="select"] > div:focus-within {
            border-color: var(--violet) !important;
            box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.12) !important;
        }

        [data-baseweb="tab-list"] {
            gap: 0.5rem;
            border-bottom: 1px solid var(--line);
        }

        [data-baseweb="tab"] {
            border-radius: 12px 12px 0 0;
            transition: background 0.2s ease, color 0.2s ease;
        }

        [data-baseweb="tab"]:hover {
            background: rgba(192, 132, 252, 0.15);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 18px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(76, 29, 149, 0.07);
        }

        [data-testid="stAlert"] {
            border-radius: 16px;
            border-left-width: 5px;
        }

        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 15% 5%, rgba(192, 132, 252, 0.3), transparent 16rem),
                linear-gradient(180deg, #24103f, #351660 72%, #24103f);
        }

        [data-testid="stSidebar"] * {
            color: #faf5ff;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 14px;
            margin: 0.2rem 0;
            transition: background 0.2s ease, transform 0.2s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(255, 255, 255, 0.13);
            transform: translateX(4px);
        }

        .math-card {
            padding: 1.4rem;
            margin: 1rem 0 1.5rem;
            border: 1px solid var(--line);
            border-radius: 22px;
            background: var(--card);
            box-shadow: 0 16px 45px rgba(76, 29, 149, 0.09);
            backdrop-filter: blur(18px);
            animation: card-in 0.5s ease both;
        }

        .step-label {
            color: var(--violet-dark);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.16em;
        }

        .set-display {
            color: var(--violet-dark);
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
        }

        .badge-yes, .badge-no {
            display: inline-block;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-weight: 700;
            animation: pulse 2.4s ease-in-out infinite;
        }

        .badge-yes {
            color: #047857;
            background: #d1fae5;
        }

        .badge-no {
            color: #be123c;
            background: #ffe4e6;
        }

        @keyframes drift {
            from { transform: translate3d(0, 0, 0) scale(1); }
            to { transform: translate3d(28px, -22px, 0) scale(1.12); }
        }

        @keyframes title-in {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes card-in {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(124, 58, 237, 0); }
            50% { box-shadow: 0 0 0 5px rgba(124, 58, 237, 0.08); }
        }

        @media (max-width: 720px) {
            [data-testid="stMainBlockContainer"] {
                padding-top: 2rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
