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
selected_cards = []

selected_card_1 = st.selectbox(
    "Select credit card #1:",
    card_names
)

selected_cards.append(selected_card_1)
remaining_cards_2 = ru.select_remaining_cards(card_names, selected_cards)

selected_card_2 = st.selectbox(
    "Select credit card #2:",
    remaining_cards_2
)

selected_cards.append(selected_card_2)
remaining_cards_3 = ru.select_remaining_cards(card_names, selected_cards)

selected_card_3 = st.selectbox(
    "Select credit card #3:",
    remaining_cards_3
)

selected_cards = [selected_card_1, selected_card_2, selected_card_3]

# Run simulation
run_button = st.button("Run Credit Card Rewards Explorer")

if run_button:
    st.subheader("Credit Card Rewards Results")

    with st.spinner("Simulating tournament..."):
        rewards = ru.determine_best_by_category(data, selected_cards)

    st.dataframe(rewards, width='content')
