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

    remaining_cards = [c for c in card_names if c not in selected_cards or c == "None"]
    remaining_cards = list(set(remaining_cards))

    return remaining_cards

def determine_best_by_category(data: pd.DataFrame, selected_cards: list):
    """Finds best credit card benefits based on category.

    Args:
        data (pd.DataFrame): credit card benefits data frame
        selected_cards (list): list of cards selected by user

    Returns:
        results (pd.DataFrame): Best benefits data frame
    """

    benefit_cols = data.columns.difference(META_COLS)  # All card benefit options
    data = data[data["Card"].isin(selected_cards)]

    best_by_category = None

    if all(c == "None" for c in selected_cards):

        return best_by_category

    else:

        best_by_category = (
            data
            .set_index("Card")[benefit_cols]
            .idxmax()
            .to_frame(name="Best_Card")
        )

        best_by_category["Max_Benefit"] = (
            data
            .set_index("Card")[benefit_cols]
            .max()
        )

        best_by_category = best_by_category.reset_index().rename(
            columns={"index": "Category"}
        )

        return best_by_category
