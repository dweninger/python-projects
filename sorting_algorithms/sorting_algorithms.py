import random

def bubble_sort(arr, visualize=False):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                if visualize:
                    print(f"Step {i + 1}, Pass {j + 1}: {arr}")

def selection_sort(arr, visualize=False):
    for i in range(len(arr)):
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
        if visualize:
            print(f"Step {i + 1}: {arr}")

def insertion_sort(arr, visualize=False):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            if visualize:
                print(f"Step {i}: {arr}")
            j -= 1
        arr[j + 1] = key
    if visualize:
        print(f"Sorted List: {arr}")

def merge_sort(arr, visualize=False):
    if len(arr) <= 1:
        return arr

    if visualize:
        print(f"Split: {arr}")

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = merge_sort(left_half, visualize)
    right_half = merge_sort(right_half, visualize)

    i = j = k = 0

    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

    if visualize:
        print(f"Merge: {arr}")

    return arr

def quick_sort(arr, visualize=False):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if x <= pivot]
        greater_than_pivot = [x for x in arr[1:] if x > pivot]

        if visualize:
            print(f"Array: {arr}")
            print(f"Pivot: {pivot}")
            print(f"Less than Pivot: {less_than_pivot}")
            print(f"Greater than Pivot: {greater_than_pivot}")

        sorted_less = quick_sort(less_than_pivot, visualize)
        sorted_greater = quick_sort(greater_than_pivot, visualize)
        sorted_array = sorted_less + [pivot] + sorted_greater
        
        if visualize:
            print(f"Sorted Array: {sorted_array}")
        
        return sorted_array

# main loop
use_visualizer = False
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Python Sorter!")
while(True):
    # Shuffle the number array so it can be sorted
    random.shuffle(arr)
    print("Here is your scrambled list of numbers: [" + ", ".join(map(str, arr)) + "]")
    print("Which sorting algorithm do you want to use?\nPlease enter a number. Enter q to quit.")
    algorithm = input(" 1) Bubble Sort\n"
        " 2) Selection Sort\n"
        " 3) Insertion Sort\n"
        " 4) Merge Sort\n"
        " 5) Quick Sort\n"
        "  > ")
    # if q is entered, quit
    if algorithm.lower() == "q":
        break
    # store the input as an int
    algorithm = int(algorithm)
    # print the steps of the sorting algorithm?
    visualizer_input = input("Visualizer? Y/N\n"
        "  > ")

    # Turn visualizer input to boolean
    if visualizer_input.lower() == "y":
        use_visualizer = True
    else:
        use_visualizer = False
    # use sorting algorithm
    if algorithm == 1:
        bubble_sort(arr, use_visualizer)
    elif algorithm == 2:
        selection_sort(arr, use_visualizer)
    elif algorithm == 3:
        insertion_sort(arr, use_visualizer)
    elif algorithm == 4:
        arr = merge_sort(arr, use_visualizer)
    elif algorithm == 5:
        arr = quick_sort(arr, use_visualizer)
    else:
        print("Incorrect selection")
    # print the sorted array if the visualizer is off
    if not use_visualizer:
        print(arr)
    # visually separate sort
    print("\n---------------------\n")
