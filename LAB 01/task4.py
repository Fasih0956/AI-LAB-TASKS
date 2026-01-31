def find_min(arr):
    min = arr[0]
    for i in range (0 , len(arr) , 1):
        if(arr[i] < min):
            min = arr[i]
        else:
            continue
    return min

def find_max(arr):
    max = arr[0]
    for i in range (0 , len(arr) , 1):
        if(arr[i] > max):
            max = arr[i]
        else:
            continue
    return max

arr = (1,4,10,19,7,8,2,100)
minval = find_min(arr)
maxval = find_max(arr)

print(f"Minimum value in list is: {minval}")
print(f"Maximum value in list is: {maxval}")




