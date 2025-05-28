import random
import csv


def get_first_column_csv(csv_file):
    first_column = []
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                first_column.append(row[0])
    return first_column


def assign_seats_to_classroom(student_list):
    if len(student_list) != 98:
        raise ValueError("Student list must contain 98 student IDs")

    shuffled_students = student_list.copy()
    random.shuffle(shuffled_students)

    blocks = []
    student_index = 0

    for block_num in range(24):
        block = [[None, None, None], [None, None, None]]

        positions_to_fill = [(0, 0), (0, 1), (1, 1), (1, 2)]

        for row, col in positions_to_fill:
            if student_index < len(shuffled_students):
                block[row][col] = shuffled_students[student_index]
                student_index += 1

        block[0][2] = "Empty"
        block[1][0] = "Empty"

        blocks.append(block)

    classroom = []
    for area_num in range(6):
        area = []
        for row in range(2):
            area_row = []
            for block_col in range(4):
                block_index = area_num * 4 + block_col
                if block_index < len(blocks):
                    for col in range(3):
                        area_row.append(blocks[block_index][row][col])
            area.append(area_row)
        classroom.append(area)

    return classroom, shuffled_students[96:98]


def rotate_areas_to_12x2(classroom):
    """将每个area从2x12旋转为12x2"""
    rotated_classroom = []

    for area in classroom:
        # area原来是2行12列，现在要转为12行2列
        rotated_area = []
        for col_idx in range(12):  # 12行
            row = []
            row.append(area[0][col_idx])  # 第一列来自原来的第一行
            row.append(area[1][col_idx])  # 第二列来自原来的第二行
            rotated_area.append(row)
        rotated_classroom.append(rotated_area)

    return rotated_classroom


def output_to_csv(
    rotated_classroom, remaining_students, filename="classroom_layout.csv"
):
    """将旋转后的课堂布局输出到CSV文件"""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # 写入每个area的数据，area之间空一行
        for area_num, area in enumerate(rotated_classroom):
            if area_num > 0:
                writer.writerow([])  # area之间空一行

            for row in area:
                writer.writerow([row[0], row[1]])

        # 写入面壁学生
        if remaining_students:
            writer.writerow([])  # 空行分隔
            writer.writerow([f'FACING THE WALL: {", ".join(remaining_students)}'])


def print_rotated_classroom_layout(rotated_classroom, remaining_students):
    """打印旋转后的课堂布局"""
    print("Rotated Classroom Seating Arrangement (12 rows x 2 columns per area):\n")

    for area_num, area in enumerate(rotated_classroom):
        print(f"Area {area_num + 1}:")
        for row_num, row in enumerate(area):
            row_display = " | ".join(str(seat).ljust(8) for seat in row)
            print(f"  Row {row_num + 1:2d}: {row_display}")
        print()

    if remaining_students:
        print(
            f"FACING THE WALL({len(remaining_students)} people): {remaining_students}"
        )


if __name__ == "__main__":
    student_ids = get_first_column_csv("for-sim-lesson/Sim2025-List.csv")

    classroom_layout, remaining = assign_seats_to_classroom(student_ids)

    # 旋转每个area为12行2列
    rotated_layout = rotate_areas_to_12x2(classroom_layout)

    # 打印旋转后的布局
    print_rotated_classroom_layout(rotated_layout, remaining)

    # 输出到CSV文件
    output_to_csv(rotated_layout, remaining, "rotated_classroom_layout.csv")
    print(f"\n布局已保存到 rotated_classroom_layout.csv 文件")
