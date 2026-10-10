"""
SmartBill - Mini App Fintech Quản lý & Tính tiền Hàng quán
Presentation + Interactive Demo + AI Chatbot
Phong cách: Bá Khí - Hiện đại, mạnh mẽ, chuyên nghiệp
Nhóm: Nguyễn Anh Khoa, Vũ Quang Huân, Nguyễn Văn Tuân, Phan Hữu Chánh, Đỗ Nguyễn An, Nguyễn Anh Hào
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from modules.db import init_db, save_order, load_orders, delete_order, clear_all_orders
from modules.pdf_export import generate_pdf
init_db()

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="SmartBill | Bá Khí Team",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== CUSTOM CSS - BÁ KHÍ TRENDY STYLE ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    :root {
        --primary: #FF6B35;
        --primary-dark: #E55A2B;
        --secondary: #004E89;
        --accent: #F7C59F;
        --bg-dark: #0B132B;
        --bg-card: #1C2541;
        --bg-light: #3A506B;
        --text: #FFFFFF;
        --text-muted: #A8B2D1;
        --success: #2EC4B6;
        --warning: #FF9F1C;
        --danger: #E71D36;
        --gradient: linear-gradient(135deg, #FF6B35 0%, #004E89 100%);
        --gradient-gold: linear-gradient(135deg, #F7C59F 0%, #FF6B35 100%);
    }
    
    html, body, [class*="css"] {
        font-family: 'Be Vietnam Pro', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(160deg, #0B132B 0%, #1C2541 40%, #0B132B 100%);
        background-attachment: fixed;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B132B 0%, #1C2541 100%);
        border-right: 1px solid rgba(255,107,53,0.2);
    }
    
    [data-testid="stSidebar"] .stMarkdown h1, 
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #FF6B35 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #FFFFFF !important;
    }
    
    /* Cards */
    .hero-card {
        background: var(--gradient);
        border-radius: 20px;
        padding: 2.5rem;
        color: white;
        box-shadow: 0 20px 40px rgba(255,107,53,0.25);
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: rgba(255,255,255,0.08);
        transform: rotate(15deg);
    }
    
    .feature-card {
        background: rgba(28, 37, 65, 0.85);
        border: 1px solid rgba(255,107,53,0.15);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        border-color: #FF6B35;
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(255,107,53,0.2);
    }
    
    .metric-card {
        background: linear-gradient(145deg, #1C2541, #0B132B);
        border: 1px solid rgba(46,196,182,0.3);
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2EC4B6;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #A8B2D1;
        margin-top: 0.25rem;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: var(--gradient-gold);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .badge {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-primary { background: rgba(255,107,53,0.2); color: #FF6B35; border: 1px solid #FF6B35; }
    .badge-success { background: rgba(46,196,182,0.2); color: #2EC4B6; border: 1px solid #2EC4B6; }
    .badge-info { background: rgba(0,78,137,0.3); color: #7EB8E8; border: 1px solid #004E89; }
    
    .team-card {
        background: rgba(28, 37, 65, 0.9);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        border: 1px solid rgba(255,107,53,0.2);
        transition: all 0.3s;
    }
    
    .team-card:hover {
        border-color: #FF6B35;
        box-shadow: 0 8px 25px rgba(255,107,53,0.25);
    }
    
    .team-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: var(--gradient);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.75rem;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
    }
    
    .invoice-box {
        background: #1C2541;
        border: 2px dashed rgba(255,107,53,0.4);
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35, #E55A2B) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(255,107,53,0.4) !important;
    }
    
    /* Chat */
    [data-testid="stChatMessage"] {
        background: rgba(28, 37, 65, 0.7);
        border-radius: 12px;
        border: 1px solid rgba(255,107,53,0.15);
    }
    
    /* Progress / Steps */
    .step-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: rgba(28,37,65,0.6);
        border-radius: 12px;
        margin-bottom: 0.75rem;
        border-left: 4px solid #FF6B35;
    }
    
    .step-num {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: var(--gradient);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        flex-shrink: 0;
    }
    
    /* Hide Streamlit branding a bit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(28,37,65,0.8);
        border-radius: 10px;
        color: #A8B2D1;
        border: 1px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B35, #004E89) !important;
        color: white !important;
        border: none !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #2EC4B6 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA ====================
MENU_ITEMS = {
    "Cơm sườn": {"price": 45000, "category": "Cơm", "emoji": "🍖"},
    "Mì xào bò": {"price": 50000, "category": "Mì", "emoji": "🍜"},
    "Phở bò": {"price": 45000, "category": "Phở", "emoji": "🍲"},
    "Bún thịt nướng": {"price": 40000, "category": "Bún", "emoji": "🥗"},
    "Gà rán (phần)": {"price": 35000, "category": "Món chính", "emoji": "🍗"},
    "Nước ép cam": {"price": 20000, "category": "Đồ uống", "emoji": "🍊"},
    "Trà sữa": {"price": 30000, "category": "Đồ uống", "emoji": "🧋"},
    "Cà phê sữa": {"price": 25000, "category": "Đồ uống", "emoji": "☕"},
    "Bánh mì thịt": {"price": 25000, "category": "Ăn nhanh", "emoji": "🥖"},
    "Cơm gà": {"price": 40000, "category": "Cơm", "emoji": "🍗"},
    "Lẩu thái (nhỏ)": {"price": 120000, "category": "Lẩu", "emoji": "🥘"},
    "Sinh tố bơ": {"price": 35000, "category": "Đồ uống", "emoji": "🥑"},
}

TEAM = [
    {"name": "Nguyễn Anh Khoa", "id": "24030118", "role": "Leader / Dev"},
    {"name": "Vũ Quang Huân", "id": "24030092", "role": "UI/UX & Demo"},
    {"name": "Nguyễn Văn Tuân", "id": "24030100", "role": "Logic & Tính toán"},
    {"name": "Phan Hữu Chánh", "id": "24030116", "role": "Phân tích dữ liệu"},
    {"name": "Đỗ Nguyễn An", "id": "24030025", "role": "Fintech & Báo cáo"},
    {"name": "Nguyễn Anh Hào", "id": "24030029", "role": "Testing & Docs"},
]

# Knowledge base for chatbot
KNOWLEDGE = {
    "smartbill": "SmartBill là ứng dụng Mini App Fintech hỗ trợ quản lý món ăn, lập hóa đơn và tính tiền tại quán ăn. Được xây dựng bằng Python + Streamlit, giúp giảm thao tác thủ công, hạn chế sai sót và nâng cao hiệu quả phục vụ khách hàng.",
    "mục tiêu": "Mục tiêu chính của SmartBill: (1) Số hóa quy trình gọi món và lập hóa đơn, (2) Tính tiền nhanh chóng, chính xác với chiết khấu & VAT, (3) Hỗ trợ chia tiền, (4) Cung cấp dữ liệu để phân tích bán hàng, (5) Giao diện đơn giản, trực quan, dễ sử dụng.",
    "tính năng": "Các tính năng chính: Chọn món & quản lý số lượng (+/-), Thêm món vào hóa đơn, Tính tiền tự động (đơn giá × số lượng), Áp dụng chiết khấu & VAT, Chia tiền cho nhiều người, Phân tích đơn hàng & doanh thu.",
    "công nghệ": "Công nghệ sử dụng: Python (xử lý logic, tính toán), Streamlit (framework xây dựng giao diện web nhanh), Streamlit Cloud (triển khai online). Người dùng truy cập qua trình duyệt, không cần cài đặt.",
    "lợi ích": "Lợi ích: Giảm thời gian tính toán & ghi chép thủ công, Hạn chế sai sót, Tăng tốc độ phục vụ, Dễ quản lý đơn hàng, Dữ liệu số hóa hỗ trợ quyết định kinh doanh, Khách hàng được phục vụ nhanh & minh bạch.",
    "hạn chế": "Hạn chế hiện tại: Chưa tích hợp thanh toán điện tử hoàn chỉnh, Chưa có hệ thống tài khoản & phân quyền chi tiết, Chưa quản lý kho nguyên vật liệu chuyên sâu, Báo cáo phân tích còn ở mức cơ bản.",
    "tương lai": "Định hướng phát triển: Dashboard doanh thu trực quan, Quản lý kho (nhập-xuất-tồn), Phân tích dữ liệu dự đoán nhu cầu, Hóa đơn điện tử, Phiên bản di động (Android/iOS), Tích hợp cổng thanh toán.",
    "nhóm": "Nhóm Bá Khí gồm 6 thành viên: Nguyễn Anh Khoa (24030118), Vũ Quang Huân (24030092), Nguyễn Văn Tuân (24030100), Phan Hữu Chánh (24030116), Đỗ Nguyễn An (24030025), Nguyễn Anh Hào (24030029).",
    "đối tượng": "SmartBill phù hợp với: Quán ăn, Quán cà phê, Quán trà sữa, Cửa hàng có nhiều sản phẩm, Các mô hình kinh doanh ẩm thực cần quản lý gọi món & tính tiền nhanh.",
}

def chatbot_response(user_input: str) -> str:
    """Simple knowledge-based chatbot with keyword matching."""
    text = user_input.lower().strip()
    
    if not text:
        return "Bạn hãy hỏi tôi về SmartBill nhé! Ví dụ: 'SmartBill là gì?', 'Tính năng?', 'Công nghệ?', 'Lợi ích?'..."
    
    # Greetings
    if any(w in text for w in ["xin chào", "hello", "hi", "chào", "hey"]):
        return "Xin chào! 👋 Tôi là trợ lý AI của **SmartBill** – nhóm Bá Khí. Bạn muốn tìm hiểu về ứng dụng, tính năng, công nghệ hay cách sử dụng demo không?"
    
    # Specific matches
    if any(w in text for w in ["là gì", "giới thiệu", "smartbill", "ứng dụng"]):
        return KNOWLEDGE["smartbill"]
    
    if any(w in text for w in ["mục tiêu", "mục đích", "aim", "goal"]):
        return KNOWLEDGE["mục tiêu"]
    
    if any(w in text for w in ["tính năng", "chức năng", "feature", "làm được gì"]):
        return KNOWLEDGE["tính năng"]
    
    if any(w in text for w in ["công nghệ", "technology", "stack", "python", "streamlit", "xây dựng"]):
        return KNOWLEDGE["công nghệ"]
    
    if any(w in text for w in ["lợi ích", "benefit", "ưu điểm", "tại sao", "giá trị"]):
        return KNOWLEDGE["lợi ích"]
    
    if any(w in text for w in ["hạn chế", "nhược điểm", "limit", "yếu"]):
        return KNOWLEDGE["hạn chế"]
    
    if any(w in text for w in ["tương lai", "phát triển", "roadmap", "kế hoạch", "sắp tới"]):
        return KNOWLEDGE["tương lai"]
    
    if any(w in text for w in ["nhóm", "team", "thành viên", "ai làm", "bá khí"]):
        return KNOWLEDGE["nhóm"]
    
    if any(w in text for w in ["đối tượng", "ai dùng", "phù hợp", "quán"]):
        return KNOWLEDGE["đối tượng"]
    
    if any(w in text for w in ["cách dùng", "hướng dẫn", "demo", "sử dụng"]):
        return """**Cách sử dụng Demo SmartBill (v2.0):**
1. Vào tab **🛒 Demo Tương tác**
2. Chọn món từ danh sách (có thể lọc theo nhóm)
3. Điều chỉnh số lượng bằng nút **+ / −**
4. Điều chỉnh **Chiết khấu %** và **VAT %**
5. Có thể **Chia tiền** cho nhiều người
6. Xem tổng tiền realtime
7. Nhấn **✅ Xác nhận** → lưu vào SQLite
8. Nhấn **📄 Xuất PDF** để tải hóa đơn

Hệ thống tự động tính toán chính xác từng bước!"""

    if any(w in text for w in ["pdf", "xuất", "export", "in hóa đơn"]):
        return """Bạn có thể **xuất PDF** ngay trong tab **🛒 Demo Tương tác** (khi đã có món trong hóa đơn), hoặc xem lại đơn đã lưu trong **📊 Phân tích & Báo cáo** rồi xuất PDF từ từng đơn. Hóa đơn PDF có mã đơn, thời gian, bảng chi tiết, tổng tiền và chia tiền."""
    
    if any(w in text for w in ["cảm ơn", "thanks", "thank"]):
        return "Không có gì ạ! 😊 Nếu còn thắc mắc gì về SmartBill, cứ hỏi tiếp nhé. Chúc bạn một ngày tốt lành!"
    
    # Default
    return f"""Tôi chưa hiểu rõ câu hỏi "{user_input}". 

Bạn có thể hỏi về:
• **SmartBill là gì?**
• **Tính năng chính**
• **Công nghệ sử dụng**
• **Lợi ích / Hạn chế**
• **Định hướng tương lai**
• **Thành viên nhóm**
• **Cách dùng demo**

Hoặc thử diễn đạt khác nhé! 💡"""

# ==================== SESSION STATE ====================
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {item_name: qty}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Xin chào! 👋 Tôi là **trợ lý SmartBill** của nhóm Bá Khí.\n\nBạn có thể hỏi tôi bất cứ điều gì về dự án: tính năng, công nghệ, lợi ích, hạn chế, hoặc hướng dẫn sử dụng demo.\n\nHãy thử hỏi: *\"SmartBill là gì?\"* hoặc *\"Tính năng chính?\"*"}
    ]
if "page" not in st.session_state:
    st.session_state.page = "🏠 Trang chủ"
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "last_order_id" not in st.session_state:
    st.session_state.last_order_id = None

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 2.5rem;">🧾</div>
        <h2 style="margin:0; color:#FF6B35; font-family:'Space Grotesk';">SmartBill</h2>
        <p style="color:#A8B2D1; font-size:0.85rem; margin:0;">Bá Khí Team • Mini App Fintech</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle
    t1, t2 = st.columns(2)
    with t1:
        if st.button("🌙 Dark", use_container_width=True, key="btn_dark"):
            st.session_state.theme = "dark"
            st.rerun()
    with t2:
        if st.button("☀️ Light", use_container_width=True, key="btn_light"):
            st.session_state.theme = "light"
            st.rerun()

    st.markdown("---")
    
    pages = [
        "🏠 Trang chủ",
        "👥 Nhóm Bá Khí",
        "💡 Giới thiệu",
        "🎯 Vấn đề & Giải pháp",
        "🛒 Demo Tương tác",
        "⚙️ Tính năng chi tiết",
        "💻 Công nghệ",
        "📊 Phân tích & Báo cáo",
        "🔮 Hạn chế & Tương lai",
        "✅ Kết luận",
        "🤖 Chatbot AI",
    ]
    
    selected = st.radio("Điều hướng", pages, index=pages.index(st.session_state.page), label_visibility="collapsed")
    st.session_state.page = selected
    
    st.markdown("---")
    try:
        _ords = load_orders(100)
        _rev = sum(o["total"] for o in _ords)
        st.markdown(f"""
        <div style="text-align:center; font-size:0.78rem; color:#A8B2D1;">
            <p style="margin:0.15rem 0;">📦 Đơn đã lưu: <b style="color:#2EC4B6;">{len(_ords)}</b></p>
            <p style="margin:0.15rem 0;">💰 Doanh thu: <b style="color:#FF6B35;">{format_vnd(_rev)}</b></p>
            <p style="margin-top:0.5rem; font-size:0.7rem;">Python + Streamlit + SQLite</p>
            <p style="font-size:0.7rem;">© 2025 Nhóm Bá Khí • v2.0</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        st.markdown("""
        <div style="text-align:center; font-size:0.75rem; color:#A8B2D1;">
            <p>Python + Streamlit + SQLite</p>
            <p>© 2025 Nhóm Bá Khí • v2.0</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== HELPER FUNCTIONS ====================
def format_vnd(amount):
    return f"{amount:,.0f} ₫".replace(",", ".")

def calc_invoice(cart, discount_pct=0, vat_pct=10):
    items = []
    subtotal = 0
    for name, qty in cart.items():
        if qty > 0 and name in MENU_ITEMS:
            price = MENU_ITEMS[name]["price"]
            line_total = price * qty
            items.append({
                "Tên món": name,
                "Đơn giá": price,
                "Số lượng": qty,
                "Thành tiền": line_total,
                "emoji": MENU_ITEMS[name]["emoji"]
            })
            subtotal += line_total
    
    discount_amount = subtotal * (discount_pct / 100)
    after_discount = subtotal - discount_amount
    vat_amount = after_discount * (vat_pct / 100)
    total = after_discount + vat_amount
    
    return items, subtotal, discount_amount, after_discount, vat_amount, total

# ==================== PAGES ====================

# ---------- TRANG CHỦ ----------
if st.session_state.page == "🏠 Trang chủ":
    st.markdown("""
    <div class="hero-card">
        <h1 style="margin:0; font-size:2.8rem; color:white;">🧾 SmartBill</h1>
        <p style="font-size:1.3rem; margin:0.5rem 0 0; opacity:0.95;">Đơn giản hơn — Hiệu quả hơn</p>
        <p style="margin-top:1rem; font-size:1.05rem; opacity:0.9;">
            Mini App Fintech hỗ trợ quản lý món ăn, lập hóa đơn, tính tiền, chiết khấu, VAT & chia tiền<br>
            dành cho quán ăn, quán cà phê, trà sữa và các mô hình ẩm thực.
        </p>
        <div style="margin-top:1.5rem;">
            <span class="badge badge-primary">Python + Streamlit</span>
            <span class="badge badge-success">SQLite + PDF</span>
            <span class="badge badge-info">Fintech • v2.0</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        _db = load_orders(100)
        _rev = sum(o["total"] for o in _db)
        _cnt = len(_db)
    except Exception:
        _db, _rev, _cnt = [], 0, 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">99.8%</div>
            <div class="metric-label">Tỷ lệ chính xác</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">~3 phút</div>
            <div class="metric-label">Thời gian TB / đơn</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{_cnt}</div>
            <div class="metric-label">Đơn đã lưu (DB)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{format_vnd(_rev)}</div>
            <div class="metric-label">Doanh thu demo</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">✨ Điểm nổi bật</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#FF6B35; margin-top:0;">⚡ Nhanh + Chính xác</h3>
            <p style="color:#A8B2D1;">Tính tiền realtime, chiết khấu, VAT, chia tiền. Hạn chế sai sót, tăng tốc phục vụ.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#2EC4B6; margin-top:0;">💾 Lưu trữ bền vững</h3>
            <p style="color:#A8B2D1;">SQLite lưu đơn hàng. Xuất PDF chuyên nghiệp. Phân tích doanh thu realtime.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#F7C59F; margin-top:0;">🤖 Chatbot + Theme</h3>
            <p style="color:#A8B2D1;">Trợ lý AI giải đáp thắc mắc. Chuyển Dark/Light. UI polish cao cấp.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👉 Sử dụng **menu bên trái** để khám phá từng phần của dự án, hoặc thử ngay **🛒 Demo Tương tác** và **🤖 Chatbot AI**.")

# ---------- NHÓM ----------
elif st.session_state.page == "👥 Nhóm Bá Khí":
    st.markdown('<p class="section-title">👥 Nhóm Bá Khí</p>', unsafe_allow_html=True)
    st.markdown("**Đội ngũ phát triển SmartBill** — Đam mê công nghệ, quyết tâm mang giải pháp số hóa đến từng quán ăn.")
    
    cols = st.columns(3)
    for i, member in enumerate(TEAM):
        with cols[i % 3]:
            initials = "".join([w[0] for w in member["name"].split() if w[0].isupper()][-2:]) or member["name"][:2]
            st.markdown(f"""
            <div class="team-card">
                <div class="team-avatar">{initials}</div>
                <h4 style="margin:0; color:white;">{member['name']}</h4>
                <p style="color:#FF6B35; margin:0.25rem 0; font-size:0.9rem;">{member['id']}</p>
                <p style="color:#A8B2D1; font-size:0.85rem; margin:0;">{member['role']}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

# ---------- GIỚI THIỆU ----------
elif st.session_state.page == "💡 Giới thiệu":
    st.markdown('<p class="section-title">💡 Giới thiệu SmartBill</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card" style="margin-bottom:1.5rem;">
        <h3 style="color:#FF6B35; margin-top:0;">SmartBill là gì?</h3>
        <p style="color:#E0E6F0; font-size:1.05rem; line-height:1.7;">
            <strong>SmartBill</strong> là ứng dụng được xây dựng nhằm hỗ trợ quán ăn trong việc lựa chọn món, 
            quản lý số lượng, lập hóa đơn và tính tổng tiền. Hệ thống giúp giảm các thao tác thủ công, 
            hạn chế sai sót và nâng cao hiệu quả phục vụ khách hàng.
        </p>
        <p style="color:#A8B2D1;">
            Đây là một <strong>Mini App Fintech</strong> tích hợp các nghiệp vụ tài chính cơ bản: 
            tính tiền, chiết khấu, VAT, chia tiền — tất cả trên một giao diện web đơn giản, 
            truy cập qua trình duyệt, không cần cài đặt phức tạp.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#2EC4B6;">🎯 Mục tiêu chính</h4>
            <ul style="color:#A8B2D1; line-height:1.8;">
                <li>Số hóa quy trình gọi món & lập hóa đơn</li>
                <li>Tính tiền nhanh, chính xác với chiết khấu & VAT</li>
                <li>Hỗ trợ chia tiền cho nhóm khách</li>
                <li>Cung cấp dữ liệu phân tích bán hàng</li>
                <li>Giao diện trực quan, dễ sử dụng</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#F7C59F;">🏪 Phù hợp với</h4>
            <ul style="color:#A8B2D1; line-height:1.8;">
                <li>Quán ăn, quán cơm, quán phở</li>
                <li>Quán cà phê, trà sữa</li>
                <li>Cửa hàng có nhiều sản phẩm</li>
                <li>Các mô hình ẩm thực cần tính tiền nhanh</li>
                <li>Nhân viên muốn giảm thao tác thủ công</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------- VẤN ĐỀ & GIẢI PHÁP ----------
elif st.session_state.page == "🎯 Vấn đề & Giải pháp":
    st.markdown('<p class="section-title">🎯 Vấn đề & Giải pháp</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card" style="border-left: 4px solid #E71D36;">
            <h3 style="color:#E71D36; margin-top:0;">❌ Vấn đề hiện tại</h3>
            <ul style="color:#A8B2D1; line-height:1.9;">
                <li>Ghi chép & tính tiền thủ công dễ sai sót</li>
                <li>Khách gọi nhiều món → khó kiểm soát số lượng</li>
                <li>Cộng tổng tiền mất nhiều thời gian</li>
                <li>Giờ cao điểm tốc độ phục vụ bị ảnh hưởng</li>
                <li>Khó kiểm tra lại các món khách đã gọi</li>
                <li>Thiếu dữ liệu để theo dõi tình hình bán hàng</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card" style="border-left: 4px solid #2EC4B6;">
            <h3 style="color:#2EC4B6; margin-top:0;">✅ Giải pháp SmartBill</h3>
            <ul style="color:#A8B2D1; line-height:1.9;">
                <li>Số hóa toàn bộ quy trình chọn món → tính tiền</li>
                <li>Điều chỉnh số lượng trực quan bằng nút +/-</li>
                <li>Tự động tính thành tiền, chiết khấu, VAT</li>
                <li>Hóa đơn tập trung, dễ kiểm tra & xác nhận</li>
                <li>Hỗ trợ chia tiền cho nhiều người</li>
                <li>Lưu dữ liệu đơn hàng để phân tích sau này</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">🔄 Quy trình hoạt động</p>', unsafe_allow_html=True)
    
    steps = [
        ("1", "Chọn món", "Nhân viên lựa chọn món khách yêu cầu từ danh mục"),
        ("2", "Điều chỉnh số lượng", "Dùng nút + / - để tăng hoặc giảm số lượng"),
        ("3", "Thêm vào hóa đơn", "Đưa món đã chọn vào đơn hàng"),
        ("4", "Kiểm tra hóa đơn", "Xem lại món, số lượng, thành tiền"),
        ("5", "Áp dụng CK / VAT", "Thiết lập chiết khấu & thuế nếu cần"),
        ("6", "Tính tiền & Thanh toán", "Hệ thống tổng hợp, khách thanh toán theo số trên hóa đơn"),
    ]
    
    for num, title, desc in steps:
        st.markdown(f"""
        <div class="step-item">
            <div class="step-num">{num}</div>
            <div>
                <strong style="color:white;">{title}</strong><br>
                <span style="color:#A8B2D1; font-size:0.9rem;">{desc}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------- DEMO TƯƠNG TÁC ----------
elif st.session_state.page == "🛒 Demo Tương tác":
    st.markdown('<p class="section-title">🛒 Demo SmartBill — Tương tác trực tiếp</p>', unsafe_allow_html=True)
    st.caption("Trải nghiệm quy trình chọn món → tính tiền như tại quán thật. Dữ liệu chỉ mang tính minh họa.")
    
    # Controls
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("#### 📋 Danh mục món")
        
        # Filter by category
        categories = ["Tất cả"] + sorted(list(set(v["category"] for v in MENU_ITEMS.values())))
        cat = st.selectbox("Lọc theo nhóm", categories, key="cat_filter")
        
        filtered = {k: v for k, v in MENU_ITEMS.items() if cat == "Tất cả" or v["category"] == cat}
        
        # Display menu as cards in grid
        menu_cols = st.columns(2)
        for idx, (name, info) in enumerate(filtered.items()):
            with menu_cols[idx % 2]:
                current_qty = st.session_state.cart.get(name, 0)
                st.markdown(f"""
                <div style="background:rgba(28,37,65,0.8); border-radius:12px; padding:0.9rem; margin-bottom:0.6rem; border:1px solid rgba(255,107,53,0.15);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.3rem;">{info['emoji']}</span>
                        <span style="color:#2EC4B6; font-weight:600;">{format_vnd(info['price'])}</span>
                    </div>
                    <div style="color:white; font-weight:500; margin:0.3rem 0;">{name}</div>
                    <div style="color:#A8B2D1; font-size:0.8rem;">{info['category']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                c_a, c_b, c_c = st.columns([1, 1.2, 1])
                with c_a:
                    if st.button("➖", key=f"minus_{name}", use_container_width=True):
                        if current_qty > 0:
                            st.session_state.cart[name] = current_qty - 1
                            if st.session_state.cart[name] == 0:
                                del st.session_state.cart[name]
                            st.rerun()
                with c_b:
                    st.markdown(f"<div style='text-align:center; padding:0.4rem; color:white; font-weight:700;'>{current_qty}</div>", unsafe_allow_html=True)
                with c_c:
                    if st.button("➕", key=f"plus_{name}", use_container_width=True):
                        st.session_state.cart[name] = current_qty + 1
                        st.rerun()
    
    with col_right:
        st.markdown("#### 🧾 Hóa đơn")
        
        discount = st.slider("Chiết khấu (%)", 0, 30, 0, 1)
        vat = st.slider("VAT (%)", 0, 15, 10, 1)
        split_n = st.number_input("Chia tiền cho (người)", 1, 20, 1)
        
        items, subtotal, disc_amt, after_disc, vat_amt, total = calc_invoice(st.session_state.cart, discount, vat)
        
        if not items:
            st.markdown("""
            <div class="invoice-box" style="text-align:center; color:#A8B2D1;">
                <p style="font-size:2rem; margin:0;">🛒</p>
                <p>Chưa có món nào.<br>Hãy chọn món từ danh mục bên trái!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="invoice-box">', unsafe_allow_html=True)
            for it in items:
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:0.4rem 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                    <span style="color:#E0E6F0;">{it['emoji']} {it['Tên món']} × {it['Số lượng']}</span>
                    <span style="color:#2EC4B6; font-weight:600;">{format_vnd(it['Thành tiền'])}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="margin-top:1rem; padding-top:0.8rem; border-top:1px solid rgba(255,107,53,0.3);">
                <div style="display:flex; justify-content:space-between; color:#A8B2D1;"><span>Tạm tính</span><span>{format_vnd(subtotal)}</span></div>
                <div style="display:flex; justify-content:space-between; color:#FF9F1C;"><span>Chiết khấu ({discount}%)</span><span>-{format_vnd(disc_amt)}</span></div>
                <div style="display:flex; justify-content:space-between; color:#A8B2D1;"><span>VAT ({vat}%)</span><span>+{format_vnd(vat_amt)}</span></div>
                <div style="display:flex; justify-content:space-between; margin-top:0.6rem; font-size:1.25rem; font-weight:700; color:white;">
                    <span>TỔNG CỘNG</span><span style="color:#FF6B35;">{format_vnd(total)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if split_n > 1:
                per_person = total / split_n
                st.markdown(f"""
                <div style="margin-top:0.8rem; padding:0.7rem; background:rgba(46,196,182,0.15); border-radius:8px; text-align:center;">
                    <span style="color:#2EC4B6;">Chia {split_n} người → mỗi người: <strong>{format_vnd(per_person)}</strong></span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            c_btn1, c_btn2, c_btn3 = st.columns(3)
            with c_btn1:
                if st.button("✅ Xác nhận", use_container_width=True, key="confirm_order"):
                    order_id = save_order(items, subtotal, disc_amt, vat_amt, total, split_n)
                    st.session_state.last_order_id = order_id
                    st.session_state.cart = {}
                    st.success(f"Đã lưu đơn #{order_id} — {format_vnd(total)}")
                    st.balloons()
                    st.rerun()
            with c_btn2:
                pdf_buf = generate_pdf(items, subtotal, disc_amt, vat_amt, total, split_n)
                st.download_button(
                    label="📄 Xuất PDF",
                    data=pdf_buf,
                    file_name=f"SmartBill_HD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="pdf_download_live"
                )
            with c_btn3:
                if st.button("🗑️ Xóa", use_container_width=True, key="clear_cart"):
                    st.session_state.cart = {}
                    st.rerun()
        
        # Quick stats from DB
        try:
            db_orders = load_orders(50)
            if db_orders:
                st.markdown("---")
                st.markdown(f"**Đơn đã lưu:** {len(db_orders)} &nbsp;|&nbsp; **Doanh thu:** {format_vnd(sum(o['total'] for o in db_orders))}")
        except Exception:
            pass

# ---------- TÍNH NĂNG CHI TIẾT ----------
elif st.session_state.page == "⚙️ Tính năng chi tiết":
    st.markdown('<p class="section-title">⚙️ Tính năng chi tiết</p>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Quản lý số lượng", "Hóa đơn & Tính tiền", "Chiết khấu / VAT / Chia tiền", "Phân tích đơn hàng"])
    
    with tabs[0]:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#FF6B35;">Quản lý số lượng món</h3>
            <p style="color:#A8B2D1;">SmartBill cho phép điều chỉnh số lượng món trực tiếp trên giao diện:</p>
            <ul style="color:#E0E6F0;">
                <li><strong>Nút ➕</strong>: Tăng số lượng món khách gọi</li>
                <li><strong>Nút ➖</strong>: Giảm số lượng</li>
                <li>Không cần nhập số lượng thủ công → hạn chế nhầm lẫn</li>
                <li>Phù hợp khi khách gọi nhiều món cùng lúc</li>
            </ul>
            <p style="color:#2EC4B6;"><strong>Lợi ích:</strong> Thao tác nhanh, dễ sử dụng, tăng độ chính xác của nhân viên.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#FF6B35;">Hóa đơn & Tính tiền</h3>
            <p style="color:#A8B2D1;">Hóa đơn là nơi tổng hợp toàn bộ món khách đã lựa chọn.</p>
            <p style="color:#E0E6F0;"><strong>Công thức:</strong></p>
            <ul style="color:#E0E6F0;">
                <li>Thành tiền = Đơn giá × Số lượng</li>
                <li>Tổng tiền hàng = Σ Thành tiền các món</li>
                <li>Hệ thống tự động tổng hợp giá trị đơn hàng</li>
            </ul>
            <p style="color:#2EC4B6;">Việc tổng hợp trên một giao diện giúp nhân viên dễ kiểm tra và hạn chế sai sót.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#FF6B35;">Chiết khấu, VAT & Chia tiền</h3>
            <p style="color:#A8B2D1;">SmartBill hỗ trợ các nghiệp vụ tài chính quan trọng:</p>
            <ul style="color:#E0E6F0;">
                <li><strong>Chiết khấu:</strong> Áp dụng mức giảm giá theo chính sách quán</li>
                <li><strong>VAT:</strong> Tính thuế GTGT vào giá trị thanh toán</li>
                <li><strong>Chia tiền:</strong> Chia tổng hóa đơn cho nhiều người trong cùng một đơn</li>
            </ul>
            <p style="color:#FF9F1C;"><strong>Công thức:</strong> Tiền thanh toán = (Tổng hàng − Chiết khấu) + VAT</p>
            <p style="color:#2EC4B6;">Các nghiệp vụ này giúp quán hoạt động minh bạch và chuyên nghiệp hơn.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#FF6B35;">Phân tích đơn hàng</h3>
            <p style="color:#A8B2D1;">Dữ liệu từ các đơn hàng được sử dụng để theo dõi hoạt động và tối ưu kinh doanh:</p>
            <ul style="color:#E0E6F0;">
                <li>Phân tích cơ bản (số đơn, doanh thu)</li>
                <li>Phân tích xu hướng</li>
                <li>Phân tích hiệu suất phục vụ</li>
            </ul>
            <p style="color:#2EC4B6;"><strong>Lợi ích:</strong> Dữ liệu bán hàng → Phân tích → Đánh giá → Quyết định kinh doanh.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- CÔNG NGHỆ ----------
elif st.session_state.page == "💻 Công nghệ":
    st.markdown('<p class="section-title">💻 Công nghệ xây dựng SmartBill</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card" style="text-align:center;">
            <div style="font-size:2.5rem;">🐍</div>
            <h3 style="color:#FF6B35;">Python</h3>
            <p style="color:#A8B2D1;">Xử lý logic, tính toán, quản lý dữ liệu. Nền tảng của toàn bộ ứng dụng.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card" style="text-align:center;">
            <div style="font-size:2.5rem;">⚡</div>
            <h3 style="color:#FF6B35;">Streamlit</h3>
            <p style="color:#A8B2D1;">Framework Python xây dựng giao diện web nhanh. Hiển thị dữ liệu trực quan.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card" style="text-align:center;">
            <div style="font-size:2.5rem;">☁️</div>
            <h3 style="color:#FF6B35;">Streamlit Cloud</h3>
            <p style="color:#A8B2D1;">Triển khai và vận hành trực tuyến. Người dùng truy cập qua trình duyệt.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <h4 style="color:#2EC4B6;">Luồng xử lý</h4>
        <p style="color:#A8B2D1;">
            <strong>Người dùng (Quản lý)</strong> → Yêu cầu tính tiền, thêm món → 
            <strong>Giao diện Streamlit</strong> → 
            <strong>Xử lý Python</strong> (tính tổng, VAT, chiết khấu, chia tiền) → 
            <strong>Hóa đơn chi tiết & Báo cáo</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------- PHÂN TÍCH ----------
elif st.session_state.page == "📊 Phân tích & Báo cáo":
    st.markdown('<p class="section-title">📊 Phân tích & Báo cáo</p>', unsafe_allow_html=True)
    
    db_orders = load_orders(100)
    
    if not db_orders:
        st.info("Chưa có đơn hàng nào trong database. Hãy vào **🛒 Demo Tương tác** tạo vài đơn (nhấn Xác nhận), sau đó quay lại đây!")
        
        # Demo sample data
        st.markdown("#### Dữ liệu minh họa (mẫu)")
        sample_data = pd.DataFrame({
            "Món": list(MENU_ITEMS.keys())[:8],
            "Số lượng bán": [12, 18, 15, 9, 14, 22, 11, 8],
            "Doanh thu": [45000*12, 50000*18, 45000*15, 40000*9, 35000*14, 20000*22, 30000*11, 25000*8]
        })
        
        fig = px.bar(sample_data, x="Món", y="Số lượng bán", color="Doanh thu",
                     color_continuous_scale=["#004E89", "#FF6B35"],
                     title="Top món bán chạy (mẫu)")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#A8B2D1",
            title_font_color="#FFFFFF"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        fig2 = px.pie(sample_data, values="Doanh thu", names="Món", title="Cơ cấu doanh thu theo món (mẫu)",
                      color_discrete_sequence=px.colors.sequential.Oranges_r)
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#A8B2D1", title_font_color="#FFFFFF")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        # Real DB data
        total_orders = len(db_orders)
        total_revenue = sum(o["total"] for o in db_orders)
        avg_order = total_revenue / total_orders if total_orders else 0
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Số đơn", total_orders)
        m2.metric("Doanh thu", format_vnd(total_revenue))
        m3.metric("TB / đơn", format_vnd(avg_order))
        m4.metric("Đơn gần nhất", f"#{db_orders[0]['id']}")
        
        # Aggregate items
        item_count = {}
        item_rev = {}
        for o in db_orders:
            for it in o["items"]:
                name = it.get("Tên món", "?")
                qty = it.get("Số lượng", 0)
                tt = it.get("Thành tiền", 0)
                item_count[name] = item_count.get(name, 0) + qty
                item_rev[name] = item_rev.get(name, 0) + tt
        
        if item_count:
            df = pd.DataFrame([{"Món": k, "Số lượng": v, "Doanh thu": item_rev.get(k, 0)} for k, v in item_count.items()])
            df = df.sort_values("Số lượng", ascending=False)
            fig = px.bar(df, x="Món", y="Số lượng", color="Doanh thu",
                         color_continuous_scale=["#004E89", "#FF6B35"],
                         title="Số lượng món đã bán (từ DB)")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              font_color="#A8B2D1", title_font_color="#FFFFFF")
            st.plotly_chart(fig, use_container_width=True)
            
            fig2 = px.pie(df, values="Doanh thu", names="Món", title="Cơ cấu doanh thu theo món",
                          color_discrete_sequence=px.colors.sequential.Oranges_r)
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#A8B2D1", title_font_color="#FFFFFF")
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("#### Chi tiết các đơn đã lưu")
        for o in db_orders:
            time_str = o["time"]
            try:
                time_str = datetime.fromisoformat(o["time"]).strftime("%H:%M:%S %d/%m/%Y")
            except Exception:
                pass
            with st.expander(f"Đơn #{o['id']} — {time_str} — {format_vnd(o['total'])}"):
                if o["items"]:
                    st.dataframe(pd.DataFrame(o["items"])[["Tên món", "Số lượng", "Thành tiền"]], use_container_width=True, hide_index=True)
                st.write(f"Chiết khấu: {format_vnd(o['discount'])} | VAT: {format_vnd(o['vat'])} | Chia: {o['split']} người")
                c1, c2 = st.columns(2)
                with c1:
                    pdf_buf = generate_pdf(o["items"], o["subtotal"], o["discount"], o["vat"], o["total"], o["split"], o["id"], time_str)
                    st.download_button("📄 Xuất PDF đơn này", data=pdf_buf,
                                       file_name=f"SmartBill_HD_{o['id']}.pdf", mime="application/pdf",
                                       key=f"pdf_{o['id']}")
                with c2:
                    if st.button("🗑️ Xóa đơn", key=f"del_{o['id']}"):
                        delete_order(o["id"])
                        st.rerun()
        
        st.markdown("---")
        if st.button("⚠️ Xóa toàn bộ lịch sử đơn", type="secondary"):
            clear_all_orders()
            st.success("Đã xóa toàn bộ đơn.")
            st.rerun()

# ---------- HẠN CHẾ & TƯƠNG LAI ----------
elif st.session_state.page == "🔮 Hạn chế & Tương lai":
    st.markdown('<p class="section-title">🔮 Hạn chế & Định hướng phát triển</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card" style="border-left:4px solid #E71D36;">
            <h3 style="color:#E71D36;">⚠️ Hạn chế hiện tại</h3>
            <ul style="color:#A8B2D1; line-height:1.9;">
                <li>Chưa tích hợp hoàn chỉnh cổng thanh toán điện tử</li>
                <li>Hệ thống tài chính & dữ liệu còn ở mức khởi đầu</li>
                <li>Chưa có hệ thống tài khoản & phân quyền chi tiết</li>
                <li>Chưa quản lý kho nguyên vật liệu chuyên sâu</li>
                <li>Báo cáo & phân tích còn có thể phát triển thêm</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card" style="border-left:4px solid #2EC4B6;">
            <h3 style="color:#2EC4B6;">🚀 Định hướng tương lai</h3>
            <ul style="color:#A8B2D1; line-height:1.9;">
                <li><strong>Dashboard doanh thu</strong> trực quan bằng biểu đồ</li>
                <li><strong>Quản lý kho</strong>: nhập – xuất – tồn nguyên liệu</li>
                <li><strong>Phân tích dữ liệu</strong> dự đoán nhu cầu</li>
                <li><strong>Hóa đơn điện tử</strong>: tạo, xuất, lưu trữ</li>
                <li><strong>Phiên bản di động</strong> (Android & iOS)</li>
                <li>Tích hợp cổng thanh toán & tokenization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------- KẾT LUẬN ----------
elif st.session_state.page == "✅ Kết luận":
    st.markdown("""
    <div class="hero-card">
        <h1 style="margin:0; color:white;">✅ Kết luận</h1>
        <p style="font-size:1.2rem; margin-top:1rem; opacity:0.95;">
            <strong>SmartBill</strong> là giải pháp ứng dụng công nghệ nhằm số hóa quy trình quản lý và tính tiền tại quán ăn.
        </p>
        <p style="opacity:0.9; margin-top:0.8rem;">
            Hệ thống tập trung vào các hoạt động: chọn món nhanh chóng, quản lý số lượng, lập hóa đơn tự động, 
            tính tiền chính xác với chiết khấu & VAT, hỗ trợ chia tiền và cung cấp dữ liệu phân tích.
        </p>
        <p style="margin-top:1.2rem; font-size:1.1rem;">
            <em>Đơn giản hơn — Hiệu quả hơn — Minh bạch hơn</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">💎 Giá trị mang lại</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#FF6B35;">Với hoạt động kinh doanh</h4>
            <p style="color:#A8B2D1;">Thao tác nhanh → giảm thời gian phục vụ → hạn chế sai sót → hỗ trợ quyết định.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#2EC4B6;">Với khách hàng</h4>
            <p style="color:#A8B2D1;">Gọi món thuận tiện → hóa đơn rõ ràng → thanh toán nhanh chóng, minh bạch.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <h4 style="color:#F7C59F;">Với quản lý</h4>
            <p style="color:#A8B2D1;">Dữ liệu được số hóa → dễ phân tích → nâng cao hiệu quả quản lý.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("Cảm ơn thầy và các bạn đã lắng nghe! Nhóm Bá Khí sẵn sàng nhận mọi câu hỏi và góp ý.")

# ---------- CHATBOT ----------
elif st.session_state.page == "🤖 Chatbot AI":
    st.markdown('<p class="section-title">🤖 Trợ lý AI SmartBill</p>', unsafe_allow_html=True)
    st.caption("Hỏi bất cứ điều gì về dự án SmartBill, tính năng, công nghệ, nhóm phát triển...")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Input
    if prompt := st.chat_input("Hỏi trợ lý về SmartBill..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        response = chatbot_response(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # Quick questions
    st.markdown("---")
    st.markdown("**Gợi ý câu hỏi nhanh:**")
    qcols = st.columns(4)
    quick_qs = ["SmartBill là gì?", "Tính năng chính?", "Công nghệ sử dụng?", "Định hướng tương lai?"]
    for i, q in enumerate(quick_qs):
        with qcols[i]:
            if st.button(q, key=f"qq_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": q})
                resp = chatbot_response(q)
                st.session_state.chat_history.append({"role": "assistant", "content": resp})
                st.rerun()
