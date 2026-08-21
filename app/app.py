import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. إعدادات الصفحة والتنسيق
# ==========================================
st.set_page_config(
    page_title="لوحة تحليلات المبيعات التنفيذية",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. إعدادات الاتصال بقاعدة بيانات MySQL
# ==========================================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "sales"

def run_query(query):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بقاعدة البيانات: {e}")
        return pd.DataFrame()

# ==========================================
# 3. الفلتر والتحكم (مع الرموز التعبيرية المميزة بالأعلى)
# ==========================================
st.markdown("""
    <div style="
        display: flex;
        direction: rtl;
        justify-content: flex-start;
        align-items: center;
        gap: 55px;
        padding-right: 40px;
        margin-bottom: 18px;
        font-size: 1.5rem;
        width: 100%;
    ">
        <span>🌐</span>
        <span>👨‍💼</span>
        <span>👩‍💼</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; margin-bottom: 15px;'>", unsafe_allow_html=True)
filter_option = st.radio(
    "اختر فئة التحليل:",
    options=["الكل", "الرجال", "النساء"],
    horizontal=True,
    index=0,
    key="gender_filter"
)
st.markdown("</div>", unsafe_allow_html=True)

# تحديد الثيم والألوان ديناميكياً بناءً على الاختيار
if filter_option == "الرجال":
    primary_color = "#2563EB"
    accent_bg = "#EFF6FF"        
    chart_color = "#3B82F6"
    gradient_theme = "linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%)"
elif filter_option == "النساء":
    primary_color = "#EC4899"
    accent_bg = "#FDF2F8"        
    chart_color = "#F43F5E"
    gradient_theme = "linear-gradient(135deg, #FDF2F8 0%, #FFFFFF 100%)"
else:
    primary_color = "#7C3AED"
    accent_bg = "#F3E8FF"        
    chart_color = "#8B5CF6"
    gradient_theme = "linear-gradient(135deg, #F3E8FF 0%, #FFFFFF 100%)"

# ==========================================
# 4. حقن التصاميم والخطوط CSS الحصرية والواضحة
# ==========================================
custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Tajawal', sans-serif !important;
        background-color: #F8FAFC !important;
        direction: rtl;
        text-align: right;
    }}
    
    .stApp {{
        background-color: #F8FAFC;
    }}

    div[role="radiogroup"] {{
        background: #FFFFFF;
        padding: 6px;
        border-radius: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        display: inline-flex !important;
        justify-content: center;
        border: 1px solid #E2E8F0;
    }}
    
    div[role="radiogroup"] label {{
        padding: 8px 24px !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        color: #1E293B !important;
        transition: all 0.3s ease !important;
    }}
    
    .kpi-card {{
        background: #FFFFFF;
        border-radius: 20px;
        padding: 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.08);
        border-color: {primary_color};
    }}

    .kpi-hero {{
        background: {gradient_theme};
        border: 2px solid {primary_color};
    }}

    .kpi-title {{
        font-size: 1.2rem;
        color: #475569;
        font-weight: 700;
        margin-bottom: 8px;
    }}

    .kpi-value-hero {{
        font-size: 2.8rem;
        font-weight: 800;
        color: {primary_color};
        line-height: 1.2;
    }}

    .kpi-value {{
        font-size: 2.1rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }}

    .badge {{
        background-color: {accent_bg};
        color: {primary_color};
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 700;
        display: inline-block;
        margin-top: 10px;
    }}

    .section-title {{
        font-size: 1.3rem;
        font-weight: 800;
        color: #0F172A;
        margin-bottom: 16px;
    }}

    .insights-card {{
        background: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        border-right: 6px solid {primary_color};
        box-shadow: 0 8px 20px -5px rgba(0, 0, 0, 0.03);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 5. بناء الاستعلامات المباشرة
# ==========================================
if filter_option == "الكل":
    sql_monthly = """
    SELECT
        CASE
            WHEN MONTH(`Date`) = 1 THEN 'January'
            WHEN MONTH(`Date`) = 2 THEN 'February'
            WHEN MONTH(`Date`) = 3 THEN 'March'
            WHEN MONTH(`Date`) = 4 THEN 'April'
            WHEN MONTH(`Date`) = 5 THEN 'May'
            WHEN MONTH(`Date`) = 6 THEN 'June'
            WHEN MONTH(`Date`) = 7 THEN 'July'
            WHEN MONTH(`Date`) = 8 THEN 'August'
            WHEN MONTH(`Date`) = 9 THEN 'September'
            WHEN MONTH(`Date`) = 10 THEN 'October'
            WHEN MONTH(`Date`) = 11 THEN 'November'
            WHEN MONTH(`Date`) = 12 THEN 'December'
        END AS MONTH_name,
        ROUND(AVG(`Quantity`), 2) AS Quantity_avg,
        ROUND(AVG(`Total Amount`), 2) AS Total_Amount_avg
    FROM `sales dataset`
    GROUP BY MONTH(`Date`);
    """
    sql_age = """
    SELECT CASE 
        WHEN `Age` BETWEEN 18 and 24 THEN '18-24' 
        WHEN `Age` BETWEEN 25 and 34 THEN '25-34' 
        WHEN `Age` BETWEEN 34 and 44 THEN '35-44' 
        WHEN `Age` BETWEEN 45 and 54 THEN '45-54'
        WHEN `Age` BETWEEN 55 and 64 THEN '55-64' 
    END as range_age ,ROUND( AVG(`Total Amount`),2) as `Total Amount_avg` ,ROUND( AVG(`Quantity`),2) as `Quantity_avg` FROM `sales dataset` GROUP BY range_age;
    """
    sql_gender_all = """
    SELECT `Gender`, ROUND( AVG(`Quantity`),2) as `Quantity_avg` ,  ROUND( AVG(`Total Amount`) ,2) as `Total Amount_avg` FROM `sales dataset` GROUP BY `Gender`;
    """
    sql_products = """
    SELECT `Product Category`, SUM(`Quantity`) AS `Total_Quantity` 
    FROM `sales dataset` 
    GROUP BY `Product Category`
    ORDER BY `Total_Quantity` DESC;
    """
elif filter_option == "النساء":
    sql_monthly = """
    SELECT
        CASE
            WHEN MONTH(`Date`) = 1 THEN 'January'
            WHEN MONTH(`Date`) = 2 THEN 'February'
            WHEN MONTH(`Date`) = 3 THEN 'March'
            WHEN MONTH(`Date`) = 4 THEN 'April'
            WHEN MONTH(`Date`) = 5 THEN 'May'
            WHEN MONTH(`Date`) = 6 THEN 'June'
            WHEN MONTH(`Date`) = 7 THEN 'July'
            WHEN MONTH(`Date`) = 8 THEN 'August'
            WHEN MONTH(`Date`) = 9 THEN 'September'
            WHEN MONTH(`Date`) = 10 THEN 'October'
            WHEN MONTH(`Date`) = 11 THEN 'November'
            WHEN MONTH(`Date`) = 12 THEN 'December'
        END AS MONTH_name,
        ROUND(AVG(`Quantity`), 2) AS Quantity_avg,
        ROUND(AVG(`Total Amount`), 2) AS Total_Amount_avg
    FROM `sales dataset`
    WHERE `Gender`='Female'
    GROUP BY MONTH(`Date`);
    """
    sql_age = """
    SELECT CASE 
        WHEN `Age` BETWEEN 18 and 24 THEN '18-24' 
        WHEN `Age` BETWEEN 25 and 34 THEN '25-34' 
        WHEN `Age` BETWEEN 34 and 44 THEN '35-44' 
        WHEN `Age` BETWEEN 45 and 54 THEN '45-54'
        WHEN `Age` BETWEEN 55 and 64 THEN '55-64' 
    END as range_age ,ROUND( AVG(`Total Amount`),2) as `Total Amount_avg` ,ROUND( AVG(`Quantity`),2) as `Quantity_avg` FROM `sales dataset` 
     WHERE `Gender`='Female'
    GROUP BY range_age;
    """
    sql_products = """
    SELECT `Product Category`, SUM(`Quantity`) AS `Total_Quantity` 
    FROM `sales dataset` 
    WHERE `Gender`='Female' 
    GROUP BY `Product Category`
    ORDER BY `Total_Quantity` DESC;
    """
else:
    sql_monthly = """
    SELECT
        CASE
            WHEN MONTH(`Date`) = 1 THEN 'January'
            WHEN MONTH(`Date`) = 2 THEN 'February'
            WHEN MONTH(`Date`) = 3 THEN 'March'
            WHEN MONTH(`Date`) = 4 THEN 'April'
            WHEN MONTH(`Date`) = 5 THEN 'May'
            WHEN MONTH(`Date`) = 6 THEN 'June'
            WHEN MONTH(`Date`) = 7 THEN 'July'
            WHEN MONTH(`Date`) = 8 THEN 'August'
            WHEN MONTH(`Date`) = 9 THEN 'September'
            WHEN MONTH(`Date`) = 10 THEN 'October'
            WHEN MONTH(`Date`) = 11 THEN 'November'
            WHEN MONTH(`Date`) = 12 THEN 'December'
        END AS MONTH_name,
        ROUND(AVG(`Quantity`), 2) AS Quantity_avg,
        ROUND(AVG(`Total Amount`), 2) AS Total_Amount_avg
    FROM `sales dataset`
    WHERE `Gender`='Male'
    GROUP BY MONTH(`Date`);
    """
    sql_age = """
    SELECT CASE 
        WHEN `Age` BETWEEN 18 and 24 THEN '18-24' 
        WHEN `Age` BETWEEN 25 and 34 THEN '25-34' 
        WHEN `Age` BETWEEN 34 and 44 THEN '35-44' 
        WHEN `Age` BETWEEN 45 and 54 THEN '45-54'
        WHEN `Age` BETWEEN 55 and 64 THEN '55-64' 
    END as range_age ,ROUND( AVG(`Total Amount`),2) as `Total Amount_avg` ,ROUND( AVG(`Quantity`),2) as `Quantity_avg` FROM `sales dataset` 
     WHERE `Gender`='Male'
    GROUP BY range_age;
    """
    sql_products = """
    SELECT `Product Category`, SUM(`Quantity`) AS `Total_Quantity` 
    FROM `sales dataset` 
    WHERE `Gender`='Male' 
    GROUP BY `Product Category`
    ORDER BY `Total_Quantity` DESC;
    """

df_monthly = run_query(sql_monthly)
df_age = run_query(sql_age)
df_products = run_query(sql_products)

if not df_monthly.empty and 'MONTH_name' in df_monthly.columns:
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_monthly['MONTH_name'] = pd.Categorical(df_monthly['MONTH_name'], categories=months_order, ordered=True)
    df_monthly = df_monthly.sort_values('MONTH_name')

# ==========================================
# 6. عنوان الداشبورد الرئيسي ومقارنة الجنسين (فوق يسار الشاشة)
# ==========================================
header_col1, header_middle, header_col2 = st.columns([1.5, 1, 1.2])

with header_col1:
    st.markdown(f"""
        <div style='text-align: right; margin-bottom: 25px;'>
            <h1 style='font-size: 2.3rem; font-weight: 800; color: #0F172A; margin:0;'>تحليلات المبيعات والأداء التنفيذي 🚀</h1>
            <p style='font-size: 1.1rem; color: #475569; margin-top: 5px;'>لوحة تحكم تفاعلية متطورة ({filter_option})</p>
        </div>
    """, unsafe_allow_html=True)

# حساب القيم الثابتة للخلاصة والمؤشرات
avg_total_amount = round(df_monthly['Total_Amount_avg'].mean(), 2) if not df_monthly.empty and 'Total_Amount_avg' in df_monthly.columns else 0.0
avg_quantity = round(df_monthly['Quantity_avg'].mean(), 2) if not df_monthly.empty and 'Quantity_avg' in df_monthly.columns else 0.0

top_age_group = "N/A"
if not df_age.empty and 'Total Amount_avg' in df_age.columns:
    top_age_row = df_age.loc[df_age['Total Amount_avg'].idxmax()]
    top_age_group = top_age_row['range_age']

max_month = "N/A"
max_month_val = 0
if not df_monthly.empty:
    max_row = df_monthly.loc[df_monthly['Total_Amount_avg'].idxmax()]
    max_month = max_row['MONTH_name']
    max_month_val = max_row['Total_Amount_avg']

# المربع الأوسط (أهم النتائج والتوصيات)
with header_middle:
    st.markdown(f"""
        <div class="insights-card">
            <div style="font-size: 1.15rem; font-weight: 800; color: #0F172A; margin-bottom: 10px;">💡 أهم النتائج والتوصيات</div>
            <ul style="margin: 0; padding-right: 18px; font-size: 1.05rem; color: #1E293B; line-height: 1.7; font-weight: 700;">
                <li>الأعلى: شهر <span style="color: {primary_color};">{max_month}</span> (${max_month_val:,.2f})</li>
                <li>الفئة: عمر <span style="color: {primary_color};">{top_age_group}</span> سنة</li>
                <li>الكمية: <span style="color: {primary_color};">{avg_quantity} وحدة</span></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with header_col2:
    if filter_option == "الكل":
        df_gender_all = run_query(sql_gender_all)
        if not df_gender_all.empty:
            st.markdown('<div class="section-title" style="font-size: 1.15rem; text-align: left; margin-bottom: 4px; font-weight: 800;">⚖️ إجمالي الإنفاق بين الجنسين</div>', unsafe_allow_html=True)
            fig_donut = px.pie(
                df_gender_all,
                names='Gender',
                values='Total Amount_avg',
                hole=0.6,
                color='Gender',
                color_discrete_map={'Male': '#2563EB', 'Female': '#EC4899'}
            )
            fig_donut.update_traces(
                textposition='inside', 
                textinfo='percent+label', 
                textfont=dict(family="Tajawal", size=13, weight="bold"),
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=150,
                margin=dict(l=0, r=0, t=0, b=0),
                font=dict(family="Tajawal", size=13, color="#1E293B"),
                showlegend=False
            )
            st.plotly_chart(fig_donut, use_container_width=True)

# ==========================================
# 7. مؤشرات الأداء الرئيسية KPI Cards
# ==========================================
col1, col2, col3 = st.columns([1.4, 1, 1])

with col1:
    st.markdown(f"""
        <div class="kpi-card kpi-hero">
            <div class="kpi-title">متوسط إجمالي الفاتوره (Hero Metric)</div>
            <div class="kpi-value-hero">${avg_total_amount:,.2f}</div>
            <span class="badge">🔥 المؤشر البصري الأبرز</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">متوسط الكمية المطلوبة</div>
            <div class="kpi-value">{avg_quantity:,.2f} <span style="font-size: 1.1rem; color: #64748B;">وحدة</span></div>
            <span class="badge" style="background-color: #F1F5F9; color: #475569;">معدل شراء ثابت</span>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">الفئة العمرية الأكثر إقبالاً</div>
            <div class="kpi-value">{top_age_group}</div>
            <span class="badge" style="background-color: #F1F5F9; color: #475569;">سنة</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 8. الرسوم البيانية الثلاثة المتناسقة (عمودي معتدل)
# ==========================================
chart_col1, chart_col2, chart_col3 = st.columns(3)

with chart_col1:
    st.markdown('<div class="section-title">📈 الاتجاه الشهري لمتوسط المبيعات</div>', unsafe_allow_html=True)
    if not df_monthly.empty:
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Scatter(
            x=df_monthly['MONTH_name'],
            y=df_monthly['Total_Amount_avg'],
            mode='lines+markers+text',
            text=df_monthly['Total_Amount_avg'],
            textposition='top center',
            textfont=dict(family="Tajawal", size=11, color="#1E293B"),
            name='متوسط المبلغ',
            line=dict(color=primary_color, width=3, shape='spline'),
            marker=dict(size=7, color=primary_color),
            fill='tozeroy',
            fillcolor=f"rgba(124, 58, 237, 0.08)"
        ))
        fig_monthly.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=30, b=10),
            height=300,
            font=dict(family="Tajawal", size=13, color="#334155"),
            xaxis=dict(showgrid=False, title="", tickfont=dict(size=11, color="#1E293B", weight="bold")),
            yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="", tickfont=dict(size=11, color="#64748B")),
            hovermode="x unified"
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.info("لا توجد بيانات متاحة لعرضها في الاتجاه الشهري.")

with chart_col2:
    st.markdown('<div class="section-title">🛍️ أكثر فئات المنتجات شراءً</div>', unsafe_allow_html=True)
    if not df_products.empty:
        fig_products = px.bar(
            df_products,
            x='Product Category',
            y='Total_Quantity',
            text='Total_Quantity'
        )
        # تم ضبط عرض الأعمدة (bargap / width) لتكون معتدلة وليست عريضة جداً
        fig_products.update_traces(
            marker_color=chart_color,
            marker_line_color="#FFFFFF",
            marker_line_width=1.5,
            opacity=0.9,
            textfont=dict(family="Tajawal", size=11, color="#FFFFFF"),
            textposition='inside',
            width=0.45  # تحكم بعرض الأعمدة لتصبح معتدلة
        )
        fig_products.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            font=dict(family="Tajawal", size=13, color="#334155"),
            xaxis=dict(showgrid=False, title="", tickfont=dict(size=11, color="#1E293B", weight="bold")),
            yaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="", tickfont=dict(size=11, color="#64748B"))
        )
        st.plotly_chart(fig_products, use_container_width=True)
    else:
        st.info("لا توجد بيانات منتجات متاحة لعرضها.")

with chart_col3:
    st.markdown('<div class="section-title">📊 المبيعات حسب الفئات العمرية</div>', unsafe_allow_html=True)
    if not df_age.empty:
        fig_age = px.bar(
            df_age,
            x='Total Amount_avg',
            y='range_age',
            orientation='h',
            text='Total Amount_avg'
        )
        fig_age.update_traces(
            marker_color=chart_color,
            marker_line_color="#FFFFFF",
            marker_line_width=1.5,
            opacity=0.9,
            textfont=dict(family="Tajawal", size=12, color="#FFFFFF"),
            textposition='inside'
        )
        fig_age.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            font=dict(family="Tajawal", size=13, color="#334155"),
            xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="", tickfont=dict(size=11, color="#64748B")),
            yaxis=dict(showgrid=False, title="", tickfont=dict(size=13, color="#1E293B", weight="bold"))
        )
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.info("لا توجد بيانات متاحة لعرضها في الفئات العمرية.")