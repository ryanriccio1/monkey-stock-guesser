# Objectives list
# Import Spreadsheet of at least 3000 companies and their end of the year stock prices
# Pick 500 at random and compare to the S&P 500 over the period of multiple years to see if the S&P 500


# this imports all of our resources for the rest of the code
import random
import os
import time
try:
    import matplotlib.pyplot as plt
    matplotlib_exists = True
except ModuleNotFoundError:
    matplotlib_exists = False
from stock_data import NASDAQStockData

# consts
SP500_high = 3978.73
SP500_low = 4195.99
SP500_percent_gain = (SP500_high - SP500_low) / SP500_low


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# makes a dart fly
def draw_dart():
    for spaces in range(125, -1, -1):
        time.sleep(0.001)
        clear()
        print("|" + spaces * " " + "<")


# def plot_pie(low, gain):
#     labels = ["Initial", "Post-Gain"]
#     sizes = [low, gain]
#     explode = (0, 0.1)
#     fig1, ax1 = plt.subplots()
#     ax1.pie(sizes, explode=explode, labels=labels,
#             shadow=True, startangle=90)
#     ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     plt.title('Average Gain')
#     plt.show()


def plot_hist(percent_gain):
    # the histogram of the data
    n, bins, patches = plt.hist(percent_gain, 20, density=1, facecolor='g', alpha=0.75,
                                linewidth=0.5, edgecolor="white")

    plt.title('Histogram of Stock Gains')
    plt.axis([-2, 2, 0, 2])
    plt.xlabel("Gain (%)")
    plt.ylabel("Distribution")
    plt.grid(True)
    plt.plot([SP500_percent_gain, SP500_percent_gain], [0, 4], '--')
    plt.text(.3, 1.75, f"S&P 500 = {SP500_percent_gain*100:.2f}%")
    plt.show()


def single_index(all_stock_data, num_iterations=1):
    # get data from x random guesses then display data
    low, high, gain, percent_gain = all_stock_data.\
        calculate_random_gain(number_of_stocks=num_iterations, print_stocks=True)
    print(f"Gain:\t\t\t${gain:.2f}")
    print(f"Percent Gain:\t\t{percent_gain * 100:.2f}%")
    print(f"S&P500 Gain:\t\t{SP500_percent_gain * 100:.2f}%")
    if percent_gain < SP500_percent_gain:
        print('\033[91m' + '\033[1m' + 'NOT SUCCESSFUL' + '\033[0m')
    else:
        print('\033[92m' + '\033[1m' + 'SUCCESSFUL' + '\033[0m')
    return low, high, gain, percent_gain


def main():
    random.seed(time.time())
    clear()
    print("Please maximize your window!")
    time.sleep(3)
    clear()
    # printing a monkey
    # Here we need to print an ASCII monkey

    print("""
           __,__
  .--.  .-"     "-.  .--.
 / .. \/  .-. .-.  \/ .. \\
| |  '|  /   Y   \  |'  | |
| \   \  \ 0 | 0 /  /   / |
 \ '- ,\.-"`` ``"-./, -' /
  `'-' /_   ^ ^   _\ '-'`
      |  \._   _./  |
      \   \ `~` /   /
       '._ '-=-' _.'
          '~---~'
          """)

    input("Press enter to make the monkey throw the dart")
    draw_dart()
    time.sleep(2)

    all_stock_data = NASDAQStockData()
    all_stock_data.process_file("stockdata.csv")

    while True:
        clear()
        # only compare a single stock to see its gain compared to S&P
        single_stock = input("Would you like to compare a single stock (y or n): ").lower()
        if single_stock == 'y':
            low, high, gain, percent_gain = single_index(all_stock_data)
            if matplotlib_exists:
                # plot_pie(low, gain)
                pass

        # compare multiple stocks with its gain compared to S&P
        else:
            stocks_per_iteration = int(input("How many stocks per iteration (2+, 10 works well): "))
            num_iterations = int(input("How many iterations: "))

            # if the simulation only occurs once
            if num_iterations == 1:
                single_index(all_stock_data, stocks_per_iteration)
            else:   # if the simulation occurs multiple times
                hist_data = []
                successful_investments = 0
                # loop through each iteration, get its data, compare it to S&P, and keep running record of success
                for x in range(num_iterations):
                    a, b, c, percent_gain = all_stock_data.calculate_random_gain(number_of_stocks=stocks_per_iteration)
                    hist_data.append(percent_gain)
                    if percent_gain > SP500_percent_gain:
                        successful_investments += 1
                print(f"There were {successful_investments} successful investment ventures out of "
                      f"{num_iterations} total guesses. The monkey's random choice of {stocks_per_iteration} stocks "
                      f"was more successful {(successful_investments/num_iterations)*100:.2f}% of the time.")
                if matplotlib_exists:
                    plot_hist(hist_data)
        more_stocks = input("Would you like to continue (y or n): ").lower()
        if more_stocks == 'n':
            break


# only run this if it is not a module
if __name__ == "__main__":
    main()
