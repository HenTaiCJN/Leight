import array_ops

# 一维数组加法
a = [1, 2, 3]
b = [4, 5, 6]
result = array_ops.array_add(a, b)
print(result)  # 输出: [5, 7, 9]

# 二维数组转置
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
transposed = array_ops.array_transpose(matrix)
print(transposed)  # 输出: [[1, 4], [2, 5], [3, 6]]

# 一维数组转二维数组
array_1d = [1, 2, 3, 4, 5, 6]
array_2d = array_ops.array_1d_to_2d(array_1d, 2, 3)
print(array_2d)  # 输出: [[1, 2, 3], [4, 5, 6]]

# 二维数组转一维数组
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
array_1d = array_ops.array_2d_to_1d(matrix)
print(array_1d)  # 输出: [1, 2, 3, 4, 5, 6]

# 二维数组按列提取
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
column = array_ops.array_extract_column(matrix, 1)
print(column)  # 输出: [2, 5]

# 二维数组添加列
matrix = [
    [1, 2],
    [3, 4]
]
new_column = [5, 6]
new_matrix = array_ops.array_add_column(matrix, new_column)
print(new_matrix)  # 输出: [[1, 2, 5], [3, 4, 6]]

# 二维数组删除列
matrix = [
    [1, 2, 3],
    [4, 5, 6]
]
column_index = 1
new_matrix = array_ops.array_remove_column(matrix, column_index)
print(new_matrix)  # 输出: [[1, 3], [4, 6]]

array_ops.array_concatenate_matrices()