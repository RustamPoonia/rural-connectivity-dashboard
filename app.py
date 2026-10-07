
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_cleaning import load_data, clean_data
from src.calculations import get_overview_kpis, calculate_state_summary


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Rural Connectivity | Operations Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEME
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f3f7fb;
        --bg-2: #edf5ff;
        --card: #ffffff;
        --text: #101828;
        --muted: #475467;
        --line: #dfe5ef;
        --blue: #2367d2;
        --blue-soft: #edf4ff;
        --green: #10A571;
        --green-soft: #ebfaf3;
        --amber: #F59F0B;
        --amber-soft: #fff7e8;
        --red: #E15B4C;
        --red-soft: #fff1ef;
        --purple: #7857d9;
        --purple-soft: #f3efff;
        --shadow: 0 10px 22px rgba(15, 23, 42, 0.06);
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(35,103,210,0.08), transparent 30%),
            linear-gradient(180deg, #f6f9fc 0%, #eef5ff 100%);
    }

    .block-container {
        max-width: 1500px;
        padding: 1.2rem 1.6rem 2.2rem 1.6rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        border-right: none;
        box-shadow: inset -1px 0 0 rgba(148, 163, 184, 0.16);
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #9ca3af !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(148, 163, 184, 0.2);
    }

    .brand {
        padding: 0.25rem 0 1.1rem 0;
    }

    .brand-icon {
        display: inline-flex;
        width: 42px;
        height: 42px;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        font-size: 18px;
        margin-bottom: 0.7rem;
        box-shadow: 0 10px 18px rgba(59,130,246,0.28);
    }

    .brand-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
    }

    .brand-subtitle {
        font-size: 0.72rem;
        color: #a5b4cf;
        margin-top: 0.15rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .side-label {
        color: #6b7280 !important;
        font-size: 0.67rem !important;
        font-weight: 700 !important;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-top: 1.1rem;
    }

    /* Header */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.2rem;
        padding: 1.05rem 1.15rem;
        border: 1px solid rgba(35,103,210,0.12);
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(235,244,255,0.92));
        box-shadow: var(--shadow);
    }

    .eyebrow {
        color: var(--blue);
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .title {
        color: var(--text);
        font-size: 2.1rem;
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .subtitle {
        color: var(--muted);
        font-size: 0.87rem;
        margin-top: 0.38rem;
    }

    .source-pill {
        background: #ffffff;
        border: 1px solid rgba(35,103,210,0.15);
        border-radius: 999px;
        padding: 0.52rem 0.9rem;
        color: #334155;
        font-size: 0.72rem;
        font-weight: 700;
        box-shadow: 0 8px 22px rgba(59, 130, 246, 0.08);
        white-space: nowrap;
    }

    .status-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--green);
        margin-right: 7px;
        box-shadow: 0 0 0 5px rgba(16, 165, 113, 0.12);
    }

    /* KPI */
    .kpi {
        background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(248,250,252,1));
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.9rem 1rem 0.8rem 1rem;
        min-height: 132px;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .kpi:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 26px rgba(15, 23, 42, 0.08);
    }

    .kpi::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 5px;
        background: var(--blue);
    }

    .kpi.green::before { background: var(--green); }
    .kpi.amber::before { background: var(--amber); }
    .kpi.red::before { background: var(--red); }
    .kpi.purple::before { background: var(--purple); }

    .kpi-label {
        color: var(--muted);
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.65rem;
    }

    .kpi-value {
        color: var(--text);
        font-size: 1.9rem;
        line-height: 1;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .kpi-foot {
        color: #79859a;
        font-size: 0.7rem;
        margin-top: 0.7rem;
        line-height: 1.4;
    }

    /* Sections */
    .section {
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }

    .section-title {
        color: var(--text);
        font-size: 1rem;
        font-weight: 750;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 0.72rem;
        margin-top: 0.15rem;
    }

    .panel {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.75rem 0.85rem 0.45rem 0.85rem;
        box-shadow: 0 2px 5px rgba(16,24,40,.025);
    }

    /* Insight cards */
    .insight {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 0.75rem 0.85rem;
        min-height: 92px;
    }

    .insight-label {
        color: #98a2b3;
        font-size: 0.66rem;
        text-transform: uppercase;
        font-weight: 750;
        letter-spacing: .06em;
    }

    .insight-value {
        color: var(--text);
        font-size: 1.18rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }

    .insight-text {
        color: var(--muted);
        font-size: 0.7rem;
        margin-top: 0.2rem;
        line-height: 1.4;
    }

    /* Footer */
    .footer {
        color: #98a2b3;
        text-align: center;
        font-size: 0.65rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--line);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================

DATA_PATH = "data/processed/GP_Wise_Data.csv"


@st.cache_data(show_spinner="Loading GP network data...")
def load_dashboard_data():
    return clean_data(load_data(DATA_PATH))


try:
    df = load_dashboard_data()
except Exception as e:
    st.error("The dashboard could not load the processed GP dataset.")
    st.exception(e)
    st.stop()


# ============================================================
# HELPERS
# ============================================================

def fmt_num(value):
    if pd.isna(value):
        return "—"
    return f"{value:,.0f}"


def fmt_pct(value):
    if pd.isna(value):
        return "—"
    return f"{value:.1f}%"


def kpi(label, value, foot, accent="blue"):
    st.markdown(
        f"""
        <div class="kpi {accent}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title, subtitle):
    st.markdown(
        f"""
        <div class="section">
            <div class="section-title">{title}</div>
            <div class="section-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(label, value, text):
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-label">{label}</div>
            <div class="insight-value">{value}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">📡</div>
            <div class="brand-title">Rural Connectivity</div>
            <div class="brand-subtitle">Operations Analytics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("DASHBOARD", unsafe_allow_html=True)
    page = st.radio(
        "Dashboard",
        ["Executive Overview", "Performance & Risk"],
        label_visibility="collapsed",
    )

    st.markdown("FILTERS", unsafe_allow_html=True)

    states = sorted(df["circle"].dropna().unique().tolist())

    selected_states = st.multiselect(
        "State",
        states,
        default=states,
    )

    if not selected_states:
        st.warning("Select at least one state.")
        st.stop()

    st.divider()

    st.markdown("DATASET", unsafe_allow_html=True)
    st.caption("GP Wise Data")
    st.caption(f"{len(df):,} GP records")
    st.caption(f"{len(df.columns)} source columns")


filtered = df[df["circle"].isin(selected_states)].copy()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="top-header">
        <div>
            <div class="eyebrow">Operations Intelligence</div>
            <div class="title">Rural Connectivity Dashboard</div>
            <div class="subtitle">
                GP network coverage, HOTO, AMC and operational performance across the selected operating states.
            </div>
        </div>
        <div class="source-pill"><span class="status-dot"></span>GP Wise Data | 16K+ records</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CALCULATIONS
# ============================================================

# Main KPIs are calculated through the project's calculation layer.
all_kpis = get_overview_kpis(filtered)

# State summary
state_summary = calculate_state_summary(filtered)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    section(
        "Network Snapshot",
        "Current network population and operational coverage for the selected states",
    )

    # 7 KPI cards
    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        kpi(
            "Existing GPs",
            fmt_num(all_kpis["total_existing_gps"]),
            "Current GP population",
            "blue",
        )

    with c2:
        kpi(
            "Revised Existing GPs",
            fmt_num(all_kpis["revised_existing_gps"]),
            "After source-level deductions",
            "purple",
        )

    with c3:
        kpi(
            "HOTO Done",
            fmt_num(all_kpis["hoto_done_gps"]),
            "GPs with HOTO status = Done",
            "green",
        )

    with c4:
        kpi(
            "HOTO Completion",
            fmt_pct(all_kpis["hoto_percentage"]),
            "Against current dashboard denominator",
            "green",
        )

    c5, c6, c7 = st.columns(3, gap="medium")

    with c5:
        kpi(
            "AMC GPs",
            fmt_num(all_kpis["amc_gps"]),
            "GPs with AMC Date",
            "amber",
        )

    with c6:
        kpi(
            "AMC Coverage",
            fmt_pct(all_kpis["amc_percentage"]),
            "Against current dashboard denominator",
            "amber",
        )

    with c7:
        kpi(
            "AMC Fibre",
            f'{fmt_num(all_kpis["amc_fibre_rkm"])} RKM',
            "AMC-linked route kilometres",
            "blue",
        )

    # --------------------------------------------------------
    # STATE ANALYSIS
    # --------------------------------------------------------

    section(
        "State Performance",
        "How the three operating states compare across network, HOTO and AMC",
    )

    state_chart = state_summary.rename(
        columns={
            "circle": "State",
            "existing_gps": "Existing GPs",
            "hoto_done_gps": "HOTO Done",
            "amc_gps": "AMC GPs",
        }
    )

    left, right = st.columns([1.7, 1], gap="large")

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        fig = px.bar(
            state_chart,
            x="State",
            y=["Existing GPs", "HOTO Done", "AMC GPs"],
            barmode="group",
            text_auto=".0f",
        )

        fig.update_layout(
            template="plotly_white",
            height=390,
            margin=dict(l=10, r=10, t=25, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                x=0,
            ),
            font=dict(family="Inter", size=11),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False,
        )

        fig.update_xaxes(showgrid=False, title=None)
        fig.update_yaxes(
            title="GP Count",
            gridcolor="#eaecf0",
            zeroline=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        table = state_chart.copy()

        for col in ["Existing GPs", "HOTO Done", "AMC GPs"]:
            table[col] = table[col].map(fmt_num)

        st.dataframe(
            table,
            hide_index=True,
            use_container_width=True,
            height=340,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # HEALTH INDICATORS
    # --------------------------------------------------------

    section(
        "Network Health",
        "Quick operational indicators that highlight healthy coverage and areas requiring attention",
    )

    # These columns are available in the source structure.
    # We use the Oct-26 GP-level value when numeric.
    uptime_col = "oct-26"

    if uptime_col in filtered.columns:
        uptime = pd.to_numeric(filtered[uptime_col], errors="coerce")

        valid_uptime = uptime.dropna()

        if len(valid_uptime) > 0:
            above_98 = (valid_uptime >= 98).sum()
            zero_uptime = (valid_uptime == 0).sum()
            below_85 = (valid_uptime < 85).sum()

            # State-wise average uptime
            uptime_state = (
                pd.DataFrame({
                    "State": filtered["circle"],
                    "Uptime": uptime,
                })
                .dropna()
                .groupby("State", as_index=False)["Uptime"]
                .mean()
            )

            h1, h2, h3 = st.columns(3, gap="medium")

            with h1:
                insight(
                    "Healthy GPs",
                    fmt_num(above_98),
                    "GPs at or above 98% Oct-26 uptime",
                )

            with h2:
                insight(
                    "Critical GPs",
                    fmt_num(zero_uptime),
                    "GPs reporting 0% Oct-26 uptime",
                )

            with h3:
                insight(
                    "Below 85%",
                    fmt_num(below_85),
                    "GPs below 85% Oct-26 uptime",
                )

            a, b = st.columns(2, gap="large")

            with a:
                st.markdown('<div class="panel">', unsafe_allow_html=True)

                fig_u = px.bar(
                    uptime_state,
                    x="State",
                    y="Uptime",
                    text="Uptime",
                    range_y=[0, 100],
                )

                fig_u.update_traces(
                    texttemplate="%{text:.1f}%",
                    textposition="outside",
                )

                fig_u.update_layout(
                    title="Average GP Uptime by State",
                    title_font_size=13,
                    height=330,
                    margin=dict(l=10, r=10, t=45, b=10),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    showlegend=False,
                )

                fig_u.update_xaxes(showgrid=False)
                fig_u.update_yaxes(
                    title="Average uptime",
                    ticksuffix="%",
                    gridcolor="#eaecf0",
                )

                st.plotly_chart(
                    fig_u,
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

                st.markdown("</div>", unsafe_allow_html=True)

            with b:
                st.markdown('<div class="panel">', unsafe_allow_html=True)

                labels = ["≥98%", "85–<98%", "<85%"]
                values = [
                    above_98,
                    max(len(valid_uptime) - above_98 - below_85, 0),
                    below_85,
                ]

                fig_d = go.Figure(
                    data=[
                        go.Pie(
                            labels=labels,
                            values=values,
                            hole=0.68,
                            textinfo="label+percent",
                        )
                    ]
                )

                fig_d.update_layout(
                    title="GP Uptime Distribution",
                    title_font_size=13,
                    height=330,
                    margin=dict(l=10, r=10, t=45, b=10),
                    showlegend=False,
                    paper_bgcolor="white",
                )

                st.plotly_chart(
                    fig_d,
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

                st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.info("No numeric Oct-26 uptime values are available for the selected states.")

    else:
        st.info("The Oct-26 GP uptime field is not available in the processed dataset.")

    # --------------------------------------------------------
    # RECONCILIATION
    # --------------------------------------------------------

    with st.expander("Source reconciliation notes"):

        st.markdown(
            """
            **Revised Existing GPs:** raw GP-level calculation = **15,987**;
            source summary = **15,978**.

            **AMC Fibre RKM:** raw GP-level calculation = **35,901 RKM**;
            source summary = **35,976 RKM**.

            The dashboard retains the raw GP-level calculations instead
            of forcing them to match the summary.
            """
        )


# ============================================================
# PERFORMANCE & RISK
# ============================================================

else:

    section(
        "Performance & Risk",
        "Operational performance, uptime distribution and attention areas",
    )

    # --------------------------------------------------------
    # RISK METRICS
    # --------------------------------------------------------

    uptime_col = "oct-26"

    if uptime_col in filtered.columns:
        uptime = pd.to_numeric(filtered[uptime_col], errors="coerce")
        valid = uptime.dropna()

        healthy = int((valid >= 98).sum())
        zero = int((valid == 0).sum())
        below85 = int((valid < 85).sum())
    else:
        healthy = zero = below85 = 0

    r1, r2, r3, r4 = st.columns(4, gap="medium")

    with r1:
        kpi(
            "≥98% Uptime",
            fmt_num(healthy),
            "Healthy GP records",
            "green",
        )

    with r2:
        kpi(
            "0% Uptime",
            fmt_num(zero),
            "Critical GP records",
            "red",
        )

    with r3:
        kpi(
            "<85% Uptime",
            fmt_num(below85),
            "Attention required",
            "amber",
        )

    with r4:
        kpi(
            "AMC GPs",
            fmt_num(all_kpis["amc_gps"]),
            "Current selected states",
            "blue",
        )

    # --------------------------------------------------------
    # UPTIME DISTRIBUTION
    # --------------------------------------------------------

    section(
        "Uptime Distribution",
        "GP-level Oct-26 uptime distribution across selected states",
    )

    if uptime_col in filtered.columns:

        uptime = pd.to_numeric(filtered[uptime_col], errors="coerce")

        bins = [-0.001, 0, 30, 50, 75, 85, 90, 95, 98, 100.001]
        labels = [
            "0%",
            ">0–30%",
            ">30–50%",
            ">50–75%",
            ">75–85%",
            ">85–90%",
            ">90–95%",
            ">95–98%",
            "≥98%",
        ]

        bands = pd.cut(
            uptime,
            bins=bins,
            labels=labels,
            include_lowest=True,
            right=True,
        )

        dist = (
            pd.DataFrame({
                "State": filtered["circle"],
                "Band": bands,
            })
            .dropna()
            .groupby(["State", "Band"], observed=False)
            .size()
            .reset_index(name="GPs")
        )

        fig = px.bar(
            dist,
            x="State",
            y="GPs",
            color="Band",
            barmode="stack",
            text_auto=True,
        )

        fig.update_layout(
            template="plotly_white",
            height=430,
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                x=0,
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(
            title="GP Count",
            gridcolor="#eaecf0",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    else:
        st.info("Oct-26 uptime data is not available.")

    # --------------------------------------------------------
    # OPERATIONAL BREAKDOWN
    # --------------------------------------------------------

    section(
        "Operational Breakdown",
        "HOTO, AMC and fibre coverage by state",
    )

    operational = state_summary.rename(
        columns={
            "circle": "State",
            "existing_gps": "Existing GPs",
            "hoto_done_gps": "HOTO Done",
            "amc_gps": "AMC GPs",
        }
    ).copy()

    # Add raw AMC RKM by state
    rkm_state = (
        filtered.loc[filtered["amc_date"].notna()]
        .groupby("circle")["total_rkm"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "circle": "State",
                "total_rkm": "AMC Fibre RKM",
            }
        )
    )

    operational = operational.merge(
        rkm_state,
        on="State",
        how="left",
    )

    operational["AMC Coverage %"] = (
        operational["AMC GPs"]
        / operational["Existing GPs"]
        * 100
    ).round(1)

    operational["HOTO %"] = (
        operational["HOTO Done"]
        / operational["Existing GPs"]
        * 100
    ).round(1)

    operational["AMC Fibre RKM"] = operational["AMC Fibre RKM"].fillna(0)

    st.dataframe(
        operational,
        use_container_width=True,
        hide_index=True,
        height=240,
        column_config={
            "AMC Coverage %": st.column_config.ProgressColumn(
                "AMC Coverage %",
                min_value=0,
                max_value=100,
                format="%.1f%%",
            ),
            "HOTO %": st.column_config.ProgressColumn(
                "HOTO %",
                min_value=0,
                max_value=100,
                format="%.1f%%",
            ),
        },
    )

    # --------------------------------------------------------
    # RAW DATA EXPLORER
    # --------------------------------------------------------

    section(
        "GP Data Explorer",
        "Use the filtered dataset for operational drill-down",
    )

    preview_cols = [
        "circle",
        "district",
        "block",
        "gp",
        "gp_code",
        "block_hoto_status",
        "amc_date",
        "total_rkm",
        "oct-26",
    ]

    preview_cols = [c for c in preview_cols if c in filtered.columns]

    st.dataframe(
        filtered[preview_cols].head(200),
        use_container_width=True,
        hide_index=True,
        height=360,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Rural Connectivity Analytics | GP Wise Data |
        Built for operational analysis
    </div>
    """,
    unsafe_allow_html=True,
)
