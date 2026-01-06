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

st.header("Max Credit Card Rewards")
st.markdown("Use this tool to find which credit cards in your wallet yield the most rewards value by percentage.")

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

    with st.spinner("Calculating card benefits..."):
        best_by_category = ru.determine_best_by_category(data, selected_cards)

    if best_by_category is not None:
        st.dataframe(
            best_by_category,
            hide_index=True,
            width='content'
        )
    else:
        st.markdown("No cards selected.")

categories = list(ru.DEFAULT_MONTHLY_SPENDING.keys())
values = list(ru.DEFAULT_MONTHLY_SPENDING.values())
sub_categories = {i: [] for i in range(3)}  # Split into 3 columns by sub categories
sub_values = {i: [] for i in range(3)}

n = len(categories)
for i in range(n):
    if i % 3 == 0:
        sub_categories[0].append(categories[i])
        sub_values[0].append(values[i])
    if i % 3 == 1:
        sub_categories[1].append(categories[i])
        sub_values[1].append(values[i])
    if i % 3 == 2:
        sub_categories[2].append(categories[i])
        sub_values[2].append(values[i])

st.header("Optimal Card by Monthly Spending")
st.markdown("Use this tool to find the optimal credit card based on monthly spending habits.")

current_monthly_spending = {}
monthly_spending_values = []
cols = st.columns(3)
for i, col in enumerate(cols):
    with col:
        for j, sub in enumerate(sub_categories[i]):
            monthly_spending_values.append(st.number_input(
                label=f"{sub} Spending ($)",
                min_value=0,
                max_value=10000,
                step=1,
                value=sub_values[i][j],
                key=f"benefit_{sub}"
            ))
            current_monthly_spending[sub] = monthly_spending_values[-1]

st.markdown(f"## Total Monthly Spending: ${sum(monthly_spending_values)}")

# Run simulation
optimizer_run_button = st.button("Run Monthly Spending Optimizer")
if optimizer_run_button:
    st.subheader("Optimized Credit Card Spending by Monthly Rewards")

    with st.spinner("Calculating card benefits..."):
        optimized_cards = ru.optimize_card_benefits(data=data, monthly_spending=current_monthly_spending)

    if optimized_cards is not None:
        st.dataframe(
            optimized_cards,
            hide_index=True
        )

benefit_cols = data.columns.difference(ru.META_COLS)
formatted_data = ru.display_percentages(data, benefit_cols)

st.subheader("All Credit Card Rewards")
st.dataframe(formatted_data,
             hide_index=True,
             width='content')
