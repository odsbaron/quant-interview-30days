#!/usr/bin/env python3
"""Learner starter: causal moving-average positions and cost-adjusted returns."""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data/synthetic_prices.csv"


def load_prices(path: Path = DATA) -> list[float]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [float(row["close"]) for row in csv.DictReader(handle)]


def rolling_signal(prices: list[float], lookback: int = 5) -> list[int]:
    """TODO: positions[t] uses only prices[:t]; insufficient history yields 0."""
    raise NotImplementedError("请实现 rolling_signal；先在笔记中写明信息可得时间。")


def strategy_returns(prices: list[float], positions: list[int], cost_bps: float = 5) -> list[float]:
    """TODO: N-1 next-interval returns; costs on changes, initial previous position 0."""
    raise NotImplementedError("请实现 strategy_returns；先用手工例子核对成本。")


def check() -> bool:
    passed = True
    try:
        example = [10, 12, 14, 8, 10, 12]
        got = rolling_signal(example, 2)
        if got != [0, 0, 1, 1, 0, 1]:
            raise AssertionError("两日窗口信号错误，检查过去窗口、严格大于和执行延迟。")
        if rolling_signal([10, 10, 10], 2) != [0, 0, 0]:
            raise AssertionError("价格等于均值时应为 0。")
        for index in range(len(example)):
            changed = list(example)
            changed[index] = 9999
            if rolling_signal(changed, 2)[:index + 1] != got[:index + 1]:
                raise AssertionError("当前或未来价格改变了此前持仓，存在前视。")
        print("PASS: 信号边界与信息时序")
    except (NotImplementedError, AssertionError, TypeError, ValueError, IndexError) as error:
        print("未通过信号检查：", error)
        passed = False
    try:
        got_returns = strategy_returns([100, 110, 99, 108.9], [0, 1, 0, 0], 10)
        expected = [0, -0.101, -0.001]
        if len(got_returns) != len(expected) or any(not math.isclose(a, b, abs_tol=1e-10) for a, b in zip(got_returns, expected)):
            raise AssertionError("收益或单边成本错误，预期 [0, -0.101, -0.001]。")
        print("PASS: 区间收益与成本")
    except (NotImplementedError, AssertionError, TypeError, ValueError, IndexError) as error:
        print("未通过收益检查：", error)
        passed = False
    return passed


def main() -> int:
    parser = argparse.ArgumentParser(description="Day 25—28 合成数据回测脚手架")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        return 0 if check() else 1
    prices = load_prices()
    print(f"已准备 {len(prices)} 个合成价格点：{DATA.name}")
    print("先读 exercises/mini_project/README.md；完成 rolling_signal 和 strategy_returns 两个 TODO。")
    print("不读取 price[t] 来决定 position[t]。完成后运行 --check；尚未作答不会记录为完成。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
