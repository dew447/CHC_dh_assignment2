# clean_characters.py
# -*- coding: utf-8 -*-
import sys
import csv
import re


EXCLUDE_PATTERNS = [
    r".*道$", r".*說$", r".*说$", r".*曰$", r".*問$", r".*问$",
    r".*笑$", r".*聽$", r".*听$", r".*見$", r".*见$",
    r".*忙$", r".*便$", r".*著$", r".*来$", r".*去$",
    r".*過$", r".*过$", r".*下$", r".*起$"
]

EXCLUDE_WORDS = set("""
說著 笑道 說道 問道 答道 叹道 忙道 便说 因说 又说 回说 再说
一個人 一個個 一個月 一會子 一番 一語未 一面拉 一面走 一面說 一面又
不住 不好 不得 不成 不敢擅 不是 不然 不知 不過是
什麼 什麼事 作什麼 做什麼 說什麼 說畢
這會子 這裡 那裡 出來 起來 過來 回來
匾額 題詠 詩句 四字 二字
""".split())

EXCLUDE_CHARS = set(list("的了着么吗啊呀吧呢哦哎嗯哪在与及并而则但因其于之乎者也所把被"))

NORMALIZATION = {
    "鳳姐兒": "鳳姐",
    "鳳姐道": "鳳姐",
    "鳳姐笑": "鳳姐",
    "鳳姐便": "鳳姐",
    "鳳姐聽": "鳳姐",
    "賈母等": "賈母",
    "老太太": "賈母",
    "太太們": "王夫人",
    "趙嬤嬤": "趙嬤嬤",
    "李嬤嬤": "李嬤嬤",
    "賈政笑": "賈政",
    "賈政聽": "賈政",
    "賈政忙": "賈政",
    "賈蓉道": "賈蓉",
    "賈珍道": "賈珍",
    "賈珍忙": "賈珍",
    "賈珍笑": "賈珍",
    "賈璉道": "賈璉",
    "賈璉笑": "賈璉",
    "秦鐘道": "秦鐘",
    "秦鐘笑": "秦鐘",
    "尤氏道": "尤氏",
    "麝月道": "麝月",
    "鳳姐又": "鳳姐", "鳳姐命": "鳳姐", "鳳姐等": "鳳姐",
    "賈赦等": "賈赦",
    "賈瑞急": "賈瑞",
    "黛玉道": "黛玉", "黛玉聽": "黛玉", "黛玉笑": "黛玉", "黛玉忙": "黛玉",
    "寶玉道": "寶玉", "寶玉笑": "寶玉", "寶玉聽": "寶玉",
    "寶玉見": "寶玉", "寶玉忙": "寶玉",
}

MANUAL_KEEP = set("""
黛玉 寶玉 鳳姐 王夫人 賈母 賈政 襲人
李嬤嬤 李紈 趙姨娘 趙嬤嬤 麝月 迎春 探春 惜春
尤氏 秦氏 秦鐘 智能兒
賈珍 賈瑞 賈璉 賈蓉 賈薔 賈赦
馮紫英 馮大爺 忠靖侯 北靜王 邢夫人
""".split())

# 常见人物称谓后缀/家族前缀（用于弱判断）
PERSON_SUFFIX = ("夫人","太太","奶奶","老爺","老爷","嬤嬤","妈妈","姑娘","姐","兒","儿","王","侯")
FAMILY_PREFIX = ("賈","贾","王","史","薛","林","尤","邢","趙","赵","李","秦","馮","冯","北靜","北静")

# ========= 核心判定函数 =========
def should_exclude(word: str) -> bool:
    if not word:
        return True
    if word in EXCLUDE_WORDS:
        return True
    if any(ch in EXCLUDE_CHARS for ch in word):
        return True
    for pat in EXCLUDE_PATTERNS:
        if re.match(pat, word):
            return True
    return False

def normalize(word: str) -> str:
    word = NORMALIZATION.get(word, word)
    # 再做一次“尾巴去除”
    word = re.sub(r"(道|說|说|笑|聽|听|見|见|忙|便|等|急|不)$","", word)
    return word

def looks_like_person(word: str) -> bool:
    if word in MANUAL_KEEP:
        return True
    if len(word) < 2 or len(word) > 3:
        return False
    if word.startswith(FAMILY_PREFIX):
        return True
    if word.endswith(PERSON_SUFFIX):
        return True
    return False


def should_exclude(word):
    if word in EXCLUDE_WORDS:
        return True
    for pat in EXCLUDE_PATTERNS:
        if re.match(pat, word):
            return True
    return False


def normalize(word):
    return NORMALIZATION.get(word, word)


def main(csv_path):
    names = set()

    # === 1. read CSV ===
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["Name"]
            if should_exclude(name):
                continue
            name = normalize(name)
            names.add(name)


    names |= MANUAL_KEEP


    final = []
    for w in names:
        if len(w) >= 2 and len(w) <= 3:
            final.append(w)

    final = sorted(set(final))

    # === 4. 输出 ===
    out = "clean_characters.txt"
    with open(out, "w", encoding="utf-8") as f:
        for w in final:
            f.write(w + "\n")

    print("已生成 clean_characters.txt（最终人物名列表）：\n")
    for w in final:
        print(w)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python clean_characters.py auto_characters.csv")
        sys.exit(0)
    main(sys.argv[1])
