count = 0


def quick_sort(array):
    global count
    count += 1
    if len(array) < 2:
        print(count)
        return array
    else:
        pivot = array[0]
        greater = [i for i in array[1:] if i > pivot]
        less = [i for i in array[1:] if i < pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)


array = [5, 6, 7, 4, 10, 3, 1, 4]
print(quick_sort(array))
