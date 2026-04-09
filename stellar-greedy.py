# =============================================
# 별의 탐욕 알고리즘 - 핵융합 시각화
# 필요한 라이브러리: streamlit, matplotlib
# 설치 방법: pip install streamlit matplotlib
# 실행 방법: streamlit run stellar_greedy.py
# =============================================

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우 기본 한국어 폰트
plt.rcParams['axes.unicode_minus'] = False      # 마이너스 기호 깨짐 방지

# ── 1. 데이터 ──────────────────────────────
# (원자번호, 원소기호, 한글이름, 핵자당 결합에너지 MeV)
elements = [
    (1,  "H",  "수소",      1.11),
    (2,  "He", "헬륨",      7.07),
    (6,  "C",  "탄소",      7.68),
    (8,  "O",  "산소",      7.98),
    (10, "Ne", "네온",      8.03),
    (12, "Mg", "마그네슘",  8.26),
    (14, "Si", "규소",      8.45),
    (20, "Ca", "칼슘",      8.55),
    (24, "Cr", "크로뮴",    8.57),
    (26, "Fe", "철",        8.79),   # ← 여기서 탐색 종료
    (28, "Ni", "니켈",      8.73),
    (50, "Sn", "주석",      8.51),
    (79, "Au", "금",        7.92),
    (92, "U",  "우라늄",    7.59),
]

IRON_INDEX = 9  # 철은 리스트에서 10번째(인덱스 9)

# ── 2. 페이지 설정 ─────────────────────────
st.set_page_config(
    page_title="별의 핵융합과 별의 탐욕 알고리즘",
    page_icon="⭐",
    layout="centered"
)

st.title("별의 핵융합과 별의 탐욕 알고리즘")
st.caption("핵융합은 매 순간 결합 에너지가 높아지는 원소로만 나아갑니다")

st.divider()

# ── 3. 슬라이더 (몇 단계까지 보여줄지) ────
step = st.slider(
    label="융합 단계 선택",
    min_value=0,
    max_value=len(elements) - 1,
    value=0,
    step=1
)

# 현재 단계의 원소 정보
current = elements[step]
z, sym, name, be = current

# ── 4. 현재 원소 카드 ──────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("현재 원소", f"{sym} ({name})")
col2.metric("원자번호 Z", z)
col3.metric("결합 에너지", f"{be:.2f} MeV")

# 철에 도달하면 경고 메시지
if step == IRON_INDEX:
    st.error("철 원소에 도달하였습니다.")
elif step > IRON_INDEX:
    st.warning("이 이후의 원소들은 별의 핵융합에서 만들어지지 않고 초신성 폭발에서 만들어집니다.")
else:
    gain = be - elements[step - 1][3] if step > 0 else 0
    if step > 0:
        st.success(f"탐욕 알고리즘: {elements[step-1][1]} → {sym} | 에너지 +{gain:.2f} MeV 증가")

st.divider()

# ── 5. 그래프 그리기 ───────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("#0a0c18")
ax.set_facecolor("#0a0c18")

# 전체 곡선 (흐릿하게)
all_z  = [e[0] for e in elements]
all_be = [e[3] for e in elements]
ax.plot(all_z, all_be, color="#444466", linewidth=2, zorder=1)
ax.scatter(all_z, all_be, color="#333355", s=60, zorder=2)

# 탐색한 경로 (주황색)
visited_z  = [e[0] for e in elements[:step + 1]]
visited_be = [e[3] for e in elements[:step + 1]]
ax.plot(visited_z, visited_be, color="#ff7b2f", linewidth=3, zorder=3)
ax.scatter(visited_z, visited_be, color="#f5c842", s=80, zorder=4)

# 현재 위치 (강조)
ax.scatter([z], [be], color="#ff7b2f", s=220, zorder=5,
           edgecolors="white", linewidths=1.5)

# 철 기준선
ax.axvline(x=26, color="#a8b5c4", linestyle="--", linewidth=1.2, alpha=0.6)
ax.text(27, 1.5, "Fe(철) \n최대 안정점", color="#a8b5c4", fontsize=9)

# 원소 이름 표시
for i, (ez, esym, _, ebe) in enumerate(elements):
    color = "#f5c842" if i <= step else "#555577"
    ax.annotate(esym, (ez, ebe), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=8.5,
                color=color, fontweight="bold")

# 축 설정
ax.set_xlabel("원자 번호 (Z)", color="#aaaaaa", fontsize=11)
ax.set_ylabel("핵자당 결합 에너지 (MeV)", color="#aaaaaa", fontsize=11)
ax.set_title("결합 에너지 곡선과 탐욕적 탐색 경로", color="#f5c842", fontsize=13, pad=12)
ax.tick_params(colors="#666688")
for spine in ax.spines.values():
    spine.set_edgecolor("#222244")
ax.set_xlim(-2, 96)
ax.set_ylim(0, 10)
ax.grid(True, color="#1a1a2e", linewidth=0.8)

# 범례
orange_patch = mpatches.Patch(color="#ff7b2f", label="탐욕적 선택 경로")
gray_patch   = mpatches.Patch(color="#444466", label="탐색되지 않은 영역")
ax.legend(handles=[orange_patch, gray_patch],
          facecolor="#111122", labelcolor="white", fontsize=9)

st.pyplot(fig)



# ── 6. 설명 텍스트 ─────────────────────────
st.divider()
with st.expander("📖 탐욕 알고리즘이란?"):
    st.markdown("""
    탐욕 알고라즘이란 매 순간 최적이라고 생각되는 선택을 하는 방법입니다. 
    \n별의 핵융합에서는 매 단계마다 결합 에너지가 가장 높은 원소로 나아갑니다.
    \n그렇기에 별의 핵융합은 탐욕 알고리즘이라고 할 수 있습니다.""")

    st.divider()
with st.expander("📖 탐욕 알고리즘과 최상 우선 탐색(언덕 등반 탐색)의 차이점"):
    st.markdown(""" 
  탐욕 알고리즘과 최상 우선 탐색의 가장 큰 차이점은 돌아갈 수 있는지의 여부입니다.
  \n탐욕 알고리즘은 매 순간 최적 선택을 하지만, 한번 선택한 경로에서 돌아갈 수 없습니다.
    \n반면 최상 우선 탐색은 현재 위치에서 가장 좋은 선택을 하지만,
  \n필요하다면 이전 단계로 돌아가 다른 경로를 탐색할 수 있습니다.""")
    
    st.divider()
with st.expander("📖 결합 에너지란?"):
    st.markdown("""
    결합 에너지란 원자핵을 구성하는 양성자와 중성자가 핵에서 묶여있는 힘의 정도이며, 단위는 MeV(메가 전자볼트)입니다.
    \n그리고 또한 이러한 결합 에너지가 높을수록 원자핵이 더 안정적이라는 것을 의미합니다.""")
    
    st.divider()
with st.expander("📖 결합 에너지란와 핵융합"):
    st.markdown("""
    핵융합은 가벼운 원소들이 결합하여 더 무거운 원소로 변하는 과정입니다.
    \n핵융합에선 수소+수소->헬륨에서 수소 원자 4개가 헬륨 원자 1개로 바뀝니다.
    \n수소의 양성자와 전자의 개수는 1개씩 4개지만, 헬륨의 양성자와 전자의 개수는 2개씩 1개입니다.
    \n따라서 수소 원자 4개가 헬륨 원자 1개로 바뀌면서 양성자와 전자 2개씩 총 4개가 사라집니다.
    \n이 사라진 양성자와 전자들은 결합 에너지로 방출됩니다.
    \n핵융합이 일어날 때, 원자핵이 더 안정적인 상태로 변하면서 결합 에너지가 방출됩니다.
    \n따라서 핵융합이 일어날 때마다 결합 에너지가 방출되어 별이 빛나게 됩니다.""")

    st.divider()
with st.expander("📖 핵융합 시 어째서 철보다 더 무거운 원소는 만들어지지 않는가"):
    st.markdown("""
    \n철(Fe)은 핵자당 결합 에너지가 가장 높은 원소입니다.
    \n철의 결합 에너지는 약 8.79 MeV로, 
    \n가장 높은 안정성(결합 에너지)을 가지고 있습니다. 
    \n이는 철보다 무거운 원소로의 핵융합이 일어나면 오히려 에너지를 흡수하게 되어, 
    \n별이 더 이상 핵융합을 통해 에너지를 생성할 수 없게 됩니다. 
    \n따라서 별은 철까지 핵융합을 진행한 후, 초신성 폭발로 더 무거운 원소를 만들어냅니다.""")

    st.divider()
with st.expander("📖 원자들의 결합 에너지"):
    st.markdown("""
                원소     |     핵자당 결합 에너지
                \n  

                \n수소 (H)     |    1.11 MeV

                \n헬륨 (He)    |       7.07 MeV

                \n탄소 (C)    |     7.68 MeV

                \n산소 (O)     |        7.98 MeV

                \n철 (Fe)      |    8.79 MeV ← 최대!

                \n금 (Au)       |   7.92 MeV

                \n우라늄 (U)       |   7.59 MeV""")
    
    st.divider()
with st.expander("📖 별의 핵융합으로 에너지를 얻는 법"):
    st.markdown("""
    가벼운 원소 → 융합 → 에너지 방출 → 별이 빛남
       \n↓
      \n철 도달
       \n↓
\n더 이상 에너지 없음 → 별 붕괴 
    \n→ 초신성 폭발 💥
       \n↓
\n철보다 무거운 원소 (금, 우라늄 등) 탄생""")
