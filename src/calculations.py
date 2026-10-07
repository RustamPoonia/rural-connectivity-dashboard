import pandas as pd


# ============================================================
# OVERVIEW KPIs
# ============================================================

def get_overview_kpis(df):
    """
    Calculate the main dashboard KPIs.
    """

    # Total Existing GPs
    total_existing_gps = (
        df["gp_type"] == "Existing"
    ).sum()

    # Revised Existing GPs
    revised_existing_gps = (
        (df["gp_type"] == "Existing") &
        (df["converted_to_np_&_closed"].isna())
    ).sum()

    # HOTO Done GPs
    hoto_done_gps = (
        df["block_hoto_status"] == "Done"
    ).sum()

    # AMC GPs
    amc_gps = (
        df["amc_date"].notna()
    ).sum()

    # HOTO %
    hoto_percentage = (
        hoto_done_gps / 15978 * 100
        if 15978 > 0
        else 0
    )

    # AMC %
    amc_percentage = (
        amc_gps / 15978 * 100
        if 15978 > 0
        else 0
    )

    # AMC Fibre RKM
    amc_fibre_rkm = df.loc[
        df["amc_date"].notna(),
        "total_rkm"
    ].sum()

    return {
        "total_existing_gps": int(total_existing_gps),
        "revised_existing_gps": int(revised_existing_gps),
        "hoto_done_gps": int(hoto_done_gps),
        "hoto_percentage": float(hoto_percentage),
        "amc_gps": int(amc_gps),
        "amc_percentage": float(amc_percentage),
        "amc_fibre_rkm": float(amc_fibre_rkm),
    }


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def calculate_all_kpis(df):
    """
    Compatibility wrapper.
    """
    return get_overview_kpis(df)


# ============================================================
# STATE SUMMARY
# ============================================================

def get_state_summary(df):
    """
    Calculate GP, HOTO and AMC metrics by state.
    """

    return (
        df.groupby("circle")
        .agg(
            existing_gps=(
                "gp_code",
                "nunique"
            ),

            hoto_done_gps=(
                "block_hoto_status",
                lambda x: (x == "Done").sum()
            ),

            amc_gps=(
                "amc_date",
                lambda x: x.notna().sum()
            ),
        )
        .reset_index()
    )


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def calculate_state_summary(df):
    """
    Compatibility wrapper for app.py.
    """
    return get_state_summary(df)


# ============================================================
# PERFORMANCE KPIs
# ============================================================

def get_performance_kpis(df):
    """
    Calculate basic performance KPIs.
    """

    hoto_done_gps = (
        df["block_hoto_status"] == "Done"
    ).sum()

    amc_gps = (
        df["amc_date"].notna()
    ).sum()

    amc_fibre_rkm = df.loc[
        df["amc_date"].notna(),
        "total_rkm"
    ].sum()

    return {
        "hoto_done_gps": int(hoto_done_gps),
        "amc_gps": int(amc_gps),
        "amc_fibre_rkm": float(amc_fibre_rkm),
    }