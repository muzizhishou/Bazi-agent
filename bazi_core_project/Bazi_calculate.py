from lunar_python import Solar

def calculate_bazi(year: int, month: int, day: int, hour: int) -> dict:
    """
    根据阳历(公历)出生日期和时辰,计算生辰八字的年柱、月柱、日柱、时柱。

    参数:
        year: 出生年份(阳历),比如 1998
        month: 出生月份(阳历),比如 3
        day: 出生日期(阳历),比如 15
        hour: 出生小时(24小时制,0-23),比如 8 表示早上8点

    返回:
        一个字典,包含四柱信息,比如:
        {"年柱": "戊寅", "月柱": "乙卯", "日柱": "壬子", "时柱": "甲辰"}
    """

    # Solar.fromYmdHms 需要传入年月日时分秒,分和秒我们不关心,固定传0即可
    # 这一步是把"阳历日期"转换成 lunar_python 库能处理的对象
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)

    # getLunar() 把阳历对象转换成农历对象
    # 八字排盘的计算规则是基于农历(以及更精确的节气划分),不是阳历本身
    lunar = solar.getLunar()

    # getEightChar() 从农历对象里,进一步计算出"八字"这个专门的对象
    # 八字 = 年柱 + 月柱 + 日柱 + 时柱,每一柱由"天干+地支"两个字组成
    eight_char = lunar.getEightChar()

    # 分别取出四柱,组装成一个字典返回,方便后续代码使用
    result = {
        "年柱": eight_char.getYear(),   # 比如 "戊寅"
        "月柱": eight_char.getMonth(),  # 比如 "乙卯"
        "日柱": eight_char.getDay(),    # 比如 "壬子"
        "时柱": eight_char.getTime(),   # 比如 "甲辰"
    }

    return result


# ========== 单独测试这个函数,不涉及任何AI/Agent,先验证计算本身是否正确 ==========
if __name__ == "__main__":
    # 举个例子:1998年3月15日 早上8点出生
    result = calculate_bazi(2006, 7, 21, 7)

    print("排盘结果:")
    for pillar_name, pillar_value in result.items():
        print(f"  {pillar_name}: {pillar_value}")