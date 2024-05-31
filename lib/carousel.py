import time

import array_ops

import dbops
from leight import led

import _thread

is_stop = False


def linear_map(x, in_min, in_max, out_min, out_max):
    # Clamp the input value to the input range
    if x < in_min:
        x = in_min
    elif x > in_max:
        x = in_max

    # Perform the linear mapping
    result = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return result


class carousel:
    def __init__(self):
        self.matrix = []
        self.speed = 100
        self.text = ' '
        self.start_col = 0

    def loop(self, text, speed):
        global is_stop
        is_stop = False
        self.speed = int(linear_map(speed, 1, 10, 800, 100))
        self.text = text

        self.text_to_2d()

    def stop(self):
        global is_stop
        is_stop = True

    def text_to_2d(self):
        one_space = [[0], [0], [0], [0], [0], [0], [0], [0]]
        merry_go_list = one_space
        for i in self.text:
            temp = array_ops.array_remove_empty_columns(dbops.get_font(i))
            merry_go_list = array_ops.array_concatenate_matrices(merry_go_list, temp)
            merry_go_list = array_ops.array_concatenate_matrices(merry_go_list, one_space)
        merry_go_list = array_ops.array_concatenate_matrices(merry_go_list, dbops.get_font("off"))
        self.matrix = merry_go_list
        self.start_col = 0
        _thread.start_new_thread(self.get_rolling_submatrices, [])

    def get_rolling_submatrices(self):
        global is_stop
        while not is_stop:
            matrix = self.matrix
            num_cols = len(matrix[0])
            submatrix_width = 8

            # 以下为主要循环部分
            end_col = self.start_col + submatrix_width - 1

            # 如果end_col超过了矩阵的列数，从头开始截取剩余的部分
            if end_col >= num_cols:
                end_col = end_col % num_cols
                submatrix_part1 = array_ops.array_get_submatrix(matrix, self.start_col, num_cols - 1)
                submatrix_part2 = array_ops.array_get_submatrix(matrix, 0, end_col)
                submatrix = array_ops.array_concatenate_matrices(submatrix_part1, submatrix_part2)
            else:
                submatrix = array_ops.array_get_submatrix(matrix, self.start_col, end_col)

            # 更新起始列
            self.start_col = (self.start_col + 1) % num_cols
            led.led_ctrl_multiple(array_ops.array_2d_to_1d(submatrix))
            time.sleep_ms(self.speed)
        _thread.exit()
