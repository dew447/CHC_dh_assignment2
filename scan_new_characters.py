# scan_new_characters.py
# -*- coding: utf-8 -*-

import re
import sys
from collections import Counter

# ========== 可调参数 ==========
MIN_LEN = 2
MAX_LEN = 3
MIN_FREQ = 3     # 低于这个频率不列为候选
TOPK = 200

# 过滤常见叙述/虚词（可继续加）
EXCLUDE_WORDS = set("""
說著 笑道 說道 問道 答道 叹道 忙道 便说 因说 又说 回说 再说
一個人 一個個 一個月 一會子 一番 一語未 一面拉 一面走 一面說 一面又
不住 不好 不得 不成 不敢擅 不是 不然 不知 不過是 什麼 什麼事
這會子 這裡 那裡 出來 起來 過來 回來 匾額 題詠 詩句 四字 二字
""".split())

EXCLUDE_CHARS = set(list("的了着么吗啊呀吧呢哦哎嗯哪在与及并而则但因其于之乎者也所把被"))

# 你当前脚本里已有的别名（用来排除“已覆盖人物”）
CURRENT_ALIASES = set("""
黛玉 林黛玉 林姑娘 林妹妹 林丫頭 林丫头
寶玉 宝玉 賈寶玉 贾宝玉 寶二爺 宝二爷 寶二哥 宝二哥 寶兄弟
寶釵 宝钗 薛寶釵 薛宝钗
鳳姐 凤姐 鳳姐兒 王熙鳳 王熙凤 熙鳳 熙凤 璉二奶奶 璉二嬸子 二奶奶 二嬸子 鳳辣子
王夫人 太太 太太們 二太太
賈母 老太太 老祖宗 老太君
賈政 老爺 老爷 二老爺
襲人 袭人
平兒 平儿
李嬤嬤 李媽媽 李妈妈
李紈 李纨 大奶奶
趙姨娘 赵姨娘 趙嬤嬤 赵嬤嬤 趙媽媽 赵妈妈
麝月
迎春 二姑娘
探春 三姑娘
惜春 四姑娘
晴雯 晴雯兒 晴雯儿
鴛鴦 鸳鸯
史湘雲 史湘云 湘雲 湘云
薛姨媽 薛姨妈
薛蟠 薛大傻子 薛老大
林如海 林老爺 林老爷 林大人 林家老爷 林家老爺
賈珍 珍大爺 珍大爷
賈瑞 賈瑞急 瑞大爺 瑞大爷
賈璉 贾琏 璉二叔 琏二叔
賈蓉 蓉哥兒 蓉哥儿
賈薔 薔大爺 薔大爷
賈環 環哥兒 环哥儿
賈赦 大老爺 大老爷
馮紫英 冯紫英 馮大爺 冯大爷
忠靖侯 北靜王 北静王 邢夫人 邢王二
賈代儒 贾代儒 張太醫 张太医
""".split())

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().replace("\u3000", "").replace("\r\n", "\n")

def detect_candidates(txt):
    pattern = rf"[\u4e00-\u9fa5]{{{MIN_LEN},{MAX_LEN}}}"
    return re.findall(pattern, txt)

def is_noise(w):
    if w in EXCLUDE_WORDS:
        return True
    if any(ch in EXCLUDE_CHARS for ch in w):
        return True
    if re.search(r"(道|說|说|笑|聽|听|見|见|忙|便|著|来|去|過|过)$", w):
        return True
    return False

def main(txt_path):
    txt = load_text(txt_path)
    cands = detect_candidates(txt)
    freq = Counter(cands)

    items = []
    for w, c in freq.items():
        if c < MIN_FREQ:
            continue
        if is_noise(w):
            continue
        items.append((w, c))

    items.sort(key=lambda x: x[1], reverse=True)

    print("\n===== 疑似人物/专名候选（过滤后）TOP{} =====\n".format(TOPK))
    for w, c in items[:TOPK]:
        flag = "" if w in CURRENT_ALIASES else "  <-- NEW"
        print(f"{w}\t{c}{flag}")

    new_only = [(w, c) for w, c in items if w not in CURRENT_ALIASES]
    with open("web/new_character_candidates.csv", "w", encoding="utf-8") as f:
        f.write("Name,Freq\n")
        for w, c in new_only:
            f.write(f"{w},{c}\n")

    print("\n>>> 已写入 new_character_candidates.csv（仅未覆盖的新候选）\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python scan_new_characters.py <txt_path>")
        sys.exit(0)
    main(sys.argv[1])
