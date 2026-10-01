"""Public portfolio demo. It does not import or run the private engine."""

import html

import streamlit as st

from examples.content_quality import evaluate_content_quality


st.set_page_config(
    page_title="AGInaz Smart Miner Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      .block-container { max-width: 1120px; padding-top: 2.2rem; padding-bottom: 3rem; }
      .sm-hero {
        position: relative; overflow: hidden; padding: 2.6rem 3rem;
        border: 1px solid #31546d; border-radius: 22px;
        background: radial-gradient(circle at 88% 8%, #155564 0, transparent 35%),
                    linear-gradient(125deg, #102539 0%, #0b1728 70%);
        box-shadow: 0 18px 48px #02081255;
      }
      .sm-eyebrow { color: #5eead4; font-size: .75rem; font-weight: 800;
                    letter-spacing: .18em; text-transform: uppercase; }
      .sm-hero h1 { color: #f2f8ff; font-size: clamp(2rem, 5vw, 3.5rem);
                    line-height: 1.07; margin: .8rem 0; letter-spacing: -.045em; }
      .sm-hero p { color: #b9ccdb; font-size: 1.08rem; max-width: 650px; margin: 0; }
      .sm-chip { display: inline-block; margin-top: 1.5rem; margin-right: .5rem;
                 padding: .38rem .72rem; border-radius: 999px; color: #ccebe9;
                 background: #1b3a49; border: 1px solid #335e68;
                 font-size: .78rem; font-weight: 650; }
      .sm-card { min-height: 155px; padding: 1.15rem 1.3rem; margin: .35rem 0 1.2rem;
                 background: #102336; border: 1px solid #294457; border-radius: 16px; }
      .sm-icon { font-size: 1.5rem; }
      .sm-card h3 { color: #f0f8ff; font-size: 1.1rem; margin: .6rem 0 .4rem; }
      .sm-card p { color: #a9c0d0; font-size: .9rem; line-height: 1.5; margin: 0; }
      .sm-kicker { color: #5eead4; font-weight: 800; letter-spacing: .12em;
                   font-size: .73rem; text-transform: uppercase; margin-bottom: .3rem; }
      .sm-muted { color: #a9c0d0; font-size: .9rem; line-height: 1.55; }
      .sm-result { padding: 1.15rem 1.35rem; border-radius: 15px;
                   background: #102336; border: 1px solid #2b5360; margin: .9rem 0; }
      .sm-result strong { color: #eefaff; font-size: 1.05rem; }
      .sm-result p { color: #b7ccd9; margin: .4rem 0 0; }
      .sm-result--warn { border-color: #846b3b; background: #2a241c; }
      .sm-divider { height: 1px; background: #294457; margin: 1.5rem 0; }
      @media (max-width: 640px) {
        .block-container { padding-top: 1rem; }
        .sm-hero { padding: 1.8rem 1.3rem; }
        .sm-card { min-height: 0; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="sm-hero">
      <div class="sm-eyebrow">AGINAZ / PUBLIC INTERACTIVE PREVIEW</div>
      <h1>Smart Miner Engine<span style="color:#5eead4">.</span></h1>
      <p>From messy web pages to structured, reusable research input.</p>
      <span class="sm-chip">⚡ HTTP-first routing</span>
      <span class="sm-chip">🧭 Browser fallback</span>
      <span class="sm-chip">📄 Clean documents</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

overview, routing, cleaning = st.tabs(
    ["✦ Overview", "⚡ Try the signal", "📄 Before / after"]
)

with overview:
    st.write("")
    st.markdown('<div class="sm-kicker">How it works</div>', unsafe_allow_html=True)
    st.subheader("One page. The right route. Cleaner output.")
    cols = st.columns(3, gap="medium")
    cards = [
        ("⚡", "Fetch efficiently", "Try lightweight HTTP first and inspect the visible content."),
        ("🧭", "Render when needed", "Use a bounded browser fallback for pages that need JavaScript."),
        ("📄", "Keep the structure", "Preserve headings, tables, links, source URL, and valid JSON-LD."),
    ]
    for col, (icon, title, description) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="sm-card"><div class="sm-icon">{icon}</div>'
                f'<h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True,
            )
    st.markdown(
        '<div class="sm-kicker">What you can try here</div>'
        '<p class="sm-muted">Run a small, deterministic routing signal from the public '
        'v1.2 excerpt, then inspect a recorded cleaning example built from synthetic '
        'data. The private engine stays private.</p>',
        unsafe_allow_html=True,
    )
    st.info(
        "This preview does not fetch websites or call an LLM. "
        "The full engine is developed in a separate private repository."
    )
    st.caption("Prototype verification: 19 offline tests and one opt-in browser test.")

with routing:
    st.write("")
    st.markdown('<div class="sm-kicker">Interactive / public excerpt</div>', unsafe_allow_html=True)
    st.subheader("Would this text pass the static-page check?")
    st.markdown(
        '<p class="sm-muted">Paste visible page text or load a sample. '
        'The result updates as you type.</p>',
        unsafe_allow_html=True,
    )
    if "sample_text" not in st.session_state:
        st.session_state.sample_text = "Loading..."
    short_col, rich_col, _ = st.columns([1, 1, 2])
    with short_col:
        if st.button("Try sparse page", use_container_width=True):
            st.session_state.sample_text = "Loading..."
    with rich_col:
        if st.button("Try content page", use_container_width=True):
            st.session_state.sample_text = (
                "Research catalog. This page describes a collection of product "
                "records, prices, categories, and source links. Each record contains "
                "a title, summary, publication date, and a link to its original "
                "source. Researchers can compare the records, filter by category, "
                "and review the supporting details. " * 4
            )
    sample = st.text_area(
        "Visible page text",
        key="sample_text",
        height=170,
        help="Only the public signal processes this text. No website is fetched.",
    )
    threshold = st.slider(
        "Minimum visible characters", min_value=0, max_value=2000, value=600, step=50
    )
    quality = evaluate_content_quality(sample, threshold)
    a, b, c = st.columns(3)
    a.metric("Visible characters", quality["visible_character_count"])
    b.metric("Words", quality["word_count"])
    c.metric("Unique-word ratio", f'{quality["unique_word_ratio"]:.0%}')
    if quality["accepted"]:
        st.markdown(
            '<div class="sm-result"><strong>✓ Static content passes this signal</strong>'
            '<p>There is enough visible, varied text to continue with the HTTP result.</p></div>',
            unsafe_allow_html=True,
        )
    else:
        reasons = {
            "INSUFFICIENT_VISIBLE_TEXT": "Too little visible text",
            "INSUFFICIENT_WORD_COUNT": "Too few words",
            "LOW_TEXT_DIVERSITY": "Text repeats too much",
        }
        readable_reasons = ", ".join(reasons[code] for code in quality["reason_codes"])
        st.markdown(
            '<div class="sm-result sm-result--warn">'
            '<strong>↗ Browser fallback candidate</strong>'
            f'<p>{html.escape(readable_reasons)}. A browser render may reveal more content.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    st.caption(
        "This signal is one routing input, not a guarantee of page quality. "
        "This demo does not perform a browser render."
    )

with cleaning:
    st.write("")
    st.markdown('<div class="sm-kicker">Recorded / synthetic example</div>', unsafe_allow_html=True)
    st.subheader("Less page noise. More useful structure.")
    st.markdown(
        '<p class="sm-muted">The example below was recorded from a local synthetic '
        'HTML fixture. It is not a live extraction.</p>',
        unsafe_allow_html=True,
    )
    left, right = st.columns(2, gap="large")
    with left:
        st.metric("Raw HTML", "473 characters")
        st.markdown("**Before · page markup**")
        st.code(
            '<nav><a href="/">Navigation</a></nav>\n'
            '<h1>Catalog</h1>\n'
            '<p>Available products and prices.</p>\n'
            '<table>…</table>',
            language="html",
        )
    with right:
        st.metric("Clean extraction input", "309 characters")
        st.markdown("**After · structured text**")
        st.code(
            "[Navigation](https://example.test/)\n\n"
            "# Catalog\n\nAvailable products and prices.\n\n"
            "| Name | Price |\n| --- | --- |\n| Laptop | 12 |\n\n"
            "[Product details](https://example.test/item/1)",
            language="markdown",
        )
    st.info(
        "The full recorded extraction input also includes source URL, title, "
        "and parsed JSON-LD. Counts are characters for one fixture, not token savings."
    )

st.markdown('<div class="sm-divider"></div>', unsafe_allow_html=True)
st.caption("© 2026 Hatef-AGInaz · Public portfolio preview · All rights reserved")
