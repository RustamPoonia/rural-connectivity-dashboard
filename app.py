import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_cleaning import load_data, clean_data


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PRATAP | Rural Connectivity",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEME / POWER BI STYLE
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #f5f6f8;
        --card: #ffffff;
        --text: #111827;
        --muted: #667085;
        --line: #e4e7ec;
        --blue: #2563eb;
        --blue-soft: #eff6ff;
        --green: #16a34a;
        --amber: #d97706;
        --red: #dc2626;
        --navy: #111827;
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: var(--bg);
    }

    .block-container {
        max-width: 1550px;
        padding: 1rem 1.35rem 2rem 1.35rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #9ca3af !important;
    }

    .brand {
        padding: 0.2rem 0 0.8rem 0;
    }

    .brand-mark {
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #2563eb;
        border-radius: 10px;
        font-size: 20px;
        margin-bottom: 0.7rem;
    }

    .brand-title {
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.03em;
    }

    .brand-subtitle {
        color: #9ca3af;
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        margin-top: 0.2rem;
    }

    .side-heading {
        color: #6b7280;
        font-size: 0.64rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 1rem 0 0.4rem 0;
    }

    /* Header */
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }

    .eyebrow {
        color: var(--blue);
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }

    .page-title {
        color: var(--text);
        font-size: 1.75rem;
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-top: 0.12rem;
    }

    .page-subtitle {
        color: var(--muted);
        font-size: 0.76rem;
        margin-top: 0.3rem;
    }

    .data-status {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 0.45rem 0.7rem;
        color: #475467;
        font-size: 0.67rem;
        white-space: nowrap;
    }

    /* Filter strip */
    .filter-title {
        color: #344054;
        font-size: 0.72rem;
        font-weight: 800;
        margin: 0.15rem 0 0.35rem 0;
    }

    /* KPI */
    .kpi {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 9px;
        padding: 0.72rem 0.8rem;
        min-height: 91px;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.035);
        position: relative;
        overflow: hidden;
    }

    .kpi::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: var(--blue);
    }

    .kpi.green::before { background: var(--green); }
    .kpi.amber::before { background: var(--amber); }
    .kpi.red::before { background: var(--red); }

    .kpi-label {
        color: #667085;
        font-size: 0.62rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .kpi-value {
        color: #101828;
        font-size: 1.48rem;
        line-height: 1;
        font-weight: 800;
        letter-spacing: -0.035em;
        margin-top: 0.42rem;
    }

    .kpi-foot {
        color: #98a2b3;
        font-size: 0.61rem;
        margin-top: 0.35rem;
    }

    /* Section / panel */
    .section-title {
        color: #101828;
        font-size: 0.91rem;
        font-weight: 800;
        margin: 0.85rem 0 0.35rem 0;
    }

    .section-subtitle {
        color: #667085;
        font-size: 0.68rem;
        margin-top: -0.2rem;
        margin-bottom: 0.45rem;
    }

    .panel {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 9px;
        padding: 0.35rem 0.55rem 0.15rem 0.55rem;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.025);
    }

    .mini-stat {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 0.65rem 0.75rem;
        min-height: 70px;
    }

    .mini-label {
        color: #667085;
        font-size: 0.62rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .mini-value {
        color: #101828;
        font-size: 1.15rem;
        font-weight: 800;
        margin-top: 0.2rem;
    }

    .footer {
        color: #98a2b3;
        text-align: center;
        font-size: 0.62rem;
        margin-top: 1.2rem;
        padding-top: 0.7rem;
        border-top: 1px solid var(--line);
    }

    /* Streamlit widgets */
    div[data-testid="stMetric"] {
        background: #ffffff;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 8px;
    }

    div[data-baseweb="select"] > div {
        border-radius: 7px;
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


def kpi(label, value, foot="", accent="blue"):
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


def section(title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=300):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=12, r=12, t=25, b=8),
        paper_bgcolor="white",
        plot_bgcolor="white",

        # Explicit dark typography for readability on white charts
        font=dict(
            family="Inter",
            size=10,
            color="#344054",
        ),
        title=dict(
            font=dict(
                family="Inter",
                size=13,
                color="#101828",
            )
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#d0d5dd",
            font=dict(
                family="Inter",
                size=10,
                color="#101828",
            ),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            x=0,
            font=dict(
                family="Inter",
                size=9,
                color="#344054",
            ),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#d0d5dd",
        title=None,
        tickfont=dict(
            family="Inter",
            size=10,
            color="#475467",
        ),
        title_font=dict(
            family="Inter",
            size=10,
            color="#344054",
        ),
    )

    fig.update_yaxes(
        gridcolor="#eaecf0",
        zeroline=False,
        title=None,
        tickfont=dict(
            family="Inter",
            size=10,
            color="#475467",
        ),
        title_font=dict(
            family="Inter",
            size=10,
            color="#344054",
        ),
    )

    # Make bar/point labels readable instead of inheriting low-contrast defaults.
    fig.update_traces(
        textfont=dict(
            family="Inter",
            size=10,
            color="#344054",
        )
    )

    return fig


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">📡</div>
            <div class="brand-title">PRATAP</div>
            <div class="brand-subtitle">Rural Connectivity Analytics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown('<div class="side-heading">Dashboard</div>', unsafe_allow_html=True)

    page = st.radio(
        "Dashboard",
        ["Executive Overview", "Performance & Risk", "GP Explorer"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="side-heading">Filters</div>', unsafe_allow_html=True)

    circles = sorted(df["circle"].dropna().unique().tolist())

    selected_circles = st.multiselect(
        "Circle",
        circles,
        default=circles,
    )

    if selected_circles:
        district_options = sorted(
            df.loc[df["circle"].isin(selected_circles), "district"]
            .dropna()
            .unique()
            .tolist()
        )
    else:
        district_options = []

    selected_districts = st.multiselect(
        "District",
        district_options,
        default=[],
    )

    district_mask = (
        df["circle"].isin(selected_circles)
        if selected_circles
        else pd.Series(False, index=df.index)
    )

    if selected_districts:
        district_mask &= df["district"].isin(selected_districts)

    block_options = sorted(
        df.loc[district_mask, "block"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_blocks = st.multiselect(
        "Block",
        block_options,
        default=[],
    )

    working_mask = district_mask.copy()

    if selected_blocks:
        working_mask &= df["block"].isin(selected_blocks)

    gp_options = sorted(
        df.loc[working_mask, "gp_code"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_gps = st.multiselect(
        "GP / GP Code",
        gp_options,
        default=[],
        help="Leave empty to include all GPs in the current Circle / District / Block selection.",
    )

    hoto_options = sorted(
        df.loc[working_mask, "block_hoto_status"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_hoto = st.multiselect(
        "HOTO Status",
        hoto_options,
        default=[],
    )

    st.divider()

    st.markdown('<div class="side-heading">Dataset</div>', unsafe_allow_html=True)
    st.caption(f"{len(df):,} GP records")
    st.caption(f"{len(df.columns)} source columns")
    st.caption("Source: GP Wise Data")


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = df.copy()

if selected_circles:
    filtered = filtered[filtered["circle"].isin(selected_circles)]
else:
    filtered = filtered.iloc[0:0]

if selected_districts:
    filtered = filtered[filtered["district"].isin(selected_districts)]

if selected_blocks:
    filtered = filtered[filtered["block"].isin(selected_blocks)]

if selected_gps:
    filtered = filtered[filtered["gp_code"].astype(str).isin(selected_gps)]

if selected_hoto:
    filtered = filtered[
        filtered["block_hoto_status"].astype(str).isin(selected_hoto)
    ]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">
        <div>
            <div class="eyebrow">Operations Intelligence</div>
            <div class="page-title">Rural Connectivity Dashboard</div>
            <div class="page-subtitle">
                GP network coverage, HOTO, AMC and operational performance.
            </div>
        </div>
        <div class="data-status">● Live dashboard dataset</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_gps = int((filtered["gp_type"] == "Existing").sum())
hoto_done = int((filtered["block_hoto_status"] == "Done").sum())
amc_gps = int(filtered["amc_date"].notna().sum())

hoto_pct = (hoto_done / total_gps * 100) if total_gps else 0
amc_pct = (amc_gps / total_gps * 100) if total_gps else 0

uptime = (
    pd.to_numeric(filtered["oct-26"], errors="coerce")
    if "oct-26" in filtered.columns
    else pd.Series(dtype=float)
)

valid_uptime = uptime.dropna()

avg_uptime = valid_uptime.mean() if len(valid_uptime) else None
healthy_gps = int((valid_uptime >= 98).sum()) if len(valid_uptime) else 0
critical_gps = int((valid_uptime == 0).sum()) if len(valid_uptime) else 0
below85_gps = int((valid_uptime < 85).sum()) if len(valid_uptime) else 0


# ============================================================
# KPI ROW
# ============================================================

section("Network Snapshot", "Current values based on the selected filters")

k1, k2, k3, k4, k5, k6 = st.columns(6, gap="small")

with k1:
    kpi("Total GPs", fmt_num(total_gps), "Existing GP records", "blue")

with k2:
    kpi("HOTO Done", fmt_num(hoto_done), "HOTO status = Done", "green")

with k3:
    kpi("HOTO Completion", fmt_pct(hoto_pct), "Completed / selected GPs", "green")

with k4:
    kpi("AMC GPs", fmt_num(amc_gps), "AMC Date available", "amber")

with k5:
    kpi("AMC Coverage", fmt_pct(amc_pct), "AMC / selected GPs", "amber")

with k6:
    kpi(
        "Avg MTD Uptime",
        fmt_pct(avg_uptime) if avg_uptime is not None else "—",
        "Oct-26 GP uptime",
        "blue",
    )


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    section(
        "Network Performance",
        "Circle-level comparison of HOTO, AMC and network uptime",
    )

    # ---------------------------
    # Row 1: Circle charts
    # ---------------------------

    circle_summary = (
        filtered.groupby("circle")
        .agg(
            total_gps=("gp_code", "nunique"),
            hoto_done=("block_hoto_status", lambda x: (x == "Done").sum()),
            amc_gps=("amc_date", lambda x: x.notna().sum()),
        )
        .reset_index()
    )

    circle_summary["hoto_pct"] = (
        circle_summary["hoto_done"] / circle_summary["total_gps"] * 100
    )

    circle_summary["amc_pct"] = (
        circle_summary["amc_gps"] / circle_summary["total_gps"] * 100
    )

    c1, c2 = st.columns(2, gap="small")

    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        fig = px.bar(
            circle_summary,
            x="circle",
            y=["hoto_done", "amc_gps"],
            barmode="group",
            text_auto=".0f",
            labels={
                "circle": "",
                "value": "GPs",
                "variable": "",
            },
        )

        fig.for_each_trace(
            lambda trace: trace.update(
                name="HOTO Done" if trace.name == "hoto_done" else "AMC GPs"
            )
        )

        fig = chart_layout(fig, 285)
        fig.update_yaxes(title="GP Count")
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        uptime_state = (
            pd.DataFrame(
                {
                    "circle": filtered["circle"],
                    "uptime": uptime,
                }
            )
            .dropna()
            .groupby("circle", as_index=False)["uptime"]
            .mean()
        )

        fig = px.bar(
            uptime_state,
            x="circle",
            y="uptime",
            text="uptime",
            labels={"circle": "", "uptime": "Average uptime"},
        )

        fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
        )

        fig = chart_layout(fig, 285)
        fig.update_yaxes(title="Average uptime", range=[0, 100], ticksuffix="%")
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # Row 2: Uptime distribution + risk
    # ---------------------------

    section(
        "Operational Health",
        "Where the network is healthy and where attention is required",
    )

    c3, c4 = st.columns(2, gap="small")

    with c3:
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        if len(valid_uptime):
            bands = pd.cut(
                uptime,
                bins=[-0.001, 0, 85, 95, 98, 100.001],
                labels=["0%", ">0–85%", ">85–95%", ">95–98%", "≥98%"],
                include_lowest=True,
            )

            distribution = (
                pd.DataFrame(
                    {
                        "circle": filtered["circle"],
                        "band": bands,
                    }
                )
                .dropna()
                .groupby(["circle", "band"], observed=False)
                .size()
                .reset_index(name="GPs")
            )

            fig = px.bar(
                distribution,
                x="circle",
                y="GPs",
                color="band",
                barmode="stack",
                text_auto=True,
                labels={"circle": "", "band": "", "GPs": "GP Count"},
            )

            fig = chart_layout(fig, 300)
            fig.update_yaxes(title="GP Count")
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )
        else:
            st.info("No numeric Oct-26 uptime values are available.")

        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        risk = (
            filtered.groupby("circle")
            .agg(
                critical=("gp_code", lambda x: 0),
                below85=("gp_code", lambda x: 0),
            )
            .reset_index()
        )

        if len(filtered):
            risk = (
                pd.DataFrame(
                    {
                        "circle": filtered["circle"],
                        "uptime": uptime,
                    }
                )
                .groupby("circle", as_index=False)
                .agg(
                    critical=("uptime", lambda x: (x == 0).sum()),
                    below85=("uptime", lambda x: (x < 85).sum()),
                )
            )

        risk_long = risk.melt(
            id_vars="circle",
            value_vars=["critical", "below85"],
            var_name="risk",
            value_name="GPs",
        )

        risk_long["risk"] = risk_long["risk"].map(
            {
                "critical": "0% Uptime",
                "below85": "<85% Uptime",
            }
        )

        fig = px.bar(
            risk_long,
            x="GPs",
            y="circle",
            color="risk",
            barmode="group",
            orientation="h",
            text_auto=True,
            labels={"circle": "", "GPs": "GP Count", "risk": ""},
        )

        fig = chart_layout(fig, 300)
        fig.update_yaxes(title="")
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # Bottom-performing GP table
    # ---------------------------

    section(
        "Attention Required",
        "Lowest uptime GPs in the current filter selection",
    )

    if len(valid_uptime):
        bottom = filtered.copy()
        bottom["uptime_value"] = uptime

        bottom = bottom[
            [
                "gp",
                "gp_code",
                "circle",
                "district",
                "block",
                "block_hoto_status",
                "amc_date",
                "uptime_value",
            ]
        ].sort_values("uptime_value", ascending=True).head(10)

        bottom = bottom.rename(
            columns={
                "gp": "GP",
                "gp_code": "GP Code",
                "circle": "Circle",
                "district": "District",
                "block": "Block",
                "block_hoto_status": "HOTO",
                "amc_date": "AMC Date",
                "uptime_value": "Oct-26 Uptime",
            }
        )

        bottom["Oct-26 Uptime"] = bottom["Oct-26 Uptime"].map(
            lambda x: f"{x:.1f}%"
        )

        st.dataframe(
            bottom,
            use_container_width=True,
            hide_index=True,
            height=285,
        )


# ============================================================
# PERFORMANCE & RISK
# ============================================================

elif page == "Performance & Risk":

    section(
        "Performance & Risk",
        "Detailed operational view of uptime and network risk",
    )

    r1, r2, r3, r4 = st.columns(4, gap="small")

    with r1:
        kpi("≥98% Uptime", fmt_num(healthy_gps), "Healthy GP records", "green")

    with r2:
        kpi("0% Uptime", fmt_num(critical_gps), "Critical GP records", "red")

    with r3:
        kpi("<85% Uptime", fmt_num(below85_gps), "Attention required", "amber")

    with r4:
        kpi("AMC GPs", fmt_num(amc_gps), "Selected network", "blue")

    section(
        "Uptime Distribution",
        "GP-level Oct-26 uptime distribution",
    )

    if len(valid_uptime):
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
        )

        dist = (
            pd.DataFrame(
                {
                    "circle": filtered["circle"],
                    "band": bands,
                }
            )
            .dropna()
            .groupby(["circle", "band"], observed=False)
            .size()
            .reset_index(name="GPs")
        )

        fig = px.bar(
            dist,
            x="circle",
            y="GPs",
            color="band",
            barmode="stack",
            text_auto=True,
            labels={"circle": "", "band": "", "GPs": "GP Count"},
        )

        fig = chart_layout(fig, 390)
        fig.update_yaxes(title="GP Count")

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    section(
        "Circle Operational Summary",
        "HOTO, AMC and uptime metrics by Circle",
    )

    operational = (
        filtered.groupby("circle")
        .agg(
            GPs=("gp_code", "nunique"),
            HOTO_Done=("block_hoto_status", lambda x: (x == "Done").sum()),
            AMC_GPs=("amc_date", lambda x: x.notna().sum()),
            Avg_Uptime=("oct-26", lambda x: pd.to_numeric(x, errors="coerce").mean()),
        )
        .reset_index()
    )

    operational["HOTO %"] = (
        operational["HOTO_Done"] / operational["GPs"] * 100
    ).round(1)

    operational["AMC %"] = (
        operational["AMC_GPs"] / operational["GPs"] * 100
    ).round(1)

    operational["Avg Uptime"] = operational["Avg_Uptime"].map(
        lambda x: f"{x:.1f}%" if pd.notna(x) else "—"
    )

    operational = operational.drop(columns=["Avg_Uptime"])

    st.dataframe(
        operational.rename(columns={"circle": "Circle"}),
        use_container_width=True,
        hide_index=True,
        height=240,
        column_config={
            "HOTO %": st.column_config.ProgressColumn(
                "HOTO %",
                min_value=0,
                max_value=100,
                format="%.1f%%",
            ),
            "AMC %": st.column_config.ProgressColumn(
                "AMC %",
                min_value=0,
                max_value=100,
                format="%.1f%%",
            ),
        },
    )


# ============================================================
# GP EXPLORER
# ============================================================

else:

    section(
        "GP Data Explorer",
        "Search and inspect individual GP records using the active filters",
    )

    explorer_cols = [
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

    explorer_cols = [c for c in explorer_cols if c in filtered.columns]

    explorer = filtered[explorer_cols].copy()

    rename_map = {
        "circle": "Circle",
        "district": "District",
        "block": "Block",
        "gp": "GP",
        "gp_code": "GP Code",
        "block_hoto_status": "HOTO Status",
        "amc_date": "AMC Date",
        "total_rkm": "Total RKM",
        "oct-26": "Oct-26 Uptime",
    }

    explorer = explorer.rename(columns=rename_map)

    if "Oct-26 Uptime" in explorer.columns:
        explorer["Oct-26 Uptime"] = pd.to_numeric(
            explorer["Oct-26 Uptime"],
            errors="coerce",
        )

    st.caption(f"{len(explorer):,} records match the current filters.")

    st.dataframe(
        explorer,
        use_container_width=True,
        hide_index=True,
        height=560,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        PRATAP | Rural Connectivity Analytics | GP Wise Data
    </div>
    """,
    unsafe_allow_html=True,
)
