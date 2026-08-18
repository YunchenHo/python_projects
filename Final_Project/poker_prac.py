# 學習版本

import random  # 用於洗牌功能
from collections import Counter  # 用於計算每種牌點出現次數
from itertools import combinations  # 用於取 7 選 5
# 取得從一組中任取 r 個不重複的所有組合（例如 7 張牌中任取 5 張）

# 定義撲克牌的花色與點數（13 點 × 4 花色 = 52 張）
suits = ['♠️', '♥️', '♦️', '♣️']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

# 清單推導式（List Comprehension）
# 建立一副 52 張撲克牌，每張牌為 "點數 + 花色" 的字串，例如 "A♠️"
def generate_deck():
    return [rank + suit for suit in suits for rank in ranks]
# 等同於
    # deck = []
    # for suit in suits:
    #     for rank in ranks:
    #         deck.append(rank + suit)
    # return deck

# 就地打亂牌組順序（洗牌）
def shuffle_deck(deck):
    random.shuffle(deck)
# 傳進 deck 參數
# random.shuffle(deck): Python 內建的函式，直接把 deck 洗亂順序

# 將單張牌轉換為數值（方便後續比較大小），2 ~ A 分別對應 0 ~ 12
def card_value(card):
    rank = card[0]  # 取得點數字元（'2' ~ 'A'）
    return '23456789TJQKA'.index(rank)
# card[0]：取出牌的第一個字元（例如 'A♠️' 中的 'A'）。
# .index()：回傳 rank 在字串中的位置。讓我們可以把 A 當作數值 12 來排序。

# 取得某副牌的數值排序（由大到小）與花色列表
def get_hand_ranks_and_suits(cards):
    values = sorted([card_value(c) for c in cards], reverse=True)  # 清單推導式 # 轉成數值後降冪排序
    suits = [c[1] for c in cards]  # 提取花色
    return values, suits

# 評估手牌牌型並回傳對應的分數（tuple 結構，第一個數字代表牌型強度，第二個是牌值序列）
def evaluate_hand(cards):
    best = (0, [])  # 初始化最佳手牌評分結果

    for combo in combinations(cards, 5):  # 遍歷所有 7 張牌中取 5 張的組合（C(7,5) = 21 種）
        values, suits_ = get_hand_ranks_and_suits(combo)  # 取得當前組合的數值與花色
        count = Counter(values)                           # 計算每個點數出現次數
        counts = sorted(count.values(), reverse=True)  # 次數由高到低排序
        unique = sorted(set(values), reverse=True)  # values去重後排序（用於判斷順子）
        # Counter(values) 計算每個數值出現的次數。
        # .values() 取得次數清單，例如[2, 2, 1]。
        # sorted(..., reverse=True) 是為了比對牌型強度。
        # sorted(set(values), reverse=True) 取得不重複的數值並排序，例如[12, 11, 10]。

        # 實際例子:
        # combo = ['J♠️', 'J♦️', '8♣️', '6♥️', '6♠️']
        # values = [11, 11, 8, 6, 6]
        # count = Counter({11: 2, 6: 2, 8: 1})
        # counts = [2, 2, 1]
        # unique = [11, 8, 6]

        is_flush = len(set(suits_)) == 1  # 同花：全部花色相同
        is_straight = unique == list(range(unique[0], unique[0] - 5, -1))  # 順子：連續五張

        # 特殊處理 A-2-3-4-5 的順子（A 視為 1）
        # 對於 {12, 0, 1, 2, 3}，unique[0] = 12，那 range(12, 7, -1) 會是 [12, 11, 10, 9, 8] → 完全對不上 → 不會被判成順子
        if set(values) == {12, 0, 1, 2, 3}:
            is_straight = True
            values = [3, 2, 1, 0, -1]
            # 修改值讓其數值上是順序的（用於比較）
            # 為了和其他順子做出合理的大小比較，把 values 設為 [3, 2, 1, 0, -1]
            # 確保「A2345」順子是最小的順子，不會誤贏「23456」

        # 判斷牌型，分數越高代表牌型越強（第一個值越大）
        # score = (10, values) 是一個元組（tuple），代表排序值&牌型
        if is_straight and is_flush and max(values) == 12:
            score = (10, values)  # 皇家同花順（Royal Flush）
        elif is_straight and is_flush:
            score = (9, values)  # 同花順（Straight Flush）
        elif counts[0] == 4:
            score = (8, values)  # 鐵支（Four of a Kind）
        elif counts[0] == 3 and counts[1] == 2:
            score = (7, values)  # 葫蘆（Full House）
        elif is_flush:
            score = (6, values)  # 同花（Flush）
        elif is_straight:
            score = (5, values)  # 順子（Straight）
        elif counts[0] == 3:
            score = (4, values)  # 三條（Three of a Kind）
        elif counts[0] == 2 and counts[1] == 2:
            score = (3, values)  # 兩對（Two Pairs）
        elif counts[0] == 2:
            score = (2, values)  # 一對（One Pair）
        else:
            score = (1, values)  # 高牌（High Card）

        # 更新最佳分數
        best = max(best, score)

    return best  # 回傳這組 7 張牌中最好的 5 張牌型與分數

# 比較兩副手牌的大小
def compare_hands(hand1, hand2):
    score1 = evaluate_hand(hand1)  # 評分第一副手牌
    score2 = evaluate_hand(hand2)  # 評分第二副手牌
    # (A > B) - (A < B) 是一種巧妙寫法，回傳 1 表示 hand1 勝，-1 表示 hand2 勝，0 表示平手
    return (score1 > score2) - (score1 < score2)