from altair import default_data_transformer
import streamlit as st
import numpy as np
import pandas as pd
import time
import base64
from PIL import Image



# タイトルと説明の表示
st.title('長期保存の材料で作る今夜の献立')
st.write('今日は買い物に行けない！そんな今晩のあなたをお助け！')
st.write('★推奨メニューと材料が表示されるよ★アレンジしてね！')

# 画像を追加 
st.image("mama.png")

# サイドバーにタイトルを追加
st.sidebar.title('食材の選択')
st.sidebar.write('注）基本調味料は加味しないよ')

# サイドバーに複数選択ボックスを作成
# サイドバーの各セレクトボックスについて、選択肢とデフォルトの選択肢を設定
option1 = st.sidebar.multiselect(
    '好きな缶を選んでください',
    ['トマト', 'ツナ', 'コーン','オイルサーディン'],
    default=['トマト']
)
option2 = st.sidebar.multiselect(
    '好きな乾物を選んでください',
    ['わかめ', 'パスタ', '鰹節', 'ショートパスタ','ちりめん'],
    default=['わかめ']
)
option3 = st.sidebar.multiselect(
    '好きな常温野菜を選んでください',
    ['玉ねぎ', 'にんじん', 'じゃがいも', 'にんにく','かぼちゃ','さつまいも'],
    default=['玉ねぎ']
)
option4 = st.sidebar.multiselect(
    '好きな冷凍食品を選んでください',
    ['シーフードミックス', 'エビ','ミックスベジタブル'],
    default=['シーフードミックス']
)
option5=st.sidebar.multiselect(
    '好きな冷蔵庫の食品を選んでください',
    ['卵', '牛乳','バター','ソーセージ','魚肉ソーセージ','ベーコン','チーズ','ヨーグルト','かまぼこ'],
    default=['卵']
)

#サイドバーに画像を追加
st.sidebar.image("mother.png")

# メインエリアに選択結果を表示
selected_items = option1 + option2 + option3 + option4 + option5
st.write('↓↓↓あなたが選んだ保存食材はこちらです↓↓↓')
st.write(', '.join(selected_items))
st.title('あなたの本日のお料理候補は？')
recipes = {
    ('トマト', 'オリーブオイル', 'にんにく', '塩コショウ', '玉ねぎ','パスタ'):  "トマトパスタ",
    ('にんにく', '玉ねぎ', 'ツナ', '卵','米'): "オムライス",
    ('ショートパスタ', '牛乳', '小麦粉', 'コンソメ', '玉ねぎ', 'エビ','ソーセージ', 'チーズ'):"グラタン",
    ('ベーコン', '玉ねぎ', 'ミックスベジタブル', 'コンソメ', 'バター','エビ'): "ピラフ",
    ('卵', 'ごま油', '鶏ガラ'): "卵チャーハン",
    ('さつまいも', 'かぼちゃ', '玉ねぎ', 'エビ', '小麦粉', 'マヨネーズ'): "天ぷら",
    ('玉ねぎ', 'ポン酢', '片栗粉', '鶏ガラ', 'ごま油'): "チヂミ",
    ('玉ねぎ', 'ケチャップ', '魚肉ソーセージ', 'コンソメ', '卵'): "ナポリタン",
    ('醤油', '玉ねぎ', 'パスタ', 'にんにく', 'オイルサーディン'): "オイルサーディンパスタ",
    ('玉ねぎ', '麺つゆ', '卵', '米', 'かまぼこ'): "木の葉丼",
    ('牛乳', 'パスタ', 'ベーコン', '卵', 'バター'): "カルボナーラ",
    ('ベーコン','ソーセージ', '玉ねぎ', 'にんじん', 'じゃがいも','コンソメ'): "ポトフ",
    ('コンソメ/味噌/鶏ガラ', 'ごま油', 'ちりめん','卵'): "卵スープ",
    ('牛乳', '玉ねぎ', 'コンソメ', 'シーフードミックス','小麦'): "クラムチャウダー",
    ('トマト缶', 'コンソメ', 'じゃがいも', 'にんじん','こしょう', 'マヨネーズ'): "ポテサラ",
    ('かぼちゃ', 'チーズ', 'ヨーグルト', '塩コショウ'): "かぼちゃサラダ",
    ('玉ねぎ', 'ツナ','鰹節', 'わかめ'): "玉ねぎサラダ",
    ('わかめ', '酢', 'ちりめん'): "わかめマリネ",
    ('じゃがいも', '小麦粉', 'さつまいも'): "フライドポテト",
    ('魚肉ソーセージ', 'HM', 'ケチャップ'): "アメリカンドッグ",
    ('じゃがいも','片栗粉','チーズ','塩'):"ガレット",
    ('コーン','バター', 'しょうゆ','ごはん'):"コーンバター飯",
}
# レシピデータの定義

# レシピに対応する画像を設定
recipe_images = {
    "トマトパスタ": "tomato_pasta.jpg",
    "オムライス": "omelet.png",
    "グラタン": "gratin.jpg",
    "ピラフ": "ebipilaf.png",
    "卵チャーハン": "eggrice.png",
    "天ぷら": "tempura.png",
    "チヂミ": "chijimi.png",
    "ナポリタン": "neapolitan.png",
    "オイルサーディンパスタ": "oil-sardine.png",
    "木の葉丼": "konoha.png",
    "カルボナーラ": "carbonara.png",
    "ポトフ": "potof.png",
    "卵スープ": "eggsoup.png",
    "クラムチャウダー": "clamchowder.png",
    "ミネストローネ": "minestrone.png",
    "ポテサラ": "potatosalad.png",
    "かぼちゃサラダ": "pumpkinsalad.png",
    "玉ねぎサラダ": "onion2.jpg",
    "わかめマリネ": "wakame.png",
    "フライドポテト": "frenchfrise.png",
    "アメリカンドッグ": "corndog.png",
    "ガレット":"gallet.jpg",
    "コーンバター飯":"corn.png"}


recipes_inv = {v:k for k,v in recipes.items()}
# 選択されたオプションをタプルにしてキーとして探す
selected_tuple = (option1, option2, option3, option4,option5)
# 選択された食材に基づいてレシピを表示する
recommended_recipes = []
# 選択された食材のいずれかがレシピのキーワードに含まれていれば、そのレシピを推薦リストに追加する
for key, recipe_name in recipes.items():
    found_match = False
    for item in selected_tuple:
        if any(x in key for x in item):
            found_match = True
            break
    if found_match:
        recommended_recipes.append(recipe_name)

# おすすめのレシピを表示する
# おすすめのレシピと画像を表示する

if recommended_recipes:
    st.subheader('おすすめ献立候補:')
    for recipe in recommended_recipes:
        st.write(recipe)
        # 対応する画像を表示
        if recipe in recipe_images:
            image = Image.open(recipe_images[recipe])
  
        st.image(image, caption=recipe, use_column_width=True)
        # 食材を展開するエクスパンダーを追加
        with st.expander("食材を見る"):
          st.write(recipes_inv[recipe])

else:
    st.write('選択された組み合わせに対するレシピはありません。他の組み合わせを試してください。')
