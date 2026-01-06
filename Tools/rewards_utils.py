import pandas as pd

FILENAME = "Data/rewards_data.json"
META_COLS = ["Card", "Bank"]
DEFAULT_MONTHLY_SPENDING = {
    "Amazon.com": 200,
    "Amazon Fresh": 30,
    "Whole Foods": 50,
    "Restaurants": 200,
    "Gas": 250,
    "Transit": 100,
    "Travel": 250,
    "HEB Brand": 500,
    "Favor": 100,
    "Other": 1200
}


def prep_benefits_data():
    """Prepare credit card benefits data.

    Returns:
        data (pd.DataFrame): credit card benefits data frame
    """
    data = pd.read_json(FILENAME)

    # Resolve NaN's with Default value
    data = data.apply(
        lambda row: row.fillna(row["Default"]),
        axis=1
    )

    # Identify benefit columns
    benefit_cols = data.columns.difference(META_COLS)

    # Compute average benefit per card and sort
    data["Avg_Benefit"] = data[benefit_cols].mean(axis=1)
    data = data.sort_values(by="Avg_Benefit", ascending=False)

    return data


def select_remaining_cards(card_names: list, selected_cards: list):
    """Select remaining cards from data.

    Args:
        card_names (list): credit card list
        selected_cards (list): list of cards selected by user

    Returns:
        remaining_cards (list): remaining cards from credit card list
    """
    if type(selected_cards) != list:
        selected_cards = [selected_cards]

    remaining_cards = [c for c in card_names if c not in selected_cards and c != "None"]

    # Prepend "None" to the top
    remaining_cards = ["None"] + remaining_cards

    return remaining_cards


def find_tie_cards(row, data):
    """Find tie cards from data."""
    category = row["Category"]
    max_val = row["Max_Benefit"]

    # All cards in this category with Max_Benefit
    tied_cards = data.loc[data[category] == max_val, "Card"].tolist()

    # Remove the already-selected Best_Card
    tied_cards = [c for c in tied_cards if c != row["Best_Card"]]

    return tied_cards


def determine_best_by_category(data: pd.DataFrame, selected_cards: list):
    """Finds best credit card benefits based on category.

    Args:
        data (pd.DataFrame): credit card benefits data frame
        selected_cards (list): list of cards selected by user

    Returns:
        best_by_category (pd.DataFrame): Best benefits data frame
    """

    benefit_cols = data.columns.difference(META_COLS)
    data = data[data["Card"].isin(selected_cards)]

    best_by_category = None

    if all(c == "None" for c in selected_cards):
        return best_by_category

    # Compute max benefit per category
    max_per_category = data[benefit_cols].max()

    # Best card (arbitrary if tie, but OK for display)
    best_card_per_category = data.set_index("Card")[benefit_cols].idxmax()

    best_by_category = (
        best_card_per_category
        .to_frame(name="Best_Card")
        .reset_index()
        .rename(columns={"index": "Category"})
    )

    best_by_category["Max_Benefit"] = best_by_category["Category"].map(max_per_category)

    # Handle ties
    best_by_category["Tie_Cards"] = best_by_category.apply(
        lambda row: find_tie_cards(row, data),
        axis=1
    )

    # Re-format
    best_by_category = display_percentage(best_by_category, "Max_Benefit")

    return best_by_category


def display_dollar_amount(data: pd.DataFrame, col_name: str):
    """Display dollar amount of credit card benefits."""
    data[col_name] = data[col_name].map(lambda x: f"${x:,.0f}")
    return data


def display_percentage(data: pd.DataFrame, col_name: str):
    """Display percentage of credit card benefits."""
    data[col_name] = data[col_name].map(lambda x: f"{x:.2f}%")
    return data


def display_dollar_amounts(data: pd.DataFrame, columns: list):
    """Display dollar amounts based on columns."""
    for col in columns:
        data = display_dollar_amount(data, col)
    return data


def display_percentages(data: pd.DataFrame, columns: list):
    """Display percentages based on columns."""
    for col in columns:
        data = display_percentage(data, col)
    return data


def optimize_card_benefits(data: pd.DataFrame, monthly_spending: dict):
    """Optimize credit card benefits

    Args:
        data (pd.DataFrame): credit card benefits data frame
        monthly_spending (dict): dictionary of user monthly spending selection

    Returns:
        optimized_cards (pd.DataFrame): Best benefits data frame
    """

    spending = monthly_spending.copy()

    # Map user "Other" spending to card "Default"
    if "Other" in spending:
        spending["Default"] = spending.pop("Other")

    scores = []
    pct_savings = []

    for _, row in data.iterrows():
        total_reward = 0.0

        for category, amount in spending.items():
            if category in row:
                total_reward += amount * row[category] * 0.01  # Convert int amount to percentage
            else:
                # fallback to Default if category missing
                total_reward += amount * row["Default"] * 0.01  # Convert int amount to percentage

        scores.append(total_reward)
        pct_savings.append(100 * total_reward / sum(spending.values()))

    optimized_cards = data.copy()
    optimized_cards["Monthly_Value"] = scores
    optimized_cards["Annual_Value"] = optimized_cards["Monthly_Value"] * 12
    optimized_cards["Pct_Savings"] = pct_savings

    # Filter and sort by best value cards
    optimized_cards = optimized_cards.sort_values("Monthly_Value", ascending=False)
    optimized_cards = optimized_cards[["Card", "Bank", "Monthly_Value", "Annual_Value", "Pct_Savings"]]

    # Re-format value
    optimized_cards = display_dollar_amounts(optimized_cards, ["Monthly_Value", "Annual_Value"])
    optimized_cards = display_percentage(optimized_cards, "Pct_Savings")

    return optimized_cards
