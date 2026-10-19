"""测试后端功能"""
import sys
from Bazi_agent import run_analysis, build_archetype_title
from Bazi_calculate import calculate_bazi

def test_api_logic():
    """模拟API逻辑测试"""
    print("=" * 50)
    print("测试后端逻辑")
    print("=" * 50)

    # 测试数据
    year, month, day, hour = 2006, 7, 21, 7

    print(f"\n输入: {year}年{month}月{day}日{hour}时")

    # 1. 调用Agent
    print("\n1. 调用Agent生成结果...")
    try:
        result = run_analysis(year, month, day, hour)
        print("✓ Agent调用成功")
        print(f"  返回字段: {list(result.keys())}")
    except Exception as e:
        print(f"✗ Agent调用失败: {e}")
        sys.exit(1)

    # 2. 校验四柱
    print("\n2. 校验四柱...")
    expected_bazi = calculate_bazi(year, month, day, hour)
    print(f"  期望: {expected_bazi['年柱']} / {expected_bazi['月柱']} / {expected_bazi['日柱']} / {expected_bazi['时柱']}")
    print(f"  实际: {result['year_pillar']} / {result['month_pillar']} / {result['day_pillar']} / {result['hour_pillar']}")

    if (result["year_pillar"] == expected_bazi["年柱"] and
        result["month_pillar"] == expected_bazi["月柱"] and
        result["day_pillar"] == expected_bazi["日柱"] and
        result["hour_pillar"] == expected_bazi["时柱"]):
        print("✓ 四柱校验通过")
    else:
        print("✗ 四柱校验失败")
        sys.exit(1)

    # 3. 校验称号
    print("\n3. 校验称号...")
    day_stem = result["day_pillar"][0]
    month_stem = result["month_pillar"][0]
    expected_title = build_archetype_title(day_stem, month_stem)
    print(f"  期望: {expected_title}")
    print(f"  实际: {result['archetype_title']}")

    if result["archetype_title"] == expected_title:
        print("✓ 称号校验通过")
    else:
        print("✗ 称号校验失败")
        sys.exit(1)

    # 4. 显示完整结果
    print("\n4. 完整结果:")
    print(f"  四柱: {result['year_pillar']} / {result['month_pillar']} / {result['day_pillar']} / {result['hour_pillar']}")
    print(f"  称号: {result['archetype_title']}")
    print(f"  标语: {result['shareable_tagline']}")
    print(f"  摘要: {result['personality_summary'][:50]}...")
    print(f"  特质数量: {len(result['traits'])}")

    print("\n" + "=" * 50)
    print("✓ 所有测试通过!")
    print("=" * 50)

    return result

if __name__ == "__main__":
    test_api_logic()
