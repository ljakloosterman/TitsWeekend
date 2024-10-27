"""Script to show payment progress"""
import datetime
import pandas as pd
import streamlit as st


def main():
    """Main function of the script"""

    # Load data
    data = pd.read_csv("overview.csv", delimiter=",", index_col=0)

    # Get remaining months untill october 2025
    today = datetime.datetime.now()
    end = datetime.datetime(2025, 10, 1)
    months = (end.year - today.year) * 12 + end.month - today.month

    # Set goals
    goal_pp = (13 - months) * 50
    goal = 12*50*len(data.columns)

    # Calculate total
    total_pp = data.sum(axis=0)
    total = total_pp.sum()

    # Show title
    st.title("Titsweekend betalingsoverzicht 💸")

    # Show total progressbar
    st.markdown("### Totaal gepayerd")
    st.progress(total/goal, f"{(total/goal)*100:.2f}% ingelegd")

    # Show individual metrics
    st.markdown("### Individueel gepayerd")
    for tit in data.columns:
        delta = total_pp[tit] - goal_pp
        st.metric(
            label=tit,
            value=f"€ {total_pp[tit]},-",
            delta=float(delta))

    # Show table
    st.markdown("### Transacties")
    st.dataframe(data)

if __name__ == "__main__":
    main()
