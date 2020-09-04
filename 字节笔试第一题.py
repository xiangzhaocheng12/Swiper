def my_func(a:list, b:list):
    #   [9,7,6,5,4,3,1]
    #   [11,6,5,3,2]
    index_a = 0
    index_b = 0
    res = []
    count = 0
    while True:
        # 首先对越界进行限制
        if index_a == len(a):
            res = res + b[index_b:]
            break
        if index_b == len(b):
            res = res + a[index_a:]
            break

        # 逐个对列表的每一个元素进行比对, 大的放到 res 里面
        if a[index_a] > b[index_b]:
            res.append(a[index_a])
            index_a += 1
        elif a[index_a] < b[index_b]:
            res.append(b[index_b])
            index_b += 1
        else:
            res.append(a[index_a])
            index_a += 1
            index_b += 1
    return res

if __name__ == '__main__':
    a = [9,7,5,4,3,1]
    b = [9,6,5,3,1]
    print(my_func(a, b))

