import streamlit as st
import pandas as pd
import streamlit.components.v1

if 'history' not in st.session_state:
    st.session_state['history'] = []

# 读取 CSV 文件
try:
    df = pd.read_csv('Hexagrams.csv')  # 替换为你的 CSV 文件名
except FileNotFoundError:
    st.error("CSV 文件未找到，请检查文件名和路径。")
    st.stop()

# 选项配置（可自行修改）
OPTIONS_CONFIG = {
    "option1": {
        "title": "上卦",
        "options": ["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"]
    },
    "option2": {
        "title": "下卦",
        "options": ["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"]
    },
}

# 页面布局
st.title("易学界 Search 🚀")

# 创建两列布局
cols = st.columns(2)
selections = {}

# 动态生成选择框
for idx, (key, config) in enumerate(OPTIONS_CONFIG.items()):
    with cols[idx]:
        selections[key] = st.selectbox(
            label=config["title"],
            options=config["options"],
        )

# 添加操作按钮
if st.button("✨ 搜索", use_container_width=True):
    # 根据选择的卦象查询链接
    upper_gua = selections["option1"]
    lower_gua = selections["option2"]
    matching_rows = df[(df["上卦"] == upper_gua) & (df["下卦"] == lower_gua)]

    if not matching_rows.empty:
        link = matching_rows.iloc[0]["相对路径"]  # 链接在 "相对路径" 列中
        full_link = f"https://www.yilusoso.com{link}"

        record = {
            "上卦": upper_gua,
            "下卦": lower_gua,
            "链接": full_link
        }
        st.session_state.history.insert(0, record)

        # 使用 JavaScript 跳转到链接
        js = f"window.open('{full_link}')"
        streamlit.components.v1.html(f"<script>{js}</script>")
    else:
        st.warning("未找到匹配的链接。")

# 历史记录展示（新增代码）
st.divider()
st.subheader("📜 搜索历史")

# 显示最多10条历史记录
if st.session_state.history:
    for idx, record in enumerate(st.session_state.history[:10]):
        st.markdown(f"{idx + 1}. 上卦：{record['上卦']} 下卦：{record['下卦']} [链接]({record['链接']})")
else:
    st.caption("暂无搜索历史")

# 清空历史按钮（新增代码）
if st.session_state.history and st.button("🧹 清空历史记录", use_container_width=True):
    st.session_state.history = []
    st.rerun()