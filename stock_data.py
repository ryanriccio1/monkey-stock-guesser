import random
try:
    from tabulate import tabulate
    tabulate_exists = True
except ModuleNotFoundError:
    tabulate_exists = False


# data structure for a single stock
class SingleStockData(object):
    def __init__(self, name, yearly_low, yearly_high) -> None:
        self._name = name
        self._yearly_low = yearly_low
        self._yearly_high = yearly_high

    # simple getters to encourage safe OOP
    def get_name(self):
        return self._name

    def get_low(self):
        return self._yearly_low

    def get_high(self):
        return self._yearly_high


# store the entire valid NASDAQ table
class NASDAQStockData(object):
    def __init__(self) -> None:
        self._stock_data = []
        self._num_stocks = 0

    def process_file(self, file_name) -> bool:
        # open file
        with open(file_name, 'r') as file:
            # priming read
            current_line = file.readline()
            while current_line:
                # separate into values
                split_line = current_line.split(",")
                name, low, high = split_line[0], float(split_line[1]), float(split_line[2])
                # append the stock data
                self._stock_data.append(SingleStockData(name, low, high))
                current_line = file.readline()
                self._num_stocks += 1
        return True

    def display_file(self) -> None:
        table_data = []
        headers = ["Count", "Name", "Low", "High"]
        # add a count to each stock
        for count, stock in enumerate(self._stock_data):
            # pull stock from index table
            current_stock = self._stock_data[count]
            # add the stock data to a new list to make easier to tabulate
            table_data.append([f"# {count+1}", current_stock.get_name(),
                               current_stock.get_low(), current_stock.get_high()])
        if tabulate_exists:
            # use tabulate (pretty print)
            print(tabulate(table_data, headers, tablefmt="grid", floatfmt=".2f"))
        else:
            # tabulate does not exist, brute force the printing
            for current_item in table_data:
                print(f'{current_item[0]}. {current_item[1]}\t\t${current_item[2]:.2f}\t\t${current_item[3]:.2f}')

    # simple getter
    def get_num_stocks(self):
        return self._num_stocks

    def calculate_random_gain(self, number_of_stocks=1, print_stocks=False):
        random_stocks = []  # to store the stocks
        tabulate_data = []  # to store data from the stocks
        headers = ["Name", "Low", "High"]   # labels
        # pick x amount of random stocks and add to list
        for x in range(number_of_stocks):
            random_index = random.randint(1, self._num_stocks) - 1
            random_stocks.append(self._stock_data[random_index])

        low_value = 0
        high_value = 0
        # loop through each stock and keep a running record of highs and lows
        for stock in random_stocks:
            tabulate_data.append([stock.get_name(), stock.get_low(), stock.get_high()])
            low_value += stock.get_low()
            high_value += stock.get_high()

        if print_stocks:
            if tabulate_exists:
                # pretty print using tabulate
                print(tabulate(tabulate_data, headers, tablefmt="grid", floatfmt=".2f"))
            else:
                # brute force table data
                for current_item in random_stocks:
                    print(f'{current_item.get_name()}\t\t${current_item.get_low():.2f}'
                          f'\t\t${current_item.get_high():.2f}')

        # calculate monetary gain and percent gain
        gain = high_value - low_value
        percent_gain = gain / low_value
        return [low_value, high_value, gain, percent_gain]
