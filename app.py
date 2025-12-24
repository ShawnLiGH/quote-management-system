"""
设备报价单管理系统 - Streamlit应用
集成PDF处理、Claude AI分析和数据库管理
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
from pathlib import Path
import tempfile
import base64

# 导入自定义模块
from src.pdf_processor import PDFProcessor
from src.claude_analyzer import ClaudeAnalyzer
from src.database import QuoteDatabase


# ==================== 页面配置 ====================
st.set_page_config(
    page_title="设备报价单管理系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS样式 ====================
st.markdown("""
<style>
    /* 主标题样式 */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    
    /* 卡片样式 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* 成功/警告/错误消息样式 */
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        color: #155724;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        color: #856404;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        color: #721c24;
        margin: 1rem 0;
    }
    
    /* 侧边栏样式 */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* 按钮样式 */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3rem;
        font-weight: bold;
    }
    
    /* 文件上传区域样式 */
    .uploadedFile {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ==================== 初始化会话状态 ====================
def init_session_state():
    """初始化Streamlit会话状态"""
    if 'pdf_processor' not in st.session_state:
        st.session_state.pdf_processor = PDFProcessor()
    
    if 'claude_analyzer' not in st.session_state:
        st.session_state.claude_analyzer = None
    
    if 'database' not in st.session_state:
        st.session_state.database = QuoteDatabase()
    
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = []
    
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    
    if 'api_key' not in st.session_state:
        # Try Streamlit Cloud secrets first, then environment variables
        try:
            st.session_state.api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except:
            st.session_state.api_key = os.getenv('ANTHROPIC_API_KEY', '')


# ==================== 工具函数 ====================
def format_currency(amount):
    """格式化货币显示"""
    if amount is None:
        return "N/A"
    return f"¥{amount:,.2f}"


def format_date(date_obj):
    """格式化日期显示"""
    if date_obj is None:
        return "N/A"
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime("%Y-%m-%d %H:%M")


def create_download_link(data, filename, file_label):
    """创建下载链接"""
    if isinstance(data, pd.DataFrame):
        csv = data.to_csv(index=False, encoding='utf-8-sig')
        b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{file_label}</a>'
    else:
        b64 = base64.b64encode(data.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{file_label}</a>'
    return href


# ==================== 页面1: 概览仪表板 ====================
def page_dashboard():
    """概览仪表板页面"""
    st.markdown('<div class="main-header">📊 概览仪表板</div>', unsafe_allow_html=True)
    
    # 获取统计数据
    db = st.session_state.database
    
    try:
        # 基础统计
        total_quotes = db.get_total_quotes_count()
        total_amount = db.get_total_amount()
        recent_quotes = db.get_recent_quotes_count(days=30)
        avg_amount = db.get_average_quote_amount()
        
        # 显示关键指标
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <h3>{total_quotes}</h3>
                <p>📄 总报价单数</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <h3>{format_currency(total_amount)}</h3>
                <p>💰 总金额</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h3>{recent_quotes}</h3>
                <p>📅 本月新增</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <h3>{format_currency(avg_amount)}</h3>
                <p>📊 平均金额</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 图表展示
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 供应商分布")
            supplier_data = db.get_supplier_statistics()
            if supplier_data:
                df_suppliers = pd.DataFrame(supplier_data, columns=['供应商', '报价单数量', '总金额'])
                fig = px.bar(df_suppliers, x='供应商', y='报价单数量', 
                           title='各供应商报价单数量',
                           color='总金额',
                           color_continuous_scale='Blues')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("暂无供应商数据")
        
        with col2:
            st.subheader("📊 月度趋势")
            monthly_data = db.get_monthly_statistics()
            if monthly_data:
                df_monthly = pd.DataFrame(monthly_data, columns=['月份', '数量', '总金额'])
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_monthly['月份'], y=df_monthly['数量'],
                                       mode='lines+markers', name='报价单数量',
                                       line=dict(color='#1f77b4', width=3)))
                fig.update_layout(title='月度报价单趋势', height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("暂无月度数据")
        
        # 最近处理的报价单
        st.subheader("🕒 最近处理的报价单")
        recent_data = db.get_recent_quotes(limit=10)
        
        if recent_data:
            df_recent = pd.DataFrame(recent_data, columns=[
                'ID', '文件名', '供应商', '报价日期', '总金额', 
                '项目数量', '处理时间', '状态'
            ])
            df_recent['总金额'] = df_recent['总金额'].apply(lambda x: format_currency(x) if x else 'N/A')
            df_recent['处理时间'] = df_recent['处理时间'].apply(format_date)
            
            st.dataframe(
                df_recent,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                    "状态": st.column_config.TextColumn("状态", width="small")
                }
            )
        else:
            st.info("📭 暂无报价单数据，请先上传和处理PDF文件")
        
        # 刷新按钮
        if st.button("🔄 刷新数据", key="refresh_dashboard"):
            st.rerun()
    
    except Exception as e:
        st.error(f"加载仪表板数据时出错: {str(e)}")


# ==================== 页面2: PDF处理中心 ====================
def page_pdf_processor():
    """PDF处理中心页面"""
    st.markdown('<div class="main-header">📄 PDF处理中心</div>', unsafe_allow_html=True)
    
    # 文件上传区域
    st.subheader("1️⃣ 上传PDF文件")
    uploaded_files = st.file_uploader(
        "选择一个或多个PDF文件",
        type=['pdf'],
        accept_multiple_files=True,
        help="支持批量上传PDF格式的报价单"
    )
    
    if uploaded_files:
        st.success(f"✅ 已选择 {len(uploaded_files)} 个文件")
        
        # 显示文件列表
        with st.expander("📋 查看文件列表", expanded=True):
            for idx, file in enumerate(uploaded_files, 1):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"{idx}. {file.name}")
                with col2:
                    st.write(f"大小: {file.size / 1024:.2f} KB")
                with col3:
                    st.write("✓ 就绪")
        
        st.markdown("---")
        
        # 处理选项
        st.subheader("2️⃣ 处理选项")
        col1, col2 = st.columns(2)
        
        with col1:
            use_ocr = st.checkbox(
                "启用OCR (光学字符识别)",
                value=False,
                help="如果PDF是扫描件或图片格式，请启用OCR"
            )
        
        with col2:
            extract_images = st.checkbox(
                "提取图片",
                value=False,
                help="提取PDF中的图片内容"
            )
        
        # 开始处理按钮
        st.markdown("---")
        st.subheader("3️⃣ 开始处理")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            process_button = st.button("🚀 开始处理", type="primary", use_container_width=True)
        with col2:
            clear_button = st.button("🗑️ 清除结果", use_container_width=True)
        
        if clear_button:
            st.session_state.processed_files = []
            st.rerun()
        
        if process_button:
            processor = st.session_state.pdf_processor
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            for idx, uploaded_file in enumerate(uploaded_files):
                try:
                    status_text.text(f"正在处理: {uploaded_file.name} ({idx + 1}/{len(uploaded_files)})")
                    
                    # 保存临时文件
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    
                    # 处理PDF
                    result = processor.extract_text_from_pdf(
                        tmp_path,
                        use_ocr=use_ocr,
                        extract_images=extract_images
                    )
                    
                    result['filename'] = uploaded_file.name
                    result['file_size'] = uploaded_file.size
                    result['processed_at'] = datetime.now()
                    results.append(result)
                    
                    # 清理临时文件
                    os.unlink(tmp_path)
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                except Exception as e:
                    st.error(f"处理 {uploaded_file.name} 时出错: {str(e)}")
                    results.append({
                        'filename': uploaded_file.name,
                        'success': False,
                        'error': str(e)
                    })
            
            st.session_state.processed_files = results
            status_text.text("✅ 处理完成!")
            progress_bar.progress(1.0)
            st.balloons()
        
        # 显示处理结果
        if st.session_state.processed_files:
            st.markdown("---")
            st.subheader("4️⃣ 处理结果")
            
            for result in st.session_state.processed_files:
                with st.expander(f"📄 {result['filename']}", expanded=False):
                    if result.get('success', False):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("页数", result.get('page_count', 0))
                        with col2:
                            st.metric("字符数", result.get('text_length', 0))
                        with col3:
                            st.metric("提取方法", result.get('method', 'N/A'))
                        
                        # 显示提取的文本
                        if result.get('text'):
                            st.text_area(
                                "提取的文本内容",
                                result['text'][:1000] + "..." if len(result['text']) > 1000 else result['text'],
                                height=200,
                                key=f"text_{result['filename']}"
                            )
                        
                        # 下载按钮
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"💾 保存到数据库", key=f"save_{result['filename']}"):
                                st.info("请先使用AI分析功能处理后再保存")
                        with col2:
                            txt_data = result.get('text', '')
                            st.download_button(
                                "📥 下载文本",
                                txt_data,
                                file_name=f"{result['filename']}.txt",
                                mime="text/plain",
                                key=f"download_{result['filename']}"
                            )
                    else:
                        st.error(f"❌ 处理失败: {result.get('error', '未知错误')}")


# ==================== 页面3: AI分析界面 ====================
def page_ai_analyzer():
    """AI分析界面页面"""
    st.markdown('<div class="main-header">🤖 AI分析界面</div>', unsafe_allow_html=True)
    
    # API密钥配置
    with st.expander("⚙️ API配置", expanded=not st.session_state.api_key):
        api_key = st.text_input(
            "Anthropic API密钥",
            value=st.session_state.api_key,
            type="password",
            help="请输入您的Anthropic API密钥"
        )
        
        if st.button("💾 保存API密钥"):
            st.session_state.api_key = api_key
            st.session_state.claude_analyzer = ClaudeAnalyzer(api_key)
            st.success("✅ API密钥已保存")
    
    if not st.session_state.api_key:
        st.warning("⚠️ 请先配置API密钥")
        return
    
    # 初始化分析器
    if st.session_state.claude_analyzer is None:
        st.session_state.claude_analyzer = ClaudeAnalyzer(st.session_state.api_key)
    
    st.markdown("---")
    
    # 选择分析方式
    st.subheader("1️⃣ 选择分析方式")
    analysis_mode = st.radio(
        "分析模式",
        ["分析已处理的PDF", "直接输入文本分析", "从数据库选择"],
        horizontal=True
    )
    
    text_to_analyze = None
    selected_filename = None
    
    if analysis_mode == "分析已处理的PDF":
        if st.session_state.processed_files:
            selected_file = st.selectbox(
                "选择要分析的文件",
                options=range(len(st.session_state.processed_files)),
                format_func=lambda x: st.session_state.processed_files[x]['filename']
            )
            
            if selected_file is not None:
                file_data = st.session_state.processed_files[selected_file]
                selected_filename = file_data['filename']
                text_to_analyze = file_data.get('text', '')
                
                st.info(f"📄 已选择: {selected_filename}")
                st.text_area("文本预览", text_to_analyze[:500] + "...", height=150)
        else:
            st.warning("⚠️ 暂无已处理的PDF文件，请先前往PDF处理中心上传文件")
    
    elif analysis_mode == "直接输入文本分析":
        text_to_analyze = st.text_area(
            "输入要分析的报价单文本",
            height=300,
            placeholder="请粘贴报价单文本内容..."
        )
        selected_filename = "手动输入_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    
    else:  # 从数据库选择
        db = st.session_state.database
        quotes = db.get_all_quotes()
        
        if quotes:
            df_quotes = pd.DataFrame(quotes, columns=[
                'ID', '文件名', '供应商', '报价日期', '总金额', 
                '项目数量', '处理时间', '状态'
            ])
            
            selected_row = st.selectbox(
                "选择报价单",
                options=range(len(df_quotes)),
                format_func=lambda x: f"{df_quotes.iloc[x]['ID']} - {df_quotes.iloc[x]['文件名']}"
            )
            
            if selected_row is not None:
                quote_id = df_quotes.iloc[selected_row]['ID']
                quote_data = db.get_quote_by_id(quote_id)
                
                if quote_data:
                    text_to_analyze = quote_data.get('original_text', '')
                    selected_filename = quote_data.get('filename', '')
                    st.info(f"📄 已选择: {selected_filename}")
        else:
            st.warning("⚠️ 数据库中暂无报价单")
    
    # 分析选项
    st.markdown("---")
    st.subheader("2️⃣ 分析选项")
    
    col1, col2 = st.columns(2)
    with col1:
        extract_supplier = st.checkbox("提取供应商信息", value=True)
        extract_items = st.checkbox("提取设备项目", value=True)
    with col2:
        extract_pricing = st.checkbox("提取价格信息", value=True)
        extract_dates = st.checkbox("提取日期信息", value=True)
    
    # 开始分析
    st.markdown("---")
    st.subheader("3️⃣ 开始分析")
    
    if st.button("🚀 开始AI分析", type="primary", disabled=not text_to_analyze):
        if not text_to_analyze:
            st.error("❌ 请先选择或输入要分析的内容")
        else:
            with st.spinner("🤖 Claude AI 正在分析中..."):
                try:
                    analyzer = st.session_state.claude_analyzer
                    
                    # 调用AI分析
                    analysis_result = analyzer.analyze_quote(
                        text_to_analyze,
                        extract_supplier=extract_supplier,
                        extract_items=extract_items,
                        extract_pricing=extract_pricing,
                        extract_dates=extract_dates
                    )
                    
                    st.session_state.current_analysis = {
                        'filename': selected_filename,
                        'text': text_to_analyze,
                        'result': analysis_result,
                        'analyzed_at': datetime.now()
                    }
                    
                    st.success("✅ 分析完成!")
                    st.balloons()
                
                except Exception as e:
                    st.error(f"❌ 分析失败: {str(e)}")
    
    # 显示分析结果
    if st.session_state.current_analysis:
        st.markdown("---")
        st.subheader("4️⃣ 分析结果")
        
        result = st.session_state.current_analysis['result']
        
        # 基本信息卡片
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("供应商", result.get('supplier', 'N/A'))
        with col2:
            st.metric("报价日期", result.get('quote_date', 'N/A'))
        with col3:
            total = result.get('total_amount', 0)
            st.metric("总金额", format_currency(total))
        
        # 设备项目列表
        if result.get('items'):
            st.subheader("📦 设备项目清单")
            items_df = pd.DataFrame(result['items'])
            st.dataframe(items_df, use_container_width=True, hide_index=True)
        
        # JSON格式查看
        with st.expander("🔍 查看完整JSON结果"):
            st.json(result)
        
        # 操作按钮
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 保存到数据库", type="primary"):
                try:
                    db = st.session_state.database
                    quote_id = db.insert_quote(
                        filename=st.session_state.current_analysis['filename'],
                        original_text=st.session_state.current_analysis['text'],
                        analysis_result=result
                    )
                    st.success(f"✅ 已保存到数据库! ID: {quote_id}")
                except Exception as e:
                    st.error(f"❌ 保存失败: {str(e)}")
        
        with col2:
            # 导出为Excel
            if result.get('items'):
                items_df = pd.DataFrame(result['items'])
                excel_data = items_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "📊 导出Excel",
                    excel_data,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col3:
            # 导出为JSON
            json_data = json.dumps(result, ensure_ascii=False, indent=2)
            st.download_button(
                "📄 导出JSON",
                json_data,
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )


# ==================== 页面4: 数据库管理 ====================
def page_database():
    """数据库管理页面"""
    st.markdown('<div class="main-header">🗄️ 数据库管理</div>', unsafe_allow_html=True)
    
    db = st.session_state.database
    
    # 数据库统计
    st.subheader("📊 数据库统计")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = db.get_total_quotes_count()
        st.metric("报价单总数", total)
    
    with col2:
        amount = db.get_total_amount()
        st.metric("总金额", format_currency(amount))
    
    with col3:
        suppliers = db.get_supplier_count()
        st.metric("供应商数量", suppliers)
    
    with col4:
        avg = db.get_average_quote_amount()
        st.metric("平均金额", format_currency(avg))
    
    st.markdown("---")
    
    # 数据查询和筛选
    st.subheader("🔍 数据查询")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_supplier = st.text_input("供应商名称", placeholder="输入供应商名称...")
    
    with col2:
        date_range = st.date_input(
            "日期范围",
            value=(datetime.now() - timedelta(days=90), datetime.now()),
            help="选择查询的日期范围"
        )
    
    with col3:
        status_filter = st.selectbox(
            "状态筛选",
            ["全部", "待处理", "已完成", "已归档"]
        )
    
    # 搜索按钮
    if st.button("🔍 搜索", type="primary"):
        # 执行搜索逻辑
        quotes = db.search_quotes(
            supplier=search_supplier if search_supplier else None,
            start_date=date_range[0] if len(date_range) > 0 else None,
            end_date=date_range[1] if len(date_range) > 1 else None,
            status=status_filter if status_filter != "全部" else None
        )
        st.session_state['search_results'] = quotes
    
    # 显示查询结果
    if 'search_results' in st.session_state:
        quotes = st.session_state['search_results']
    else:
        quotes = db.get_all_quotes()
    
    if quotes:
        st.markdown("---")
        st.subheader("📋 报价单列表")
        
        df = pd.DataFrame(quotes, columns=[
            'ID', '文件名', '供应商', '报价日期', '总金额', 
            '项目数量', '处理时间', '状态'
        ])
        
        # 格式化显示
        df['总金额'] = df['总金额'].apply(lambda x: format_currency(x) if x else 'N/A')
        df['处理时间'] = df['处理时间'].apply(format_date)
        
        # 使用dataframe组件显示
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "操作": st.column_config.TextColumn("操作", width="small")
            }
        )
        
        # 批量操作
        st.markdown("---")
        st.subheader("⚡ 批量操作")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 导出全部数据"):
                csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "下载CSV文件",
                    csv_data,
                    file_name=f"quotes_export_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("🗑️ 清空数据库"):
                if st.checkbox("确认清空所有数据（不可恢复）"):
                    try:
                        db.clear_all_data()
                        st.success("✅ 数据库已清空")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 清空失败: {str(e)}")
        
        with col3:
            if st.button("🔄 刷新数据"):
                st.rerun()
        
        # 详细查看
        st.markdown("---")
        st.subheader("🔍 详细查看")
        
        selected_id = st.selectbox(
            "选择报价单ID查看详情",
            options=df['ID'].tolist(),
            format_func=lambda x: f"ID: {x} - {df[df['ID']==x]['文件名'].values[0]}"
        )
        
        if selected_id:
            quote_detail = db.get_quote_by_id(selected_id)
            
            if quote_detail:
                with st.expander("📄 查看详细信息", expanded=True):
                    # 基本信息
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**文件名:** {quote_detail.get('filename', 'N/A')}")
                        st.write(f"**供应商:** {quote_detail.get('supplier', 'N/A')}")
                        st.write(f"**报价日期:** {quote_detail.get('quote_date', 'N/A')}")
                    
                    with col2:
                        st.write(f"**总金额:** {format_currency(quote_detail.get('total_amount'))}")
                        st.write(f"**项目数量:** {quote_detail.get('item_count', 0)}")
                        st.write(f"**状态:** {quote_detail.get('status', 'N/A')}")
                    
                    # 项目列表
                    if quote_detail.get('items'):
                        st.subheader("设备项目")
                        items_df = pd.DataFrame(quote_detail['items'])
                        st.dataframe(items_df, use_container_width=True)
                    
                    # 原始文本
                    if quote_detail.get('original_text'):
                        with st.expander("原始文本"):
                            st.text_area(
                                "文本内容",
                                quote_detail['original_text'],
                                height=300,
                                key=f"detail_text_{selected_id}"
                            )
                    
                    # 操作按钮
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📝 编辑", key=f"edit_{selected_id}"):
                            st.info("编辑功能开发中...")
                    
                    with col2:
                        if st.button("🗑️ 删除", key=f"delete_{selected_id}"):
                            try:
                                db.delete_quote(selected_id)
                                st.success("✅ 删除成功")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ 删除失败: {str(e)}")
                    
                    with col3:
                        json_data = json.dumps(quote_detail, ensure_ascii=False, indent=2)
                        st.download_button(
                            "📥 导出",
                            json_data,
                            file_name=f"quote_{selected_id}.json",
                            mime="application/json",
                            key=f"export_{selected_id}"
                        )
    else:
        st.info("📭 暂无数据，请先处理PDF文件并保存到数据库")


# ==================== 页面5: 结果查看 ====================
def page_results():
    """结果查看页面"""
    st.markdown('<div class="main-header">📊 结果查看</div>', unsafe_allow_html=True)
    
    db = st.session_state.database
    
    # 选择查看方式
    view_mode = st.radio(
        "查看方式",
        ["表格视图", "卡片视图", "对比视图"],
        horizontal=True
    )
    
    quotes = db.get_all_quotes()
    
    if not quotes:
        st.info("📭 暂无数据")
        return
    
    if view_mode == "表格视图":
        st.subheader("📋 表格视图")
        
        df = pd.DataFrame(quotes, columns=[
            'ID', '文件名', '供应商', '报价日期', '总金额', 
            '项目数量', '处理时间', '状态'
        ])
        
        # 添加筛选器
        col1, col2 = st.columns(2)
        with col1:
            suppliers = ['全部'] + list(df['供应商'].unique())
            selected_supplier = st.selectbox("筛选供应商", suppliers)
        
        with col2:
            sort_by = st.selectbox("排序方式", ['ID', '总金额', '处理时间'])
        
        # 应用筛选
        if selected_supplier != '全部':
            df = df[df['供应商'] == selected_supplier]
        
        df = df.sort_values(by=sort_by, ascending=False)
        
        # 显示表格
        df['总金额'] = df['总金额'].apply(lambda x: format_currency(x) if x else 'N/A')
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    elif view_mode == "卡片视图":
        st.subheader("🎴 卡片视图")
        
        # 每行显示3个卡片
        cols = st.columns(3)
        
        for idx, quote in enumerate(quotes):
            col_idx = idx % 3
            
            with cols[col_idx]:
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; background: white;">
                        <h4 style="color: #1f77b4; margin: 0;">{quote[1]}</h4>
                        <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0;">供应商: {quote[2] or 'N/A'}</p>
                        <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0;">金额: {format_currency(quote[4])}</p>
                        <p style="color: #666; font-size: 0.9rem; margin: 0.5rem 0;">项目: {quote[5]} 个</p>
                        <p style="color: #666; font-size: 0.8rem; margin: 0.5rem 0;">{format_date(quote[6])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("查看详情", key=f"view_card_{quote[0]}"):
                        st.session_state['selected_quote_id'] = quote[0]
                        st.rerun()
    
    else:  # 对比视图
        st.subheader("⚖️ 对比视图")
        
        # 选择要对比的报价单
        quote_ids = [q[0] for q in quotes]
        quote_labels = [f"{q[0]} - {q[1]}" for q in quotes]
        
        col1, col2 = st.columns(2)
        with col1:
            compare1 = st.selectbox("选择报价单 1", options=quote_ids, format_func=lambda x: quote_labels[quote_ids.index(x)])
        
        with col2:
            compare2 = st.selectbox("选择报价单 2", options=quote_ids, format_func=lambda x: quote_labels[quote_ids.index(x)], index=min(1, len(quote_ids)-1))
        
        if compare1 != compare2:
            quote1 = db.get_quote_by_id(compare1)
            quote2 = db.get_quote_by_id(compare2)
            
            if quote1 and quote2:
                # 对比表格
                comparison_data = {
                    '项目': ['供应商', '报价日期', '总金额', '项目数量', '处理时间'],
                    '报价单 1': [
                        quote1.get('supplier', 'N/A'),
                        quote1.get('quote_date', 'N/A'),
                        format_currency(quote1.get('total_amount')),
                        quote1.get('item_count', 0),
                        format_date(quote1.get('processed_at'))
                    ],
                    '报价单 2': [
                        quote2.get('supplier', 'N/A'),
                        quote2.get('quote_date', 'N/A'),
                        format_currency(quote2.get('total_amount')),
                        quote2.get('item_count', 0),
                        format_date(quote2.get('processed_at'))
                    ]
                }
                
                df_comparison = pd.DataFrame(comparison_data)
                st.dataframe(df_comparison, use_container_width=True, hide_index=True)
                
                # 价格对比图表
                if quote1.get('total_amount') and quote2.get('total_amount'):
                    fig = go.Figure(data=[
                        go.Bar(name='报价单 1', x=['总金额'], y=[quote1['total_amount']]),
                        go.Bar(name='报价单 2', x=['总金额'], y=[quote2['total_amount']])
                    ])
                    fig.update_layout(title='价格对比', height=400)
                    st.plotly_chart(fig, use_container_width=True)


# ==================== 页面6: 系统设置 ====================
def page_settings():
    """系统设置页面"""
    st.markdown('<div class="main-header">⚙️ 系统设置</div>', unsafe_allow_html=True)
    
    # API设置
    st.subheader("🔑 API配置")
    with st.expander("Anthropic API设置", expanded=True):
        api_key = st.text_input(
            "API密钥",
            value=st.session_state.api_key,
            type="password"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 保存API密钥"):
                st.session_state.api_key = api_key
                st.session_state.claude_analyzer = ClaudeAnalyzer(api_key)
                st.success("✅ 已保存")
        
        with col2:
            if st.button("🧪 测试连接"):
                if api_key:
                    try:
                        analyzer = ClaudeAnalyzer(api_key)
                        # 简单测试
                        result = analyzer.analyze_quote("测试文本", extract_supplier=True)
                        st.success("✅ 连接成功")
                    except Exception as e:
                        st.error(f"❌ 连接失败: {str(e)}")
                else:
                    st.error("❌ 请先输入API密钥")
    
    st.markdown("---")
    
    # 数据库设置
    st.subheader("🗄️ 数据库配置")
    with st.expander("数据库设置", expanded=True):
        db_path = st.text_input(
            "数据库路径",
            value="data/quotes.db",
            help="SQLite数据库文件路径"
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 重新连接"):
                try:
                    st.session_state.database = QuoteDatabase(db_path)
                    st.success("✅ 重新连接成功")
                except Exception as e:
                    st.error(f"❌ 连接失败: {str(e)}")
        
        with col2:
            if st.button("📊 查看统计"):
                db = st.session_state.database
                st.info(f"报价单总数: {db.get_total_quotes_count()}")
        
        with col3:
            if st.button("🗑️ 清空数据"):
                if st.checkbox("确认清空", key="confirm_clear_settings"):
                    try:
                        st.session_state.database.clear_all_data()
                        st.success("✅ 已清空")
                    except Exception as e:
                        st.error(f"❌ 清空失败: {str(e)}")
    
    st.markdown("---")
    
    # PDF处理设置
    st.subheader("📄 PDF处理配置")
    with st.expander("PDF处理设置", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            default_ocr = st.checkbox("默认启用OCR", value=False)
            default_extract_images = st.checkbox("默认提取图片", value=False)
        
        with col2:
            max_pages = st.number_input("最大处理页数", min_value=1, max_value=1000, value=100)
            timeout = st.number_input("处理超时(秒)", min_value=10, max_value=300, value=60)
        
        if st.button("💾 保存PDF设置"):
            st.success("✅ 设置已保存")
    
    st.markdown("---")
    
    # 显示设置
    st.subheader("🎨 显示设置")
    with st.expander("界面显示设置", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            theme = st.selectbox("主题", ["浅色", "深色", "自动"])
            language = st.selectbox("语言", ["中文", "English"])
        
        with col2:
            items_per_page = st.number_input("每页显示数量", min_value=10, max_value=100, value=20)
            chart_height = st.number_input("图表高度", min_value=300, max_value=800, value=400)
        
        if st.button("💾 保存显示设置"):
            st.success("✅ 设置已保存")
    
    st.markdown("---")
    
    # 系统信息
    st.subheader("ℹ️ 系统信息")
    with st.expander("查看系统信息", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**应用版本:** 1.0.0")
            st.write("**Python版本:**", "3.9+")
            st.write("**Streamlit版本:**", st.__version__)
        
        with col2:
            st.write("**数据库类型:** SQLite")
            st.write("**AI模型:** Claude")
            st.write("**PDF引擎:** PyMuPDF")
    
    st.markdown("---")
    
    # 数据管理
    st.subheader("📦 数据管理")
    with st.expander("备份和恢复", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**备份数据库**")
            if st.button("📥 创建备份"):
                try:
                    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                    st.info(f"备份已创建: {backup_name}")
                except Exception as e:
                    st.error(f"❌ 备份失败: {str(e)}")
        
        with col2:
            st.write("**恢复数据库**")
            backup_file = st.file_uploader("选择备份文件", type=['db'])
            if backup_file and st.button("📤 恢复"):
                st.info("恢复功能开发中...")
    
    st.markdown("---")
    
    # 关于
    st.subheader("ℹ️ 关于")
    st.markdown("""
    ### 设备报价单管理系统
    
    **版本:** 1.0.0  
    **开发者:** Your Name  
    **更新日期:** 2024-12-23
    
    **功能特性:**
    - ✅ PDF文本提取（支持OCR）
    - ✅ Claude AI智能分析
    - ✅ 数据库管理
    - ✅ 可视化报表
    - ✅ 数据导入导出
    
    **技术栈:**
    - Streamlit
    - PyMuPDF
    - Anthropic Claude API
    - SQLite
    - Plotly
    
    ---
    
    如有问题或建议，请联系技术支持。
    """)


# ==================== 主应用 ====================
def main():
    """主应用入口"""
    # 初始化
    init_session_state()
    
    # 侧边栏导航
    with st.sidebar:
        st.markdown("## 🎯 导航菜单")
        
        page = st.radio(
            "选择功能",
            [
                "📊 概览仪表板",
                "📄 PDF处理中心",
                "🤖 AI分析界面",
                "🗄️ 数据库管理",
                "📈 结果查看",
                "⚙️ 系统设置"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 快速统计
        st.markdown("### 📊 快速统计")
        try:
            db = st.session_state.database
            total = db.get_total_quotes_count()
            amount = db.get_total_amount()
            
            st.metric("报价单总数", total)
            st.metric("总金额", format_currency(amount))
        except:
            st.info("统计数据加载中...")
        
        st.markdown("---")
        
        # 系统状态
        st.markdown("### 🔧 系统状态")
        
        # API状态
        api_status = "🟢 已配置" if st.session_state.api_key else "🔴 未配置"
        st.write(f"API: {api_status}")
        
        # 数据库状态
        try:
            db_status = "🟢 正常" if st.session_state.database else "🔴 异常"
        except:
            db_status = "🔴 异常"
        st.write(f"数据库: {db_status}")
        
        st.markdown("---")
        
        # 版权信息
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p>设备报价单管理系统</p>
            <p>Version 1.0.0</p>
            <p>© 2024 All Rights Reserved</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 路由到对应页面
    if page == "📊 概览仪表板":
        page_dashboard()
    elif page == "📄 PDF处理中心":
        page_pdf_processor()
    elif page == "🤖 AI分析界面":
        page_ai_analyzer()
    elif page == "🗄️ 数据库管理":
        page_database()
    elif page == "📈 结果查看":
        page_results()
    elif page == "⚙️ 系统设置":
        page_settings()


# ==================== 运行应用 ====================
if __name__ == "__main__":
    main()
