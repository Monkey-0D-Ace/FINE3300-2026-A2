import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data_frame = pd.read_csv("STATIC_INFLATIONCALC.csv", skiprows=8)
data_frame["date"] = pd.to_datetime(data_frame["date"])
data_frame["year"] = data_frame["date"].dt.year
data_frame["month"] = data_frame["date"].dt.month
data_frame["annual_change"] = data_frame["STATIC_INFLATIONCALC"].pct_change(periods=12) * 100


# CPI graphing
fig, ax = plt.subplots()

ax.plot(
    data_frame["date"],
    data_frame["STATIC_INFLATIONCALC"],
    label="CPI"
)

# Right-hand axis
ax2 = ax.twinx()

ax2.plot(
    data_frame["date"],
    data_frame["annual_change"],
    linestyle="--",
    label="Annual % Change"
)

# CPI base level
ax.axhline(
    y=100,
    linestyle=":",
    label="Base Level"
)

# Graph title and labels
ax.set_title("Canadian Consumer Price Index and Annual Percentage Change")
ax.set_xlabel("Date")
ax.set_ylabel("Consumer Price Index")
ax2.set_ylabel("Annual Percentage Change (%)")

# Legend
ax.legend(loc="upper left")
ax2.legend(loc="upper right")

# Saving graph
fig.savefig("CPI_Graph.png")


#print(data_frame.head()) - testing data frame
#print(data_frame.tail())
#print(data_frame.info())


price = float(input("Enter the price of goods or services: $"))

if price <= 0:
    print("Price must be greater than zero.")

else:
    first_date = input("Enter the first date (YYYY-MM): ")
    second_date = input("Enter the second date (YYYY-MM): ")

    if len(first_date) != 7 or first_date[4] != "-":
        print("First date must be entered in YYYY-MM format.")

    elif len(second_date) != 7 or second_date[4] != "-":
        print("Second date must be entered in YYYY-MM format.")

    elif first_date[0:4].isdigit() == False or first_date[5:7].isdigit() == False:
        print("First date must contain numbers in YYYY-MM format.")

    elif second_date[0:4].isdigit() == False or second_date[5:7].isdigit() == False:
        print("Second date must contain numbers in YYYY-MM format.")

    elif int(first_date[5:7]) < 1 or int(first_date[5:7]) > 12:
        print("First date month must be between 01 and 12.")

    elif int(second_date[5:7]) < 1 or int(second_date[5:7]) > 12:
        print("Second date month must be between 01 and 12.")

    else:
        first_date = pd.to_datetime(first_date + "-01")
        second_date = pd.to_datetime(second_date + "-01")

        if first_date < data_frame["date"].min() or first_date > data_frame["date"].max():
            print("First date is outside the available CPI data range.")

        elif second_date < data_frame["date"].min() or second_date > data_frame["date"].max():
            print("Second date is outside the available CPI data range.")

        elif second_date <= first_date:
            print("Second date must be later than the first date.")

        else:
            first_row = data_frame[data_frame["date"] == first_date]
            second_row = data_frame[data_frame["date"] == second_date]

            first_cpi = first_row["STATIC_INFLATIONCALC"].iloc[0]
            second_cpi = second_row["STATIC_INFLATIONCALC"].iloc[0]

            #print("First CPI:", first_cpi) - testing CPI values
            #print("Second CPI:", second_cpi) - testing CPI values

            equivalent_price = price * (second_cpi / first_cpi)

            percentage_change = ((second_cpi / first_cpi) - 1) * 100

            number_of_months = (
                (second_date.year - first_date.year) * 12
                + (second_date.month - first_date.month)
            )

            number_of_years = number_of_months / 12

            annual_rate = (
                np.power(
                    second_cpi / first_cpi,
                    1 / number_of_years
                ) - 1
            ) * 100


            print()
            print("Inflation Calculator Results")
            print("----------------------------")
            print(f"Original price: ${price:.2f}")
            print(f"Equivalent price: ${equivalent_price:.2f}")
            print(f"Percentage change: {percentage_change:.2f}%")
            print(f"Number of years: {number_of_years:.2f}")
            print(f"Annual rate of change: {annual_rate:.2f}%")
            print(f"First CPI: {first_cpi:.1f}")
            print(f"Second CPI: {second_cpi:.1f}")


plt.show()