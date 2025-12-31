# Local libraries
import Tools.rewards_utils as ru

# Third party packages
import streamlit as st


# Page config
st.set_page_config(
    page_title="March Madness Bracketology",
    layout="centered"
)

st.title("💳 Credit Card Rewards Explorer")

# Prep card options
data = ru.prep_benefits_data()
best_by_category = ru.determine_best_by_category(data)

card_names = list(data["Card"])

selected_card = st.selectbox(
    "Select a credit card:",
    card_names
)