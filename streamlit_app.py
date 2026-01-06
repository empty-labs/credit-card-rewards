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

card_names = ["None"] + list(data["Card"])
selected_cards = []

cols = st.columns(3)
for i, col in enumerate(cols):
    with col:
        selected_cards.append(st.selectbox(
            f"Credit card #{i+1}:",
            card_names,
            index=0
        ))
        card_names = ru.select_remaining_cards(card_names, selected_cards)

# Run simulation
run_button = st.button("Run Credit Card Rewards Explorer")

if run_button:
    st.subheader("Selected Credit Card Rewards Results")

    with st.spinner("Simulating tournament..."):
        rewards = ru.determine_best_by_category(data, selected_cards)

    if rewards is not None:
        # st.dataframe(rewards, width='content')
        st.dataframe(
            rewards,
            column_config={
                "Max_Benefit": st.column_config.NumberColumn(
                    "Max Benefit",
                    format="%.0f%%"
                )
            },
            width='content'
        )
    else:
        st.markdown("No cards selected.")


st.subheader("All Credit Card Rewards")
st.dataframe(data, width='content')
