import math

def check_till(number, check_max, prime_list):
    for i in range(2, int(math.sqrt(number)) + 1):
        if prime_list[i-1]:
            start_value = i * i
            if start_value <= check_max:
                start_value = (check_max // i + 1) * i
            start_value = max(start_value, i * i)
            for multiple in range(start_value, number + 1, i):
                prime_list[multiple-1] = False
    return number

def print_command(number, prime_list):
    if prime_list[number-1]:
        print("I LOVE PCLUB")
    else:
        print("I AM NOOB")

if __name__ == "__main__":
    number_of_entries = int(input())
    list_of_entries = []
    max_in_entries = 0
    for i in range(number_of_entries):
        list_of_entries.append(int(input()))
        if list_of_entries[i] > max_in_entries:
            max_in_entries = list_of_entries[i]
    max_checked = int(0)
    list_of_numbers = [True]*max_in_entries
    list_of_numbers[0] = False
    for i in list_of_entries:
        if i > max_checked:
            max_checked = check_till(i, max_checked, list_of_numbers)
        print_command(i, list_of_numbers)