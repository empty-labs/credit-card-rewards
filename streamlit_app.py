# Local libraries
import Tools.rewards_utils as ru

# Third party packages
import streamlit as st


# Page config
st.set_page_config(
    page_title="Credit Card Rewards",
    layout="centered"
)

st.title("💳 Credit Card Rewards Explorer")

# Prep card options
data = ru.prep_benefits_data()

card_names = list(data["Card"])

selected_card = st.selectbox(
    "Select a credit card:",
    card_names
)

# Run simulation
run_button = st.button("Run Credit Card Rewards Explorer")

if run_button:
    st.subheader("Credit Card Rewards Results")

    with st.spinner("Simulating tournament..."):
        rewards = ru.determine_best_by_category(data)

    st.dataframe(rewards, width='content')
