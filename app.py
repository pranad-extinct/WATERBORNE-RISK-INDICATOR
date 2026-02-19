import streamlit as st

st.set_page_config(page_title="Waterborne Risk Estimator", layout="centered")

st.title("🌊 Waterborne Risk Estimator")
st.write("Estimate waterborne health risk using weighted environmental indicators.")

st.markdown("---")

# INPUTS
area = st.selectbox(
    "Area Type",
    ["Rural", "Semi-Urban", "Urban", "Industrial"]
)

water = st.selectbox(
    "Water Source Quality",
    ["Clean", "Moderate", "Contaminated"]
)

sewage = st.selectbox(
    "Sewage System Condition",
    ["Good", "Moderate", "Poor"]
)

flood = st.selectbox(
    "Flooding Frequency",
    ["Rare", "Seasonal", "Frequent"]
)

population = st.selectbox(
    "Population Density",
    ["Low", "Medium", "High"]
)

st.markdown("---")

if st.button("Calculate Risk Score"):

    # Base numeric mapping
    values = {
        "Clean": 0.2, "Moderate": 0.6, "Contaminated": 1.0,
        "Good": 0.2, "Poor": 1.0,
        "Rare": 0.2, "Seasonal": 0.6, "Frequent": 1.0,
        "Low": 0.3, "Medium": 0.6, "High": 1.0
    }

    water_val = values[water]
    sewage_val = values[sewage]
    flood_val = values[flood]
    population_val = values[population]

    # Area-specific logic
    if area == "Rural":
        area_val = 0.6   # fertilizer & runoff risk
    elif area == "Semi-Urban":
        area_val = 0.5
    elif area == "Urban":
        area_val = 0.7   # sewage & density
    elif area == "Industrial":
        area_val = 1.0   # chemical discharge

    # Weights (Normalized Model)
    w_area = 0.25
    w_water = 0.25
    w_sewage = 0.25
    w_flood = 0.15
    w_population = 0.10

    risk_score = (
        area_val * w_area +
        water_val * w_water +
        sewage_val * w_sewage +
        flood_val * w_flood +
        population_val * w_population
    )

    # Risk Level
    if risk_score < 0.33:
        level = "Low Risk"
        color = "green"
    elif risk_score < 0.66:
        level = "Moderate Risk"
        color = "orange"
    else:
        level = "High Risk"
        color = "red"

    # Dominant Factor
    contributions = {
        "Area Type": area_val * w_area,
        "Water Source": water_val * w_water,
        "Sewage System": sewage_val * w_sewage,
        "Flooding": flood_val * w_flood,
        "Population Density": population_val * w_population
    }

    dominant = max(contributions, key=contributions.get)

    st.subheader("Results")

    st.metric("Final Risk Score (0–1 Scale)", round(risk_score, 3))
    st.markdown(f"### Risk Level: :{color}[{level}]")
    st.write(f"Dominant Risk Driver: **{dominant}**")

    st.progress(risk_score)

    st.markdown("---")
    st.caption("This estimator provides theoretical risk scoring for research and educational purposes only.")
