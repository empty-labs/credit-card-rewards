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


def determine_best_by_category(data: pd.DataFrame):
    """Finds best credit card benefits based on category.

    Args:
        data (pd.DataFrame): credit card benefits data frame

    Returns:
        results (pd.DataFrame): Best benefits data frame
    """

    benefit_cols = data.columns.difference(META_COLS)

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


