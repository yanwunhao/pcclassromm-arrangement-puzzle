import csv
import random


def get_and_remove_random_element(input_list):
    if not input_list:  # Check if list is empty
        return None

    # Generate a random index
    random_index = random.randint(0, len(input_list) - 1)

    # Remove and return the element at random index
    return input_list.pop(random_index)


def csv_to_list(file_path):
    result_list = []

    with open(file_path, "r", newline="") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row:  # Check if row is not empty
                result_list.append(row[0])

    return result_list


if __name__ == "__main__":
    class1_list = csv_to_list("./data/class1.csv")
    class2_list = csv_to_list("./data/class2.csv")

    new_class1_list = []
    new_class2_list = []

    for item in class1_list:
        item = item + "_class1"
        new_class1_list.append(item)
    class1_list = new_class1_list
    for item in class2_list:
        item = item + "_class2"
        new_class2_list.append(item)
    class2_list = new_class2_list

    sitmap = []

    i = 0

    while class1_list or class2_list:
        line = []
        for j in range(6):
            if i % 2 == 0:
                if j % 2 == 0:
                    line.append(get_and_remove_random_element(class1_list))
                else:
                    line.append(get_and_remove_random_element(class2_list))
            else:
                if j % 2 == 0:
                    line.append(get_and_remove_random_element(class2_list))
                else:
                    line.append(get_and_remove_random_element(class1_list))
        sitmap.append(line)
        i += 1

    for row in sitmap[:11]:
        print(row)
    print("=================This is the walkway==================")
    for row in sitmap[12:]:
        print(row)
