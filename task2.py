import random


def binary_float_search(arr, target):
    """
    Perform binary search for a floating-point target in a sorted list of floats.
    Returns loops count and "top margin"
    """
    low = 0
    high = len(arr) - 1
    loops = 0
    top_margin = None

    while low <= high:
        loops += 1
        mid = (low + high) // 2
        mid_value = arr[mid]

        if mid_value < target:
            low = mid + 1
        else:
            high = mid - 1
            top_margin = mid_value

    return loops, top_margin

def random_float_list(size, min_value=0.0, max_value=100.0):
    """Generate a sorted list of [size] random floating-point numbers."""
    return sorted([random.uniform(min_value, max_value) for _ in range(size)])


def main():
    size = 10
    random_floats = random_float_list(size)
    print("Sorted list of random floats:", random_floats)

    target = float(input("Enter a floating-point number to search for: "))
    loops, top_margin = binary_float_search(random_floats, target)
    print(f"Number of loops: {loops}")
    if top_margin is not None:
        print(f"Top margin (smallest number >= target): {top_margin}")
    else:
        print("No number in the list is greater than or equal to the target.")

if __name__ == "__main__":
    main()
