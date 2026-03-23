import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# ===================== 1. 页面基础配置（视觉+布局优化） =====================
st.set_page_config(
    page_title="智能体赋能的企业运营分析系统",
    page_icon="📈",
    layout="wide",  # 宽屏布局，适配演示
    initial_sidebar_state="expanded"  # 侧边栏默认展开
)

# 自定义CSS（美化样式，贴合企业级视觉）
st.markdown("""
    <style>
    /* 标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2E4057;
        text-align: center;
        margin-bottom: 20px;
    }
    /* 模块标题 */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #3A6351;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    /* 提示文本 */
    .hint-text {
        font-size: 0.9rem;
        color: #6B7280;
    }
    /* 结果卡片 */
    .result-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #3A6351;
        margin: 10px 0;
    }
    /* 隐藏Streamlit默认样式 */
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ===================== 2. 页面标题与说明（专业感提升） =====================
st.markdown('<div class="main-title">📈 智能体赋能的企业运营分析与决策支持系统</div>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; color:#6B7280;">基于多智能体协同引擎 | 聚焦医药生物领域 | 精准归因·数据溯源</p>',
    unsafe_allow_html=True)
st.divider()  # 分隔线，提升布局层次感

# ===================== 3. 侧边栏优化（功能分类+配置项） =====================
with st.sidebar:
    st.markdown('<div class="section-title">⚙️ 系统配置</div>', unsafe_allow_html=True)

    # 行业筛选（默认选中医药生物，贴合比赛设计）
    industry = st.selectbox(
        "选择分析行业",
        options=["医药生物", "新能源", "电子信息", "化工材料", "先进制造"],
        index=0,
        help="选择目标行业，智能体会加载对应领域的专业分析模型"
    )

    # 时间范围筛选（新增，贴合财报分析场景）
    time_range = st.select_slider(
        "选择分析时间范围",
        options=["近1季度", "近2季度", "近1年", "近3年"],
        value="近1年",
        help="筛选财报/研报的时间范围"
    )

    # 分析深度配置（新增，体现智能体的定制化）
    analysis_depth = st.radio(
        "选择分析深度",
        options=["基础分析（仅数据）", "深度分析（数据+归因）", "全面分析（数据+归因+建议）"],
        index=1,
        horizontal=True
    )

    # 数据来源说明（比赛要求，新增）
    st.markdown('<div class="section-title">📋 数据来源</div>', unsafe_allow_html=True)
    st.markdown("""
    - 上市公司公开财务报告
    - 券商行业/个股研报
    - 宏观经济公开数据
    """, help="所有数据均符合资本市场信息披露规范")

    # 系统版本（演示用，新增）
    st.markdown('<div class="section-title">ℹ️ 系统信息</div>', unsafe_allow_html=True)
    st.markdown("版本：V1.0 | 引擎：多智能体协同")

# ===================== 4. 主交互区优化（体验+可视化） =====================
# 分两列布局，提升空间利用率
col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    st.markdown('<div class="section-title">📝 分析需求输入</div>', unsafe_allow_html=True)

    # 公司名称输入（优化提示+校验）
    company_name = st.text_input(
        "目标企业名称",
        placeholder="例如：华润三九、恒瑞医药",
        help="请输入准确的上市公司名称，支持A股/港股医药生物企业"
    )

    # 自然语言查询框（放大+示例提示）
    user_query = st.text_area(
        "分析需求（自然语言）",
        placeholder="""示例1：分析华润三九2023年一季度净利润下滑原因
示例2：对比恒瑞医药与药明康德近1年毛利率变化
示例3：诊断云南白药2024年经营风险点""",
        height=120,
        help="支持数值查询、对比分析、归因诊断、风险洞察等场景"
    )

    # 提交按钮（美化+状态提示）
    submit_btn = st.button(
        "🚀 启动智能分析",
        type="primary",
        use_container_width=True  # 按钮占满列宽
    )

with col2:
    # 新增：历史查询记录（提升交互体验）
    st.markdown('<div class="section-title">📜 历史查询</div>', unsafe_allow_html=True)
    if "history" not in st.session_state:
        st.session_state.history = []

    # 展示历史记录（最多5条）
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            with st.expander(f"[{item['time']}] {item['company']}"):
                st.write(f"需求：{item['query']}")
                st.write(f"状态：{item['status']}")
    else:
        st.markdown('<p class="hint-text">暂无历史查询记录</p>', unsafe_allow_html=True)

# ===================== 5. 分析结果展示（可视化+交互优化） =====================
st.markdown('<div class="section-title">📊 智能分析结果</div>', unsafe_allow_html=True)

# 初始化结果容器
result_container = st.empty()

if submit_btn:
    # 输入校验（优化提示）
    if not company_name.strip():
        st.warning("⚠️ 请输入目标企业名称！")
    elif not user_query.strip():
        st.warning("⚠️ 请输入具体的分析需求！")
    else:
        # 1. 加载动画（提升体验）
        with st.spinner("🤖 智能体正在检索数据、分析逻辑..."):
            time.sleep(2)  # 模拟分析耗时（实际替换为真实逻辑）

            # 2. 模拟分析结果（需替换为Notebook中的真实智能体逻辑）
            # 示例数据（贴合医药生物行业）
            financial_data = pd.DataFrame({
                "季度": ["2023Q1", "2023Q2", "2023Q3", "2023Q4", "2024Q1"],
                "净利润(亿元)": [1.2, 1.5, 1.8, 2.1, 1.9],
                "毛利率(%)": [28.5, 27.8, 27.2, 26.8, 27.5],
                "研发投入(亿元)": [0.8, 0.9, 1.1, 1.2, 1.3]
            })

            # 归因分析结果
            attribution_analysis = f"""
            ### 核心结论
            {company_name}（{industry}）{time_range}净利润整体呈增长趋势，但2024Q1略有回落（1.9亿元，同比-2.6%）。

            ### 归因分析
            1. **核心驱动因素**：研发投入持续增加（2024Q1达1.3亿元，同比+62.5%），推动创新药管线布局，但短期影响利润；
            2. **行业环境影响**：2024Q1医药集采政策落地，核心产品价格下调5%-8%，毛利率小幅回升至27.5%；
            3. **经营策略调整**：渠道库存优化，销售费用率下降2.1个百分点，部分抵消集采影响。

            ### 决策建议
            {'【基础分析】' if analysis_depth == "基础分析（仅数据）" else ''}
            {'【深度分析】' if analysis_depth == "深度分析（数据+归因）" else ''}
            {'【全面分析】' if analysis_depth == "全面分析（数据+归因+建议）" else ''}
            建议重点关注创新药上市进度，利用集采政策窗口期优化产品线结构，平衡研发投入与短期利润。
            """

            # 3. 更新历史记录
            st.session_state.history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "company": company_name,
                "query": user_query[:50] + "..." if len(user_query) > 50 else user_query,
                "status": "分析完成"
            })

        # 4. 展示结果（美化+可视化）
        with result_container.container():
            # 结果卡片
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(attribution_analysis)
            st.markdown('</div>', unsafe_allow_html=True)

            # 可视化图表（升级为Plotly，更美观交互性更强）
            tab1, tab2 = st.tabs(["净利润趋势", "毛利率vs研发投入"])
            with tab1:
                fig1 = px.line(
                    financial_data,
                    x="季度",
                    y="净利润(亿元)",
                    title=f"{company_name}净利润趋势",
                    color_discrete_sequence=["#3A6351"],
                    markers=True
                )
                fig1.update_layout(height=300)
                st.plotly_chart(fig1, use_container_width=True)

            with tab2:
                fig2 = px.bar(
                    financial_data,
                    x="季度",
                    y=["毛利率(%)", "研发投入(亿元)"],
                    title=f"{company_name}毛利率与研发投入对比",
                    barmode="group"
                )
                fig2.update_layout(height=300)
                st.plotly_chart(fig2, use_container_width=True)

            # 数据溯源（比赛要求，新增）
            st.markdown("""
            <div class="hint-text">
            📌 数据溯源：
            - 财务数据：{company}2023-2024年季度财报
            - 行业分析：XX证券{industry}行业研报（2024年4月）
            - 分析引擎：SQL智能体+RAG检索智能体协同生成
            </div>
            """.format(company=company_name, industry=industry), unsafe_allow_html=True)

            # 导出报告（演示用，新增）
            if st.button("📄 导出分析报告", use_container_width=True):
                st.success("✅ 分析报告已导出为PDF格式（演示功能）")

# 空状态提示（优化体验）
elif not submit_btn and not st.session_state.history:
    st.markdown(
        '<p class="hint-text" style="text-align:center;">请输入分析需求并点击「启动智能分析」按钮，体验智能体的企业运营分析能力</p>',
        unsafe_allow_html=True)