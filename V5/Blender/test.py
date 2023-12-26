shape_list = [0, 0.2, 0.4, 0.9]

def all_values_below_threshold(lst, threshold):
    return all(value < threshold for value in lst)

print(all_values_below_threshold(shape_list, 0.99))