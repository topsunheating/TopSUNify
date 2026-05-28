import streamlit as st

# ==============================================================================
# ۱. پیکربندی صفحه و استایل‌های سفارشی (CSS) برای شبیه‌سازی اپلیکیشن موبایل
# ==============================================================================
st.set_page_config(
    page_title="TopSUNify | هوش مصنوعی گرمایش",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def inject_custom_css():
    css = """
    <style>
    /* تنظیم فونت و راست‌چین کردن کل بدنه برنامه */
    @import url('https://v1.fontapi.ir/css/Vazir');
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Vazir', sans-serif !important;
        background-color: #f8fafc !important;
    }
    
    /* مخفی کردن المان‌های پیش‌فرض و هدر استریم‌لیت برای ظاهر بومی موبایل */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 80px !important; /* فضای کافی برای اینکه محتوا زیر منوی پایینی نرود */
        max-width: 550px !important;
        margin: 0 auto !important;
    }

    /* مخفی کردن دکمه‌های ناوبری اصلی استریم‌لیت که در پس‌زمینه کار می‌کنند */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        display: none !important;
    }

    /* --- سیستم نوار ناوبری فیکس شده در پایین (Bottom Navigation) دقیقاً مشابه عکس ارسالی --- */
    .fixed-bottom-nav {
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 550px !important;
        height: 64px !important; /* ارتفاع استاندارد منوهای موبایلی */
        background-color: #ffffff !important;
        border-top: 1px solid #f1f5f9 !important; /* خط جداکننده بسیار ظریف و ملایم در بالای منو */
        z-index: 999999 !important;
        display: flex !important;
        justify-content: space-around !important;
        align-items: center !important;
        padding-bottom: env(safe-area-inset-bottom) !important;
        box-shadow: none !important; /* حذف سایه‌های ضخیم قدیمی برای تخت و ملو شدن طرح */
    }

    .nav-tab-item {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        color: #64748b !important; /* رنگ خاکستری ملایم و مات برای تب‌های غیرفعال */
        font-size: 10px !important; /* فونت کوچک، ظریف و منظم برای جا شدن هماهنگ ۶ تب */
        font-weight: 500 !important;
        background: none !important;
        border: none !important;
        cursor: pointer !important;
        width: 100% !important;
        height: 100% !important;
        gap: 4px !important;
        transition: all 0.2s ease !important;
    }

    /* استایل دکمه و تب فعال - رنگ نارنجی برند تاپسان با وزن فونت مشخص‌تر */
    .nav-tab-item.active-tab {
        color: #ea580c !important; 
        font-weight: bold !important;
    }

    /* ابعاد آیکون‌ها نسبت به نوشته زیرین */
    .nav-tab-icon {
        font-size: 20px !important;
        transition: transform 0.2s ease !important;
    }

    .nav-tab-item.active-tab .nav-tab-icon {
        transform: scale(1.1); /* بزرگنمایی بسیار خفیف آیکون در حالت فعال */
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# ==============================================================================
# ۲. مدیریت پایداری وضعیت برنامه (Session State)
# ==============================================================================
if "active-tab" not in st.session_state:
    st.session_state.active_tab = "dashboard"  # تب پیش‌فرض هنگام ورود به برنامه

# ==============================================================================
# ۳. هدر برنامه و لوگوی جدید تاپسان (ابتدا آیکون، سپس متن بر اساس اصلاحیه)
# ==============================================================================
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 25px; margin-top: 10px;">
        <img src="https://raw.githubusercontent.com/ArianSabet/TopSUNify/main/TopSUN-Powered.png" width="180" alt="TopSUN Heating">
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# ۴. دکمه‌های ناوبری پنهان استریم‌لیت (موتور محرک جاوااسکریپت منو)
# ==============================================================================
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("H_INV", key="hidden_inv"): st.session_state.active_tab = "invoice"
with col2:
    if st.button("H_SER", key="hidden_ser"): st.session_state.active_tab = "services"
with col3:
    if st.button("H_DAS", key="hidden_das"): st.session_state.active_tab = "dashboard"
with col4:
    if st.button("H_WAR", key="hidden_war"): st.session_state.active_tab = "warranty"
with col5:
    if st.button("H_INF", key="hidden_inf"): st.session_state.active_tab = "info"
with col6:
    if st.button("H_PRO", key="hidden_pro"): st.session_state.active_tab = "profile"

# ==============================================================================
# ۵. بخش رندر کردن محتوای هر تب (منطق و فرآیندهای برنامه شما)
# ==============================================================================
if st.session_state.active_tab == "dashboard":
    st.markdown("### 📊 داشبورد مدیریتی پروژه")
    st.write(f"جناب **رضا تلچی**، به سامانه هوشمند تاپسان خوش آمدید.")
    
    # نمونه فیلدهای متراژ که قبلاً پیاده کرده بودید
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        st.metric("متراژ کل فیلم عرض ۸۰", "0.0 م")
    with c_col2:
        st.metric("متراژ کل فیلم عرض ۴۰", "0.0 م")
        
    st.info("برای محاسبات مهندسی و بارگذاری نقشه، از منوی پایین گزینه «پیش‌فاکتور» را انتخاب کنید.")

elif st.session_state.active_tab == "invoice":
    st.markdown("### 🗂️ صدور پیش‌فاکتور و محاسبات")
    st.write("در این بخش می‌توانید نقشه‌های CAD خود را بارگذاری کرده و لیست متریال (BOM) را دریافت کنید.")
    # کدهای مربوط به پردازش DXF/DWG و فیلتر اقلام صفر در این بخش قرار می‌گیرد.

elif st.session_state.active_tab == "services":
    st.markdown("### 🛠️ خدمات فنی")
    st.write("درخواست‌های سرویس، نصب و اتصالات سیستم‌های گرمایشی.")

elif st.session_state.active_tab == "warranty":
    st.markdown("### 🛡️ ثبت و فعال‌سازی گارانتی")
    st.write("فرم ثبت سریال تجهیزات و فعال‌سازی گارانتی رسمی تاپسان.")

elif st.session_state.active_tab == "info":
    st.markdown("### 📖 اطلاعات فنی و استانداردها")
    st.write("دفترچه‌های راهنما، نقشه‌های استاندارد و کاتالوگ‌های فیلم‌های حرارتی.")

elif st.session_state.active_tab == "profile":
    st.markdown("### 👤 پروفایل کاربری")
    st.write("**کاربر:** رضا تلچی")
    st.write("**شماره تماس:** ۰۹۱۲۰۱۹۸۲۲۹")

# ==============================================================================
# 📱 ۶. نوار ناوبری موبایل سفارشی - کاملاً منطبق بر عکس دریافتی از شما
# ترتیب دقیق از راست به چپ: پیش فاکتور -> خدمات فنی -> داشبورد -> ثبت گارانتی -> اطلاعات فنی -> پروفایل
# ==============================================================================
active_invoice = "active-tab" if st.session_state.active_tab == "invoice" else ""
active_services = "active-tab" if st.session_state.active_tab == "services" else ""
active_dashboard = "active-tab" if st.session_state.active_tab == "dashboard" else ""
active_warranty = "active-tab" if st.session_state.active_tab == "warranty" else ""
active_info = "active-tab" if st.session_state.active_tab == "info" else ""
active_profile = "active-tab" if st.session_state.active_tab == "profile" else ""

bottom_navigation_html = f"""
<div class="fixed-bottom-nav">
    <button class="nav-tab-item {active_profile}" onclick="document.getElementById('b_pro').click();">
        <div class="nav-tab-icon">👤</div>
        <div>پروفایل</div>
    </button>
    <button class="nav-tab-item {active_info}" onclick="document.getElementById('b_inf').click();">
        <div class="nav-tab-icon">📖</div>
        <div>اطلاعات فنی</div>
    </button>
    <button class="nav-tab-item {active_warranty}" onclick="document.getElementById('b_war').click();">
        <div class="nav-tab-icon">🛡️</div>
        <div>ثبت گارانتی</div>
    </button>
    <button class="nav-tab-item {active_dashboard}" onclick="document.getElementById('b_das').click();">
        <div class="nav-tab-icon">📊</div>
        <div>داشبورد</div>
    </button>
    <button class="nav-tab-item {active_services}" onclick="document.getElementById('b_ser').click();">
        <div class="nav-tab-icon">🛠️</div>
        <div>خدمات فنی</div>
    </button>
    <button class="nav-tab-item {active_invoice}" onclick="document.getElementById('b_inv').click();">
        <div class="nav-tab-icon">🗂️</div>
        <div>پیش فاکتور</div>
    </button>
</div>

<script>
// ارتباط امن و بدون اختلال در نشست (Session State) با دکمه‌های مخفی استریم‌لیت
const parentDoc = window.parent.document;
function syncButtons() {{
    const btns = parentDoc.querySelectorAll('button[kind="secondary"]');
    btns.forEach(btn => {{
        if(btn.innerText.includes("H_INV")) btn.id = "b_inv";
        if(btn.innerText.includes("H_SER")) btn.id = "b_ser";
        if(btn.innerText.includes("H_DAS")) btn.id = "b_das";
        if(btn.innerText.includes("H_WAR")) btn.id = "b_war";
        if(btn.innerText.includes("H_INF")) btn.id = "b_inf";
        if(btn.innerText.includes("H_PRO")) btn.id = "b_pro";
    }});
}}
// اجرای مداوم برای اطمینان از صحت کارکرد دکمه‌ها در رندرهای متوالی صفحه
syncButtons();
setTimeout(syncButtons, 300);
</script>
"""

# رندر نهایی منوی ناوبری پایینی با کامپوننت HTML استریم‌لیت
st.components.v1.html(bottom_navigation_html, height=66)
