import streamlit as st
import requests

# CONFIGURATION
API_URL = "http://127.0.0.1:8000"


# PAGE CONFIG
st.set_page_config(
    page_title="Agent Report Generator", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# CUSTOM CSS FOR STYLING
custom_css = """
<style>
    /* ===============================
            BACKGROUND & TEXT
       ===============================*/
    /* Apply background gradient: Green at the bottom to Black at the top */
    .stApp {
        background: linear-gradient(
        to top,
        #114232,
        #000000
        ); 
    }
    
    /* Make all text white and soft (lighter font-weight, slight transparency) */
    h1, h2, h3, p, span, div, label {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #F8F9FA !important; /* Soft, slightly off-white */
        font-weight: 300 !important; /* Softens the text appearance */
        letter-spacing: 0.5px;
    }

    /* =========================
               SIDEBAR 
       ========================= */
    [data-testid="stSidebar"] {
        text-align: left !important;
        background-color: #121212 !important; /* Very dark grey background */
        border-right: 1px solid #222222;       /* Subtle dark border */
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
    text-align: left !important;
    }

    /* Make sidebar inner containers dark grey */
    [data-testid="stSidebar"] > div:first-child {
        background-color: #121212 !important;
    }

    .sidebar-divider {
        border-bottom: 1px solid #222222;
        margin: 1rem 0;
    }

    .status-indicator {
        font-size: 0.85rem;
        margin-bottom: 4px;
    }
    .status-online { color: #3fb950; font-weight: 600; }
    .status-dag { color: #8250df; font-weight: 600; }
    .status-verified { color: #8250df; font-weight: 600; }

    /* Sidebar buttons - grey*/
    [data-testid="stSidebar"] div.stButton > button,
    [data-testid="stSidebar"] div.stDownloadButton > button {
    background-color: #2b2b2b !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
    border-radius: 6px;
    transition: all 0.2s ease-in-out;
    margin-top: 2px;
    }
    [data-testid="stSidebar"] div.stButton > button:hover,
    [data-testid="stSidebar"] div.stDownloadButton > button:hover {
            background-color: #3a3a3a !important;
            border-color: #666666 !important;
            color: #ffffff !important;
    }

    /* RECENT DROPDOWN */
    [data-testid="stSidebar"] [data-testid="stExpander"] details summary {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    color: #F8F9FA !important;

    /* Only slightly adjust spacing */
    padding-left: 10px !important;
    padding-right: 5px !important;
    }

    /* MODEL DROPDOWN */
    [data-testid="stSidebar"] [data-baseweb="popover"] {
    background-color: rgba(255, 255, 255, 0.1) !important;
    border: none !important;
    }

    /* Dropdown list */
    [data-testid="stSidebar"] [data-baseweb="menu"] {
    background-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* DROPDOWN MENU */
    [data-testid="stSidebar"] [data-baseweb="menu"] li {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: #FFFFFF !important;
    }

    /* Text inside options */
    [data-testid="stSidebar"] [data-baseweb="menu"] li * {
    color: #FFFFFF !important;
    }

    /* Hovered option */
    [data-testid="stSidebar"] [data-baseweb="menu"] li:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: #FFFFFF !important;
    }

    /* Currently selected option */
    [data-testid="stSidebar"] [data-baseweb="menu"] li[aria-selected="true"] {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: #FFFFFF !important;
    }


    /* ================================= 
            PIPELINE CARDS 
       ================================= */
    .pipeline-section-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #8b949e !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }
    .pipeline-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 15px;
        margin-bottom: 40px;
    }
    .pipeline-card {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid #121212;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        flex-direction: column;
    }
    .pipeline-num {
        color: #58a6ff;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .pipeline-title {
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 1rem;
    }
    .pipeline-desc {
        color: #8b949e !important;
        font-size: 0.8rem;
        line-height: 1.4;
    }

    /* Pipeline columns */
    div[data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
    }

    /* Make cards fill the column equally */
    div[data-testid="column"] .pipeline-card {
    height: 140px !important;
    min-height: 140px !important;
    max-height: 140px !important;
    flex: 1 !important;
    }

    /* ================================= 
            MAIN CONTENT POSITION 
       ================================= */
    /* CENTER THE CONTENT VERTICALLY */
    .block-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 85vh; /* Takes up most of the viewport height to push content to the middle */
        padding-top: 30vh !important;
    }
    
    /* CENTER THE TEXT HORIZONTALLY */
    h1, .stMarkdown p {
        text-align: center;
    }

    /* ======================
            TEXT INPUT 
       ====================== */
    .stTextInput > div > div > input {
        color: white;
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 12px 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #58a6ff !important;
        box-shadow: none !important;
    }
    
    /* Style the generate button */
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.3);
        border-color: white;
        box-shadow: 0 4px 12px rgba(50, 90, 95, 0.3) !important;
    }

    .suggestions {
        font-size: 0.85rem;
        color: #8b949e;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .suggestions span {
        color: #8250df;
        cursor: pointer;
    }

</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)


# --- Sidebar ---
with st.sidebar:
    st.title("ResearchForge ✨")
    st.markdown("### Studio Control")
    st.markdown("<p style='font-size: 0.85rem; color: #8b949e; margin-bottom: 20px;'>Multi-Agent Autonomous Research Orchestrator</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    
    st.markdown("### System State")
    st.markdown("<div class='status-indicator'>• Engine: <span class='status-online'>Online</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='status-indicator'>• Topology: <span class='status-dag'>LangGraph DAG</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='status-indicator'>• Consensus: <span class='status-verified'>Fact-Verified</span></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    
    # LLM MODEL SELECTION (Kept from original code, styled nicely)
    st.markdown("### Model Configuration")
    
    # LLM MODEL SELECTION
    st.subheader("LLM Model")

    model_options = {
        "Claude Sonnet": "anthropic/claude-sonnet-4-20250514",
        "GPT-4o": "openai/gpt-4o",
        "Gemini 1.5 Pro": "gemini/gemini-1.5-pro",
    }

    selected_model_name = st.selectbox(
        "Choose a model",
        options=list(model_options.keys()),
        index=0,
        label_visibility="collapsed"
    )

    selected_model = model_options[selected_model_name]

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("### Research History")
    # "Recent" Dropdown
    with st.expander("Recent", expanded=True):

        try:
            response = requests.get(
                f"{API_URL}/reports/recent",
                timeout=10
            )

            recent_reports = response.json()

            # Successful response
            if response.status_code == 200:
                if not recent_reports:

                    st.caption(
                        "No recent reports."
                    )

                else:
                    # Display reports
                    for report in recent_reports:

                        report_id = report["id"]
                        topic = report["topic"]

                        # Report title
                        st.markdown(f"**{report['topic']}**")

                        #Date
                        created_at = report.get(
                            "created_at"
                        )

                        if created_at:
                            st.caption(
                            created_at
                            )

                        # Download buttons
                        dl_col1, dl_col2 = st.columns(2)

                        # PDF
                        with dl_col1:
                            # Requires unique keys for each button in a loop
                            try:
                                pdf_response = (
                                    requests.get(
                                        f"{API_URL}/reports/"
                                        f"{report_id}/pdf",
                                        timeout=30,
                                    )
                                )   

                                if pdf_response.status_code == 200:
                                    st.download_button(
                                        label="📄 PDF", 
                                        data=pdf_response.content, 
                                        file_name=f"{report['topic']}.pdf", 
                                        mime="application/pdf", 
                                        key=f"pdf_{report['topic']}",
                                        #use_container_width=True,                                                                        use_container_width=True
                                )
                            except requests.exceptions.RequestException:
                                st.caption("PDF unavailable")

                        # DOCX        
                        with dl_col2:
                            try:
                                docx_response = (
                                    requests.get(
                                        f"{API_URL}/reports/"
                                        f"{report_id}/docx",
                                        timeout=30,
                                    )
                                )

                                if docx_response.status_code == 200:
                                    st.download_button(
                                        label="📝 DOCX", 
                                        data=docx_response.content, 
                                        file_name=f"{report['topic']}.docx", 
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                                        key=f"docx_{report['topic']}",
                                        use_container_width=True
                                    )
                            except requests.exceptions.RequestException:
                                st.caption("DOCX unavailable")

                            # Separator
                            st.divider()

            elif response.status_code == 404:
                st.info("No recent reports yet.")

            else:
                st.error("Unable to retrieve recent report.")

        except requests.exceptions.RequestException:
            st.warning("Research API is not running.")
            
            

# MAIN UI

# Pipeline Visualization
st.markdown("<div class='pipeline-section-title'>Autonomous Agent Pipeline</div>", unsafe_allow_html=True)
st.markdown("""
<div class="pipeline-grid">
    <div class="pipeline-card">
        <div class="pipeline-num">01</div>
        <div class="pipeline-title">Planner</div>
        <div class="pipeline-desc">Planner creates the report outline</div>
    </div>
    <div class="pipeline-card">
        <div class="pipeline-num">02</div>
        <div class="pipeline-title">Web_Researcher</div>
        <div class="pipeline-desc">Queries Tavily engines</div>
    </div>
    <div class="pipeline-card">
            <div class="pipeline-num">03</div>
            <div class="pipeline-title">Acad_Researcher</div>
            <div class="pipeline-desc">Queries BASE engines for academic literature</div>
        </div>
    <div class="pipeline-card">
        <div class="pipeline-num">04</div>
        <div class="pipeline-title">Writer</div>
        <div class="pipeline-desc">Writer creates the initial draft of the report</div>
    </div>
    <div class="pipeline-card">
        <div class="pipeline-num">05</div>
        <div class="pipeline-title">Reviewer</div>
        <div class="pipeline-desc">Reviewer evaluates the draft and provides feedback.</div>
    </div>
    <div class="pipeline-card">
        <div class="pipeline-num">06</div>
        <div class="pipeline-title">Formatter</div>
        <div class="pipeline-desc">Formatter formats the final report</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("Multi-Agent Report Generator")
st.markdown("Enter your research topic below. Our AI agents will investigate, compile, and format a comprehensive report for you.")

# Adding a small spacer
st.write("")

# Search Bar and Generate Button

col1, col2 = st.columns([4, 1]) # The search bar gets 4 parts of the space, the button gets 1

with col1:
    # INPUT FIELD
    topic = st.text_input("Topic Search", placeholder="What would you like a report on?", label_visibility="collapsed")

with col2:
    # GENERATE BUTTON
    generate_btn = st.button("Generate", use_container_width=True)

# Trigger Logic (Generate button)
if generate_btn:
    if not topic.strip():

        st.warning(
            "Please enter a research topic."
        )

    else:

        payload = {
            "topic": topic,
            # Use your actual values here
            "length": "medium",
            "style": "academic",
            "citation_format": "APA",
            "model": selected_model,
        }

        try:
            response = requests.post(
                f"{API_URL}/reports/generate",
                json=payload,
                timeout=300,
            )

            if response.status_code == 200:

                report = response.json()

                st.success(
                    "Report generated successfully!"
                )

                # Display report
                st.markdown(report["content"])

                # Refresh so Recent shows new report
                st.rerun()

            else:
                st.error(
                    f"Error generating report: {response.status_code} - {response.text}"
                )
                
        except requests.exceptions.RequestException as exc:
            st.error(
                f"Could not connect to API: {exc}"
            )