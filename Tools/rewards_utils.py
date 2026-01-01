import pandas as pd

FILENAME = "Data/rewards_data.json"
META_COLS = ["Card", "Bank", "Default"]


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
        results (pd.DataFrame): Best benefits data frame
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

    return best_by_category
