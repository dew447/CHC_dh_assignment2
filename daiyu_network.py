# daiyu_network.py
# -*- coding: utf-8 -*-
import re
import sys
from collections import Counter
# ==========================================================
# 1) 人物
# ==========================================================
CANON_NAMES = [
    "黛玉",
    "寶玉",
    "寶釵",
    "鳳姐",
    "王夫人",
    "賈母",
    "賈政",
    "襲人",
    "平兒",
    "李嬤嬤",
    "李紈",
    "趙姨娘",
    "趙嬤嬤",
    "麝月",
    "迎春",
    "探春",
    "惜春",
    "尤氏",
    "秦氏",
    "秦鐘",
    "智能兒",
    "晴雯",
    "鴛鴦",
    "史湘雲",
    "薛姨媽",
    "薛蟠",
    "林如海",
    "賈珍",
    "賈瑞",
    "賈璉",
    "賈蓉",
    "賈薔",
    "賈環",
    "賈赦",
    "馮紫英",
    "馮大爺",
    "忠靖侯",
    "北靜王",
    "邢夫人",
    "邢王二",
    "賈代儒",
    "張太醫",
    "來旺媳"
]
ALIAS_TO_CANON = {
    # ---------- 黛玉 ----------
    "黛玉": "黛玉",
    "林黛玉": "黛玉",
    "林姑娘": "黛玉",
    "林妹妹": "黛玉",
    "林丫頭": "黛玉",
    "林丫头": "黛玉",

    # ---------- 宝玉 ----------
    "寶玉": "寶玉",
    "宝玉": "寶玉",
    "賈寶玉": "寶玉",
    "贾宝玉": "寶玉",
    "寶二爺": "寶玉",
    "宝二爷": "寶玉",
    "寶二哥": "寶玉",
    "宝二哥": "寶玉",
    "寶兄弟": "寶玉",
    "二哥哥": "寶玉",
    "愛哥哥": "寶玉",
    "爱哥哥": "寶玉",


    # ---------- 薛宝钗 ----------
    "寶釵": "寶釵",
    "宝钗": "寶釵",
    "薛寶釵": "寶釵",
    "薛宝钗": "寶釵",

    # ---------- 凤姐 ----------
    "鳳姐": "鳳姐",
    "凤姐": "鳳姐",
    "鳳姐兒": "鳳姐",
    "凤姐儿": "鳳姐",
    "王熙鳳": "鳳姐",
    "王熙凤": "鳳姐",
    "熙鳳": "鳳姐",
    "熙凤": "鳳姐",
    "璉二奶奶": "鳳姐",
    "璉二嬸子": "鳳姐",
    "琏二奶奶": "鳳姐",
    "二奶奶": "鳳姐",
    "二嬸子": "鳳姐",
    "二婶子": "鳳姐",
    "鳳辣子": "鳳姐",

    # ---------- 王夫人 ----------
    "王夫人": "王夫人",
    "太太": "王夫人",
    "二太太": "王夫人",

    # ---------- 贾母 ----------
    "賈母": "賈母",
    "贾母": "賈母",
    "老太太": "賈母",
    "老祖宗": "賈母",
    "老太君": "賈母",

    # ---------- 贾政 ----------
    "賈政": "賈政",
    "贾政": "賈政",
    "老爺": "賈政",
    "老爷": "賈政",
    "二老爺": "賈政",
    "二老爷": "賈政",

    # ---------- 襲人 ----------
    "襲人": "襲人",
    "袭人": "襲人",

    # ---------- 平儿 ----------
    "平兒": "平兒",
    "平儿": "平兒",

    # ---------- 李嬤嬤 ----------
    "李嬤嬤": "李嬤嬤",
    "李媽媽": "李嬤嬤",
    "李妈妈": "李嬤嬤",

    # ---------- 李紈 ----------
    "李紈": "李紈",
    "李纨": "李紈",
    "大奶奶": "李紈",

    # ---------- 赵姨娘 / 赵嬤嬤 ----------
    "趙姨娘": "趙姨娘",
    "赵姨娘": "趙姨娘",
    "趙嬤嬤": "趙嬤嬤",
    "赵嬤嬤": "趙嬤嬤",
    "趙媽媽": "趙嬤嬤",
    "赵妈妈": "趙嬤嬤",

    # ---------- 麝月 ----------
    "麝月": "麝月",

    # ---------- 三春 / 晴雯 / 鸳鸯 ----------
    "迎春": "迎春",
    "二姑娘": "迎春",
    "探春": "探春",
    "三姑娘": "探春",
    "惜春": "惜春",
    "四姑娘": "惜春",
    "晴雯": "晴雯",
    "晴雯兒": "晴雯",
    "晴雯儿": "晴雯",
    "鴛鴦": "鴛鴦",
    "鸳鸯": "鴛鴦",

    # ---------- 史湘雲 ----------
    "史湘雲": "史湘雲",
    "史湘云": "史湘雲",
    "湘雲": "史湘雲",
    "湘云": "史湘雲",

    # ---------- 薛姨媽 / 薛蟠 ----------
    "薛姨媽": "薛姨媽",
    "薛姨妈": "薛姨媽",
    "薛蟠": "薛蟠",
    "薛大傻子": "薛蟠",
    "薛老大": "薛蟠",

    # ---------- 林如海 ----------
    "林如海": "林如海",
    "林老爺": "林如海",
    "林老爷": "林如海",
    "林大人": "林如海",
    "林家老爺": "林如海",
    "林家老爷": "林如海",

    # ---------- 尤氏 ----------
    "尤氏": "尤氏",
    "珍大奶奶": "尤氏",

    # ----------  ----------
    "秦氏": "秦氏",
    "蓉大奶奶": "秦氏",
    "蓉哥兒媳婦": "秦氏",
    "秦鐘": "秦鐘",
    "秦钟": "秦鐘",

    # ---------- 智能兒 ----------
    "智能兒": "智能兒",
    "智能儿": "智能兒",

    # ---------- 贾家男性 ----------
    "賈珍": "賈珍",
    "珍大爺": "賈珍",
    "珍大爷": "賈珍",
    "賈瑞": "賈瑞",
    "賈瑞急": "賈瑞",
    "瑞大爺": "賈瑞",
    "瑞大爷": "賈瑞",
    "賈璉": "賈璉",
    "贾琏": "賈璉",
    "璉二叔": "賈璉",
    "琏二叔": "賈璉",
    "賈蓉": "賈蓉",
    "蓉哥兒": "賈蓉",
    "蓉哥儿": "賈蓉",
    "賈薔": "賈薔",
    "薔大爺": "賈薔",
    "薔大爷": "賈薔",
    "賈環": "賈環",
    "环哥儿": "賈環",
    "環哥兒": "賈環",
    "賈赦": "賈赦",
    "贾赦": "賈赦",
    "大老爺": "賈赦",
    "大老爷": "賈赦",

    # ---------- 冯紫英 ----------
    "馮紫英": "馮紫英",
    "冯紫英": "馮紫英",
    "馮大爺": "馮大爺",
    "冯大爷": "馮大爺",

    # ---------- 外部人物 ----------
    "忠靖侯": "忠靖侯",
    "北靜王": "北靜王",
    "北静王": "北靜王",
    "邢夫人": "邢夫人",
    "邢王二夫人": "邢王二",
    "邢王二": "邢王二",

    # ---------- 其他 ----------
    "賈代儒": "賈代儒",
    "贾代儒": "賈代儒",
    "張太醫": "張太醫",
    "张太医": "張太醫",
    # ---------- 來旺媳 ----------
    "來旺媳": "來旺媳",
    "来旺媳": "來旺媳",
    "來旺媳婦": "來旺媳",
    "来旺媳妇": "來旺媳",

}

ALL_NAMES = sorted(ALIAS_TO_CANON.keys(), key=len, reverse=True)

# 自动收集所有“黛玉”的别名
DAIYU_CANON = "黛玉"
DAIYU_ALIASES = {a for a, c in ALIAS_TO_CANON.items() if c == DAIYU_CANON}
DAIYU_ALIASES.add(DAIYU_CANON)

# ==========================================================
# 3) 提及触发动词
# ==========================================================
MENTION_VERBS = r"(" \
    r"道|说|問|问|笑道|说道|答道|叹道|忙道|因说|便说|報說|报说|报与|報與" \
    r"提起|提到|说起|談起|谈起|念起|念及|想着|想著|想起|思量|惦记|惦念|记起|忆起|" \
    r"指|指了指|指着|指著|望|望着|望著|看|看着|看著|瞧|瞧着|瞧著|" \
    r"拉|拉着|拉著|携|携着|携著|推|推着|推著|扶|扶着|扶著|" \
    r"唤|唤着|唤著|叫|叫着|叫著|" \
    r"使眼色|打量|招手|作揖|行礼|行禮" \
r")"

MAX_DISTANCE = 25  # 句内最远距离阈值

# ==========================================================
# 4) 情感倾向词典
# ==========================================================
POS_WORDS = [
    "笑","喜","歡喜","喜欢","快活","高興","高兴","親","亲","愛","爱","好","妙",
    "夸","賞","赏","溫","温","體貼","体贴","疼","怜","贊","赞","安慰"
]
NEG_WORDS = [
    "哭","泣","淚","泪","愁","嘆","叹","怨","惱","恼","怒","罵","骂","病","死",
    "傷","伤","痛","冷笑","嫌","逼","惊","嚇","吓","不快","難過","难过"
]

def detect_speakers(sents):
    """
    检测每句里的“X + 说话动词”，返回：
    speaker_records = [
        { "idx":句号, "speaker":标准人物名, "alias":别名, "sent":句子 }
    ]
    """
    records = []
    # 任意人物别名 + 说话动词
    spk_pattern = re.compile(
        rf"({ '|'.join(map(re.escape, ALL_NAMES)) }){MENTION_VERBS}"
    )

    for i, sent in enumerate(sents):
        for m in spk_pattern.finditer(sent):
            alias = m.group(1)
            canon = ALIAS_TO_CANON.get(alias, alias)
            records.append({
                "idx": i,
                "speaker": canon,
                "alias": alias,
                "sent": sent
            })
    return records

def sentiment_label(sent: str) -> str:
    pos = any(w in sent for w in POS_WORDS)
    neg = any(w in sent for w in NEG_WORDS)
    if pos and neg:
        return "混合"
    if pos:
        return "正面"
    if neg:
        return "负面"
    return "中性"

# ==========================================================
# 5) 基础清洗与切句
# ==========================================================
def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    return txt.replace("\u3000", "").replace("\r\n", "\n")

def split_sentences(txt):
    sents = re.split(r"[。！？；\n]+", txt)
    return [s.strip() for s in sents if s.strip()]

# ==========================================================
# 6) 抓人物名
# ==========================================================
def find_names_in_sent(sent):
    found = set()
    for name in ALL_NAMES:
        if name in sent:
            found.add(ALIAS_TO_CANON[name])
    return list(found)

# ==========================================================
# 7) 句内最小距离
# ==========================================================
def min_distance_between(sent, aliases1, aliases2):
    positions1, positions2 = [], []
    for a in aliases1:
        start = 0
        while True:
            idx = sent.find(a, start)
            if idx == -1: break
            positions1.append(idx)
            start = idx + len(a)
    for b in aliases2:
        start = 0
        while True:
            idx = sent.find(b, start)
            if idx == -1: break
            positions2.append(idx)
            start = idx + len(b)
    if not positions1 or not positions2:
        return None
    return min(abs(i - j) for i in positions1 for j in positions2)

# ==========================================================
# 8) 黛玉共现/互动：窗口法 + 记录句子
# ==========================================================
def cooccur_around_daiyu(sents, window=2):
    co_cnt = Counter()
    occurrences = []
    records = []

    for i, sent in enumerate(sents):
        if any(a in sent for a in DAIYU_ALIASES):
            start = max(0, i-window)
            end = min(len(sents), i+window+1)
            ctx = " ".join(sents[start:end])

            names = find_names_in_sent(ctx)
            names = [n for n in names if n != DAIYU_CANON]
            co_cnt.update(names)

            occurrences.append((i, sent, names))

            sent_names = sorted(set(find_names_in_sent(sent)) - {DAIYU_CANON})
            records.append({
                "idx": i,
                "sent": sent,
                "co_names": sent_names,
                "sentiment": sentiment_label(sent)
            })

    return co_cnt, occurrences, records

# ==========================================================
# ==========================================================
def who_mentions_daiyu(sents):
    cnt = Counter()
    records = []

    pattern = re.compile(
        rf"({ '|'.join(map(re.escape, ALL_NAMES)) }){MENTION_VERBS}[^。！？；\n]*?"
        rf"({ '|'.join(map(re.escape, DAIYU_ALIASES)) })"
    )

    for i, sent in enumerate(sents):
        for m in pattern.finditer(sent):
            speaker_alias = m.group(1)
            speaker = ALIAS_TO_CANON[speaker_alias]

            distance = min_distance_between(sent, {speaker_alias}, DAIYU_ALIASES)
            if distance is not None and distance <= MAX_DISTANCE:
                if speaker != DAIYU_CANON:
                    cnt[speaker] += 1
                    co_names = sorted(set(find_names_in_sent(sent)) - {DAIYU_CANON})
                    records.append({
                        "idx": i, "speaker": speaker, "sent": sent,
                        "co_names": co_names, "distance": distance,
                        "sentiment": sentiment_label(sent)
                    })
    return cnt, records


def daiyu_mentions_who(sents):
    cnt = Counter()
    records = []

    # “黛玉别名 + 提及动词” 作为触发点
    trigger_pattern = re.compile(
        rf"({'|'.join(map(re.escape, DAIYU_ALIASES))}){MENTION_VERBS}"
    )

    for i, sent in enumerate(sents):
        triggers = list(trigger_pattern.finditer(sent))
        if not triggers:
            continue

        # 收集本句所有可能的“提及目标”
        sentence_targets = {}

        for trig in triggers:
            speech_start = trig.end()  # 本次触发点后开始算黛玉“提及别人”

            # 在整句里扫描所有别名，找出出现在 speech_start 后的别名
            for alias in ALL_NAMES:
                start = 0
                while True:
                    pos = sent.find(alias, start)
                    if pos == -1:
                        break
                    start = pos + len(alias)

                    if pos < speech_start:
                        continue  # 方向：只允许在触发点之后出现的别名

                    canon = ALIAS_TO_CANON[alias]
                    if canon == DAIYU_CANON:
                        continue  # 不算“黛玉提黛玉”

                    # 保存：同一句同一人多次只保留第一次距离最短的
                    if canon not in sentence_targets:
                        sentence_targets[canon] = {
                            "alias": alias,
                            "pos": pos,
                            "dist": min_distance_between(sent, DAIYU_ALIASES, {alias})
                        }
                    else:
                        # 更新更短距离（更可信）
                        old = sentence_targets[canon]["dist"]
                        new = min_distance_between(sent, DAIYU_ALIASES, {alias})
                        if new is not None and old is not None and new < old:
                            sentence_targets[canon] = {
                                "alias": alias,
                                "pos": pos,
                                "dist": new
                            }

        # 过滤掉距离过远的提及
        for name, info in sentence_targets.items():
            dist = info["dist"]
            if dist is None or dist > MAX_DISTANCE:
                continue

            cnt[name] += 1

            # 共现人物（本句中的其他人物，但不含黛玉）
            co_names = sorted(set(find_names_in_sent(sent)) - {DAIYU_CANON})

            records.append({
                "idx": i,
                "target": name,
                "alias": info["alias"],
                "sent": sent,
                "co_names": co_names,
                "distance": dist,
                "sentiment": sentiment_label(sent)
            })

    return cnt, records

def detect_dialogue_with_daiyu(speaker_records, window=2):
    """
    统计：黛玉说话附近（前后 window 句）哪些人也在说话
    """
    # 找到黛玉的说话句
    daiyu_idxs = [r["idx"] for r in speaker_records if r["speaker"] == DAIYU_CANON]

    partner_cnt = Counter()
    partner_records = []

    # 所有人按句号分组
    idx_to_speakers = {}
    for r in speaker_records:
        idx_to_speakers.setdefault(r["idx"], []).append(r["speaker"])

    for idx in daiyu_idxs:
        # 对话区间
        start = max(0, idx - window)
        end = idx + window

        local_speakers = []
        for j in range(start, end + 1):
            if j in idx_to_speakers:
                local_speakers.extend(idx_to_speakers[j])

        # 去掉黛玉自己
        local_speakers = [p for p in local_speakers if p != DAIYU_CANON]

        # 统计
        for p in set(local_speakers):   # 一段不重复
            partner_cnt[p] += 1
            partner_records.append({
                "daiyu_idx": idx,
                "partner": p,
                "window_speakers": list(set(local_speakers)),
            })

    return partner_cnt, partner_records


# ==========================================================
# 10) 输出辅助
# ==========================================================
def topk(counter, k=15):
    return counter.most_common(k)

# ==========================================================
# 11) 主程序
# ==========================================================
def main(txt_path):
    txt = load_text(txt_path)
    sents = split_sentences(txt)

    co_cnt, occs, co_records = cooccur_around_daiyu(sents, window=2)
    mention_daiyu_cnt, mention_records = who_mentions_daiyu(sents)
    daiyu_mention_cnt, daiyu_records = daiyu_mentions_who(sents)
    # S) 识别所有角色的说话句
    speaker_records = detect_speakers(sents)

    # T) 黛玉对话对象
    dialogue_cnt, dialogue_records = detect_dialogue_with_daiyu(speaker_records, window=2)

    print("\n==============================")
    print("T. 黛玉对话最多的对象（按说话邻近度）")
    for name, c in dialogue_cnt.most_common(15):
        print(f"{name}\t{c}")

    print("\n==============================")
    print("A. 黛玉出现次数（按句计）:", len(occs))
    print("==============================\n")

    print("B. 黛玉出现前后共现/互动最多的角色 TOP15")
    for name, c in topk(co_cnt, 15):
        print(f"{name}\t{c}")

    print("\n==============================\n")
    print("C. 哪些角色更常提起黛玉 ")
    for name, c in topk(mention_daiyu_cnt, 15):
        print(f"{name}\t{c}")

    print("\n==============================\n")
    print("D. 黛玉更常提起哪些人 ")
    for name, c in topk(daiyu_mention_cnt, 15):
        print(f"{name}\t{c}")

    # E) 导出 Gephi 共现边表
    edge_counter = Counter()
    window = 2
    for i, sent in enumerate(sents):
        if any(a in sent for a in DAIYU_ALIASES):
            start = max(0, i-window)
            end = min(len(sents), i+window+1)
            ctx_names = find_names_in_sent(" ".join(sents[start:end]))
            ctx_names = [n for n in ctx_names if n != DAIYU_CANON]
            for n in ctx_names:
                edge_counter[(DAIYU_CANON, n)] += 1

    out_csv = "daiyu_edges_cooccur.csv"
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write("Source,Target,Weight\n")
        for (src, tgt), w in edge_counter.items():
            f.write(f"{src},{tgt},{w}\n")

    print("\n==============================")
    print(f"E. 已导出共现边表: {out_csv}")
    print("==============================\n")

    # F/G/H) 打印并导出句子（共现人物+情感）
    def format_record(rec):
        co_str = "、".join(rec.get("co_names", [])) if rec.get("co_names") else "(无)"
        senti = rec.get("sentiment", "中性")
        dist = rec.get("distance", None)
        if dist is not None:
            return f"[句{rec['idx']}] 共现:{co_str} | 情感:{senti} | 距离:{dist} | {rec['sent']}"
        else:
            return f"[句{rec['idx']}] 共现:{co_str} | 情感:{senti} | {rec['sent']}"

    print("F. 黛玉共现句子")
    for rec in co_records:
        print(format_record(rec))

    print("\nG. 别人提及黛玉的句子")
    for rec in mention_records:
        print(format_record(rec))

    print("\nH. 黛玉提及他人的句子")
    for rec in daiyu_records:
        print(format_record(rec))

    with open("web/daiyu_interaction_sentences.txt", "w", encoding="utf-8") as f:
        f.write("【F. 黛玉共现句子（全部）】\n")
        for rec in co_records:
            f.write(format_record(rec) + "\n")

        f.write("\n【G. 别人提及黛玉的句子\n")
        for rec in mention_records:
            f.write(format_record(rec) + "\n")

        f.write("\n【H. 黛玉提及他人的句子\n")
        for rec in daiyu_records:
            f.write(format_record(rec) + "\n")

    print("\n>>> 已写入 daiyu_interaction_sentences.txt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python daiyu_network.py <txt_path>")
        sys.exit(0)
    main(sys.argv[1])
