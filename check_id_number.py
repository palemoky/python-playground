# -*- coding: utf8 -*-

"""
关于身份证的相信内容请参看 https://blog.shixinyu.space/post/id-number-infos/
"""

from datetime import datetime, date

"""
校验身份证号码是否非法
"""

def check_id_number(id_number):
    weight = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    mod_map = (1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2)

    try:
        # 参数校验
        if 18 != len(id_number):
            raise ValueError('check_id_number function only accepts 18 characters. Input was:' + id_number)
        elif not id_number[:17].isdigit() or \
                (not id_number[17].isdigit() and id_number[17] not in ['x', 'X']) or \
                not check_birthday(id_number[6:14]):
            raise ValueError(id_number + ' is an invalid ID number!')

        # 包含 X 时转换为大写
        if not id_number.isdigit():
            id_number = id_number.upper()

        # 计算校验和
        sum = 0
        for wgt, num in zip(weight, id_number[:17]):
            sum += wgt * int(num)

        return str(mod_map[sum % 11]) == id_number[17]
    except ValueError as e:
        return e


def check_birthday(birthday):
    try:
        # 验证生日是否合法，包含闰年验证
        datetime.strptime(birthday, '%Y%m%d').date()
    except ValueError:
        return False
    else:
        # 验证生日是否在指定范围
        return '19000101' < birthday < date.today().strftime('%Y%m%d')


print(check_id_number('11010519491231002X'))