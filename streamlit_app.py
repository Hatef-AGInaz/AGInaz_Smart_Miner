"""Public portfolio demo. It does not import or run the private engine."""
import streamlit as st

from examples.content_quality import evaluate_content_quality


st.set_page_config(page_title="AGInaz Smart Miner Engine", page_icon="🔎", layout="centered")
st.title("AGInaz Smart Miner Engine")
st.caption("Structured web content for research workflows · portfolio demo")

overview, routing, cleaning = st.tabs(
    ["Overview", "Try the public router signal", "Recorded cleaning example"]
)

with overview:
    st.write(
        "Smart Miner chooses between a lightweight HTTP fetch and a bounded "
        "browser fallback. It then cleans the page into a reusable document "
        "with headings, tables, links, source URL and valid JSON-LD. Optional "
        "schema extraction can use that document without another fetch."
    )
    st.info(
        "This public demo runs a small v1.2 routing signal and displays a "
        "recorded synthetic cleaning example. It does not fetch websites, "
        "call an LLM, or expose the private v1.3 engine."
    )
    st.write("Local prototype verification: 19 offline tests and one browser test.")

with routing:
    st.write("Paste text to inspect the deterministic static-content signal.")
    sample = st.text_area(
        "Visible text", value="Loading...", height=160,
        help="Evaluated locally inside this public demo; no website is fetched.",
    )
    threshold = st.number_input(
        "Minimum visible characters", min_value=0, max_value=10000,
        value=600, step=50,
    )
    quality = evaluate_content_quality(sample, int(threshold))
    st.metric("Visible characters", quality["visible_character_count"])
    st.metric("Words", quality["word_count"])
    st.metric("Unique-word ratio", quality["unique_word_ratio"])
    if quality["accepted"]:
        st.success("Static content passes this signal.")
    else:
        st.warning("Browser fallback candidate: " + ", ".join(quality["reason_codes"]))
    st.caption(
        "This signal alone does not prove page quality or render AJAX content."
    )

with cleaning:
    st.write("Recorded output from a synthetic local HTML fixture:")
    left, right = st.columns(2)
    left.metric("Raw HTML characters", 473)
    right.metric("Clean extraction-input characters", 309)
    st.code(
        "[Navigation](https://example.test/)\n\n"
        "# Catalog\n\nAvailable products and prices.\n\n"
        "| Name | Price |\n| --- | --- |\n| Laptop | 12 |\n\n"
        "[Product details](https://example.test/item/1)",
        language="markdown",
    )
    st.caption(
        "The complete extraction input also includes the source URL, title "
        "and parsed JSON-LD. These are character counts, not token savings."
    )
