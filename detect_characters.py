# detect_characters.py
# -*- coding: utf-8 -*-

import re
import sys
from collections import Counter

# ===== 可调参数 =====
MIN_FREQ = 3         # 出现次数 >= MIN_FREQ 才认为是疑似人物
MAX_LEN = 3          # 人名最长 3 字（红楼梦里大多 2-3 字）
MIN_LEN = 2          # 人名最短 2 字
TOPK = 200           # 打印前 TOPK 个

# 常见虚词/高频无意义词（可以继续加）
EXCLUDE_WORDS = set("""
什么一个我们你们他们她们自己如此这般如何不知所以因而因此于是可是只是
说道笑道问道答道叹道忙道便道因说又说回说再说
今日昨日明日此时这时那时一面一边一时一回一日
这里那里出来进去起来过去回来
""".split())

# 含这些字的大概率不是人名（可按需要增补）
EXCLUDE_CHARS = set(list("的了着么吗啊呀吧呢哦哎嗯哪在与及并而则但因其于之乎者也所把被"))

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    txt = txt.replace("\u3000", "").replace("\r\n", "\n")
    return txt

def detect_candidates(txt):
    # 找连续 2~3 字中文词
    pattern = rf"[\u4e00-\u9fa5]{{{MIN_LEN},{MAX_LEN}}}"
    cands = re.findall(pattern, txt)
    return cands

def filter_names(cands):
    freq = Counter(cands)
    names = []
    for w, c in freq.items():
        if c < MIN_FREQ:
            continue
        if w in EXCLUDE_WORDS:
            continue
        if any(ch in EXCLUDE_CHARS for ch in w):
            continue
        names.append((w, c))
    # 按频率降序
    names.sort(key=lambda x: x[1], reverse=True)
    return names

def save_csv(names, out_path="auto_characters.csv"):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Name,Freq\n")
        for n, c in names:
            f.write(f"{n},{c}\n")

def main(txt_path):
    txt = load_text(txt_path)
    cands = detect_candidates(txt)
    names = filter_names(cands)

    print("\n==============================")
    print(f"自动检测疑似人物名（频率≥{MIN_FREQ}，长度{MIN_LEN}-{MAX_LEN}字）")
    print("==============================\n")

    for n, c in names[:TOPK]:
        print(f"{n}\t{c}")

    save_csv(names)
    print("\n==============================")
    print("已导出人物频率表：auto_characters.csv")
    print("==============================\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python detect_characters.py <txt_path>")
        sys.exit(0)
    main(sys.argv[1])
