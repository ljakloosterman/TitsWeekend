"""Script to show payment progress"""
import datetime
import pandas as pd
import streamlit as st

from streamlit.components.v1 import html


def open_page():
    url = "https://www.ing.nl/payreq/m/?trxid=qHXrcxrMH5kKrcKxMOcPTjOPXWWaVAvT"

    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)


def get_months():
    """Get months until october 2025"""

    # Get current date
    today = datetime.datetime.now()

    # Get months until october 2025
    end = datetime.datetime(2025, 10, 1)
    return (end.year - today.year) * 12 + end.month - today.month


def add_transaction(transactions, tit, value):
    """Adds transaction and updates json"""

    # Add new transaction
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    new_transaction = pd.DataFrame({
        "Datum": [today],
        "Tit": [tit],
        "Bedrag": [value]
    })
    transactions = pd.concat([transactions, new_transaction])

    # Save transactions as json
    transactions.to_json("transactions.json", orient='records', indent=4)


def main():
    """Main function of the script"""

    # Load transactions
    transactions = pd.read_json("transactions.json")

    # Get remaining months untill october 2025
    months = get_months()

    # Define tits
    tits = [
        "Stan",
        "Roeland",
        "Michiel",
        "Joost",
        "Mees",
        "Yasper",
        "Vincent",
        "Bart",
        "Gijs",
        "Ernst",
        "Sam",
        "Nout",
        "Max",
        "Luc"
        ]

    # Set goals
    goal_pp = (13 - months) * 50
    goal = 12*50*len(tits)

    # Get total money saved
    total = transactions["Bedrag"].sum()

    # Show title
    st.title("Titsweekend betalingsoverzicht 💸")

    # Show total progressbar
    st.markdown("### Totaal gepayerd")
    st.progress(total/goal, f"€ {total},- ingelegd")

    # Show individual metrics
    st.markdown("### Individueel gepayerd")
    for tit in tits:
        col1, col2, col3 = st.columns(3)

        # Column for status
        with col1:
            total_pp = transactions.loc[
                transactions["Tit"] == tit, "Bedrag"
            ].sum()
            delta = total_pp - goal_pp
            st.metric(
                label=tit,
                value=f"€ {total_pp},-",
                delta=float(delta))

        # Column to add transactions
        with col2:
            value = st.number_input(
                "Nieuwe betaling:",
                key=f"value{tit}",
                step=1.0,
                min_value=50.0,
                max_value=600.0
                )

        with col3:
            if st.button('Betalen met je bek', on_click=open_page, key=f"button_{tit}"):
                add_transaction(transactions, tit, value)

        # Divider for clarity
        st.divider()

    # Show transactions
    st.markdown("### Transacties")
    st.dataframe(
        transactions,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Bedrag": st.column_config.NumberColumn(format="€%d")
        },
    )

if __name__ == "__main__":
    main()
