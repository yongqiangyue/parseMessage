#! encoding=utf-8

import numpy as np

# 5 提取多维数组的行列
my_array_more = np.array([[4, 5], [6, 11]])
print(my_array_more)
print("")
print(my_array_more[:, 1])
print("")
print("")
# 4
my_2d_array_new = np.ones((2, 4))
print my_2d_array_new
# 4 打印二维数组
my_2d_array = np.zeros((2, 3))
print(my_2d_array)
# 3
my_random_array = np.random.random((1,5))
print(my_random_array)
# 2
my_new_1_array = np.ones((5))
print(my_new_1_array)
my_new_array = np.zeros((5))
print(my_new_array)
# 1
my_array = np.array([1,2,3,4,5])
# print(my_array)
print(my_array.shape)
print(my_array[0])
print(my_array[1])
my_array[0] = -1
print(my_array)