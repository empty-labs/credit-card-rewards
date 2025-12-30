# Credit Card Rewards

This project is a resource for optimizing reward benefits based on your credit card portfolio.

# Streamlit App Link
TODO: Swap link for new streamlit app

[College Hoops Streamlit](https://credit-card-rewards-bjkxnhdsnkr2n6vrs9bkxg.streamlit.app/)

## Conda environment

When setting up the project, consider using a conda environment to isolate the required packages.

1. Create new conda environment (you can also use PyCharm's interpreter settings to create your conda environment instead of using command line here)
```commandline
conda env create --name credit-card-rewards
```
2. Add packages to conda
```commandline
conda install anaconda::pandas -y
conda install conda-forge::streamlit -y
```
3. Set up jupyter for conda environment ([sauce](https://stackoverflow.com/questions/39604271/conda-environments-not-showing-up-in-jupyter-notebook))
```commandline
pip install jupyter ipykernel
```
```commandline
python -m ipykernel install --user --name credit-card-rewards --display-name "credit-card-rewards"
```

## Streamlit Deployment
1. Create requirements list.  Prune as needed.
```commandline
pip list --format=freeze > requirements.txt
```
2. Test minimal environment
```commandline
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
3. Delete test environment
```commandline
deactivate
rm -rf test_env
```