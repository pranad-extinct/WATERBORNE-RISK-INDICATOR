import streamlit as st

st.set_page_config(page_title="Water Contamination Risk Estimator")

st.title("Water Contamination Risk Estimation System")
st.markdown("### Indicator-Based Environmental Risk Assessment Model")

# -------------------- INPUT SECTION --------------------

water_source = st.selectbox(
    "Water Source Type",
    ["Groundwater", "Surface Water", "Municipal Supply", "Open Well"]
)

area_type = st.selectbox(
    "Area Type",
    ["Urban", "Semi-Urban", "Rural"]
)

sewage = st.selectbox(
    "Sewage System Condition",
    ["Good", "Moderate", "Poor"]
)

flooding = st.selectbox(
    "Flooding Frequency",
    ["Rare", "Seasonal", "Frequent"]
)

population = st.selectbox(
    "Population Density",
    ["Low", "Moderate", "High"]
)

# -------------------- SCORING MATRICES --------------------

water_matrix = {
    "Groundwater": (1, 3, 2, 1),
    "Surface Water": (4, 3, 3, 2),
    "Municipal Supply": (2, 1, 2, 2),
    "Open Well": (4, 2, 1, 1)
}

area_matrix = {
    "Urban": (2, 1, 4, 4),
    "Semi-Urban": (2, 2, 2, 2),
    "Rural": (2, 4, 1, 1)
}

sewage_matrix = {
    "Good": (1, 0, 0, 1),
    "Moderate": (3, 0, 0, 2),
    "Poor": (4, 0, 0, 3)
}

flooding_matrix = {
    "Rare": (1, 1, 1, 1),
    "Seasonal": (3, 3, 2, 2),
    "Frequent": (4, 4, 3, 3)
}

population_matrix = {
    "Low": (1, 2, 1, 1),
    "Moderate": (2, 2, 2, 2),
    "High": (4, 1, 3, 4)
}

# -------------------- CALCULATION --------------------

if st.button("Estimate Risk"):

    microbial = 0
    agricultural = 0
    industrial = 0
    pharmaceutical = 0

    for matrix, choice in [
        (water_matrix, water_source),
        (area_matrix, area_type),
        (sewage_matrix, sewage),
        (flooding_matrix, flooding),
        (population_matrix, population)
    ]:
        m, a, i, p = matrix[choice]
        microbial += m
        agricultural += a
        industrial += i
        pharmaceutical += p

    total_score = microbial + agricultural + industrial + pharmaceutical

    if total_score == 0:
        st.error("Invalid input combination.")
    else:

        # Category Percentages
        microbial_pct = round((microbial / total_score) * 100, 2)
        agricultural_pct = round((agricultural / total_score) * 100, 2)
        industrial_pct = round((industrial / total_score) * 100, 2)
        pharmaceutical_pct = round((pharmaceutical / total_score) * 100, 2)

        # Overall Water Quality Index (0–1 scale)
        MAX_TOTAL_SCORE = 80
        overall_index = round(total_score / MAX_TOTAL_SCORE, 4)

        results = {
            "Microbial Contamination": microbial_pct,
            "Agricultural Chemical Contamination": agricultural_pct,
            "Industrial Chemical Contamination": industrial_pct,
            "Pharmaceutical / Emerging Contaminant Risk": pharmaceutical_pct
        }

        dominant = max(results, key=results.get)

        st.markdown("## Contamination Probability Distribution (%)")
        for category, value in results.items():
            st.write(f"{category}: {value}%")

        st.markdown("## Dominant Risk Category")
        st.success(dominant)

        st.markdown("## Overall Water Quality Risk Index (0–1 Scale)")
        st.info(f"Overall Risk Index: {overall_index}")

        st.markdown("---")
        st.caption(
            "Disclaimer: This model provides a weighted probabilistic environmental "
            "risk estimation based on predefined indicator scoring. It does not "
            "guarantee laboratory-confirmed water quality results. Actual contamination "
            "levels must be verified through chemical and microbiological testing."
        )
