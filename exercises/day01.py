"""Day 01 起步练习：公平骰子的期望与两数之和。

默认运行只显示题面。填写 TODO 后，用 --check 检查自己的实现。
此文件不会写入学习记录或修改完成状态。
"""

from __future__ import annotations

import argparse
import math
import random
from collections.abc import Callable


def expected_die_value() -> float:
    """返回一个公平六面骰子点数 X 的理论期望 E[X]。

    X 的取值为 1、2、3、4、5、6，每个取值的概率均为 1/6。
    请先在笔记中写出定义与推导，再实现本函数。
    """
    # TODO：用期望定义实现，保留笔记中的推导。
    raise NotImplementedError("尚未实现 expected_die_value；请先完成理论推导。")


def two_sum(nums: list[int], target: int) -> tuple[int, int] | list[int] | None:
    """找到两个不同位置，使对应元素之和等于 target。

    有解时返回两个索引（tuple 或 list 均可，顺序不限）；无解返回 None。
    可以返回任意一组有效答案。元素值可以重复，但同一个索引不能用两次，不修改输入。
    """
    # TODO：先写出暴力思路，再考虑如何降低时间复杂度。
    raise NotImplementedError("尚未实现 two_sum；请独立完成后再检查。")


def simulate_die_average(trials: int = 10_000, seed: int = 42) -> float:
    """用局部固定种子的随机数生成器估计平均点数，不改全局随机状态。

    这是观察实验的工具；模拟均值不能代替理论推导。
    """
    if not isinstance(trials, int) or isinstance(trials, bool) or trials <= 0:
        raise ValueError("trials 必须是正整数。")
    rng = random.Random(seed)
    return sum(rng.randint(1, 6) for _ in range(trials)) / trials


def show_exercises() -> None:
    print("Day 01：公平六面骰子期望 + 两数之和（60 分钟）")
    print("时间分配：5 分钟回顾 / 10 分钟阅读推导 / 35 分钟独立练习 / 10 分钟复盘。")
    print()
    print("练习 A：令 X 为公平六面骰子的点数，每个结果 1～6 的概率都是 1/6。")
    print("1. 根据期望的定义，推导 E[X]，再填写 expected_die_value()。")
    print("2. 用 --simulate 观察固定种子的小规模模拟，解释模拟均值与理论值的差异。")
    print()
    print("练习 B：nums=[2, 7, 11, 15]，target=9，返回两个不同位置的索引。")
    print("变式：重复元素 [3, 3] / target=6；负数 [-3, 4, 3, 90] / target=0；")
    print("      无解 [1, 2, 3] / target=99；同一位置不能使用两次。")
    print("有解可返回任意有效索引对，tuple/list 与索引顺序不限；无解返回 None。")
    print("写出思路、复杂度与边界情况，再填写 two_sum()。")
    print()
    print("使用方式：")
    print("  python3 exercises/day01.py             # 只看题面，不执行 TODO")
    print("  python3 exercises/day01.py --simulate  # 固定 seed=42，模拟 10,000 次")
    print("  python3 exercises/day01.py --check     # 完成 TODO 后检查")
    print("提示位于 exercises/README.md 的折叠区；使用提示后请如实记入每日笔记。")


def check_expected_value() -> None:
    value = expected_die_value()
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AssertionError("expected_die_value 应返回有限数值。")
    theoretical_value = sum(range(1, 7)) / 6
    if not math.isclose(value, theoretical_value, rel_tol=1e-12, abs_tol=1e-12):
        raise AssertionError("理论期望不符合每个点数概率为 1/6 的条件，请检查定义与计算。")


def check_two_sum() -> None:
    cases = [
        ("基本输入", [2, 7, 11, 15], 9, True),
        ("重复值、不同索引", [3, 3], 6, True),
        ("负数", [-3, 4, 3, 90], 0, True),
        ("允许任意多解", [1, 2, 3, 4], 5, True),
        ("多个零", [0, 0, 0], 0, True),
        ("无解", [1, 2, 3], 99, False),
        ("禁止复用同一位置", [3], 6, False),
        ("空输入", [], 0, False),
    ]
    for label, nums, target, has_solution in cases:
        # 传入副本，依据原始输入验证返回索引，同时检查输入是否被修改。
        given = nums.copy()
        answer = two_sum(given, target)
        if given != nums:
            raise AssertionError(f"{label}：不得修改输入数组。")
        if not has_solution:
            if answer is not None:
                raise AssertionError(f"{label}：无解时应返回 None。")
            continue
        if not isinstance(answer, (tuple, list)) or len(answer) != 2:
            raise AssertionError(f"{label}：应返回含两个索引的 tuple 或 list。")
        i, j = answer
        if type(i) is not int or type(j) is not int:
            raise AssertionError(f"{label}：索引必须是整数。")
        if not (0 <= i < len(nums) and 0 <= j < len(nums)):
            raise AssertionError(f"{label}：索引超出了输入范围。")
        if i == j:
            raise AssertionError(f"{label}：同一个索引不能使用两次。")
        if nums[i] + nums[j] != target:
            raise AssertionError(f"{label}：所选原始元素之和不等于 target。")


def run_checks() -> int:
    checks: list[tuple[str, Callable[[], None]]] = [
        ("公平骰子的理论期望", check_expected_value),
        ("两数之和及边界变式", check_two_sum),
    ]
    failures = 0
    for label, check in checks:
        try:
            check()
        except NotImplementedError as exc:
            failures += 1
            print(f"[未作答] {label}：{exc}")
        except Exception as exc:
            failures += 1
            print(f"[失败] {label}：{type(exc).__name__}: {exc}")
        else:
            print(f"[通过] {label}")
    if failures:
        print("检查未通过。初始 TODO 的失败是尚未作答的预期；请完成实现或修正错误后重试。")
        return 1
    print("当前练习检查通过。请自行记录独立程度、推导与错误；此工具不记录完成状态。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="验证你填写的两个 TODO 函数")
    mode.add_argument("--simulate", action="store_true", help="观察固定种子的骰子模拟均值")
    args = parser.parse_args()
    if args.check:
        return run_checks()
    if args.simulate:
        mean = simulate_die_average()
        print(f"公平六面骰子：seed=42，10,000 次模拟，平均点数={mean:.4f}")
        print("这是一个可复现样本；请与自己的理论推导比较，并解释差异。")
        return 0
    show_exercises()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
