import streamlit as st
import pandas as pd  
import io

# 1. レイアウト設定
st.set_page_config(page_title="テストデータ", layout="wide")

st.title("テスト.xlsx")

# 2．Excelファイルの読み込み
df = pd.read_excel("テスト.xlsx")

# 3. フィルタセクション
st.write("### 絞り込み検索")
col1, col2, col3 = st.columns(3)

with col1:
    selected_years = st.multiselect(
        "年度を選択",
        options=sorted(df["年度"].unique().tolist(), reverse=True),
        default=[]
    )

with col2:
    selected_offices = st.multiselect(
        "事業所を選択",
        options=sorted(df["事業所"].unique().tolist()),
        default=[]
    )


with col3:
    selected_depts = st.multiselect(
        "診療科を選択",
        options=sorted(
            df["診療科"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        ),
        default=[]
    )


# 4. フィルタリングロジック
filtered_df = df.copy()

if selected_years:
    filtered_df = filtered_df[filtered_df["年度"].isin(selected_years)]
if selected_offices:
    filtered_df = filtered_df[filtered_df["事業所"].isin(selected_offices)]
if selected_depts:
    filtered_df = filtered_df[filtered_df["診療科"].isin(selected_depts)]

# 5. CSVダウンロード機能
# 日本語文字化け防止のためutf-8-sig
csv_data = filtered_df.to_csv(index=False).encode('utf-8-sig')

st.download_button(
    label="📥 表示中のデータをCSVで保存",
    data=csv_data,
    file_name='extracted_data.csv',
    mime='text/csv',
)

# 6. テーブル表示（PC/SP共に横スクロール対応）
st.write(f"表示件数: {len(filtered_df)} 件")

st.dataframe(
    filtered_df,
    use_container_width=True, 
    hide_index=True
)

# 見栄えの調整
st.markdown("""
    <style>
    div[data-testid="stDataFrame"] {
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)