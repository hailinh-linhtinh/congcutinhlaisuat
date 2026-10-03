import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CẤU HÌNH TRANG & GIAO DIỆN HỒNG PASTEL ---
st.set_page_config(
    page_title="Máy Tính Tiết Kiệm Màu Hồng",
    page_icon="🌸",
    layout="wide",
)

# CSS tùy chỉnh giao diện hồng pastel và hiệu ứng
st.markdown("""
    <style>
    /* Màu nền chung và font chữ */
    .stApp {
        background-color: #FFF0F5;
        color: #4A4A4A;
    }
    
    /* Tiêu đề chính */
    h1, h2, h3 {
        color: #D87093 !important;
        font-family: 'Helvetica', sans-serif;
    }
    
    /* Tùy chỉnh các khối thông tin (metric card) */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
        border: 1px solid #FFC0CB;
    }
    div[data-testid="stMetric"] label {
        color: #DB7093 !important;
        font-weight: bold;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #C71585 !important;
    }
    
    /* Nút bấm dễ thương */
    .stButton>button {
        background-color: #FFB6C1;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        border: none;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(255, 192, 203, 0.5);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF69B4;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Thanh kéo */
    .stSlider slider {
        accent-color: #FF69B4;
    }
    </style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ỨNG DỤNG ---
st.title("🌸 Trạm Tiết Kiệm Hồng Pastel 🌸")
st.markdown("Cùng lập kế hoạch tài chính thật xinh xắn và ngọt ngào cho tương lai của bạn nhé! ✨")
st.markdown("---")

# --- KHU VỰC NHẬP LIỆU BẰNG THANH KÉO (SLIDER) ---
st.subheader("🌷 Nhập thông tin khoản tiết kiệm")

col_input1, col_input2 = st.columns(2)

with col_input1:
    # Số tiền gửi từ 1 triệu đến 5 tỷ VNĐ
    so_tien_gui = st.slider(
        "💰 Số tiền gửi (VNĐ)",
        min_value=1_000_000,
        max_value=5_000_000_000,
        value=50_000_000,
        step=1_000_000,
        format="%d VNĐ"
    )
    st.write(f"Đã chọn: **{so_tien_gui:,.0f} VNĐ**")

    # Kỳ hạn gửi từ 1 đến 36 tháng
    ky_han_thang = st.slider(
        "⏳ Kỳ hạn gửi (Tháng)",
        min_value=1,
        max_value=36,
        value=12,
        step=1
    )

with col_input2:
    # Lãi suất từ 0.1% đến 15% / năm
    lai_suat_nam = st.slider(
        "📈 Lãi suất (% / năm)",
        min_value=0.1,
        max_value=15.0,
        value=6.0,
        step=0.1
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "🎁 Hình thức nhận lãi",
        ["Cuối kỳ", "Hàng tháng", "Hàng quý"]
    )

    loai_lai = st.radio(
        "⚡ Chọn loại lãi",
        ["Lãi đơn", "Lãi kép"],
        horizontal=True
    )

st.markdown("---")

# --- NÚT TÍNH TOÁN VÀ HIỆU ỨNG ĐỘNG ---
if st.button("✨ Tính Toán Ngay Thôi ✨"):
    # Hiệu ứng chờ nhẹ nhàng
    with st.spinner("Đang tính toán những con số tài lộc cho bạn... 🎀"):
        time.sleep(0.6)
    
    # Hiệu ứng pháo hoa chúc mừng (hiệu ứng động "qua o")
    st.balloons()

    # --- LOGIC TÍNH TOÁN ---
    r_thang = (lai_suat_nam / 100) / 12
    tong_so_thang = ky_han_thang
    
    tien_lai_dinh_ky = 0
    tong_tien_lai = 0
    tong_goc_va_lai = 0

    if loai_lai == "Lãi đơn":
        # Lãi đơn: Tiền lãi mỗi tháng tính trên số gốc ban đầu
        tien_lai_hang_thang = so_tien_gui * r_thang
        tong_tien_lai = tien_lai_hang_thang * tong_so_thang
        tong_goc_va_lai = so_tien_gui + tong_tien_lai
        
        if hinh_thuc_nhan_lai == "Hàng tháng":
            tien_lai_dinh_ky = tien_lai_hang_thang
        elif hinh_thuc_nhan_lai == "Hàng quý":
            tien_lai_dinh_ky = tien_lai_hang_thang * 3
        else:
            tien_lai_dinh_ky = tong_tien_lai
            
    else:  # Lãi kép
        if hinh_thuc_nhan_lai == "Cuối kỳ" or hinh_thuc_nhan_lai == "Lãi kép toàn bộ":
            # Gốc + lãi nhập gốc liên tục hàng tháng
            tong_goc_va_lai = so_tien_gui * ((1 + r_thang) ** tong_so_thang)
            tong_tien_lai = tong_goc_va_lai - so_tien_gui
            tien_lai_dinh_ky = tong_tien_lai / tong_so_thang  # Giá trị trung bình hàng tháng
        else:
            # Nếu chọn nhận lãi hàng tháng/quý mà là lãi kép thì thường là khách rút lãi tiêu, phần gốc giữ nguyên
            # Ở đây chuẩn hóa công thức lãi kép tái đầu tư hàng tháng
            tong_goc_va_lai = so_tien_gui * ((1 + r_thang) ** tong_so_thang)
            tong_tien_lai = tong_goc_va_lai - so_tien_gui
            tien_lai_dinh_ky = so_tien_gui * r_thang # Kỳ đầu tiên

    # --- HIỂN THỊ KẾT QUẢ ---
    st.subheader("📊 Kết Quả Tài Chính Của Bạn")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    
    with res_col1:
        st.metric(label="🌱 Tiền lãi định kỳ", value=f"{tien_lai_dinh_ky:,.0f} VNĐ")
    with res_col2:
        st.metric(label="🌿 Tổng tiền lãi nhận được", value=f"{tong_tien_lai:,.0f} VNĐ")
    with res_col3:
        st.metric(label="🌸 Tổng gốc + lãi", value=f"{tong_goc_va_lai:,.0f} VNĐ")

    # --- TÍNH NĂNG "QUA O": DỰ PHÓNG MỤC TIÊU & DU LỊCH/MUA SẮM ---
    st.markdown("---")
    st.subheader("🔮 Tính Năng 'Qua O': Bạn có thể mua gì với số tiền lãi này?")
    
    # Gợi ý quà tặng/mục tiêu dựa trên tổng tiền lãi
    muc_tieu_sugg = [
        ("🥤 Trà sữa thả ga", 50_000),
        ("💄 Một thỏi son môi xinh xắn", 500_000),
        ("👟 Một đôi giày thể thao mới", 2_000_000),
        ("✈️ Chuyến du lịch nội địa chill chill", 5_000_000),
        ("💻 Một chiếc Laptop mới toanh", 20_000_000),
        ("🛵 Một chiếc xe máy vi vu phố phường", 40_000_000),
    ]
    
    # Tìm món quà phù hợp nhất với tổng tiền lãi
    qua_tang_phu_hop = "Hành trang tự do tài chính to lớn!"
    for ten_item, gia_tri in muc_tieu_sugg:
        if tong_tien_lai >= gia_tri:
            so_luong = int(tong_tien_lai // gia_tri)
            qua_tang_phu_hop = f"Bạn có thể đổi lấy khoảng **{so_luong} lần** {ten_item}!"

    st.info(f"💡 **Gợi ý vui từ trạm tiết kiệm:** Tiền lãi từ khoản tiết kiệm này đủ để bạn: \n\n 👉 **{qua_tang_phu_hop}**")

    # Biểu đồ tăng trưởng tài sản theo tháng
    st.markdown("### 📈 Biểu đồ tăng trưởng số dư theo thời gian")
    thang_list = list(range(1, ky_han_thang + 1))
    if loai_lai == "Lãi kép":
        so_du_list = [so_tien_gui * ((1 + r_thang) ** m) for m in thang_list]
    else:
        so_du_list = [so_tien_gui + (so_tien_gui * r_thang * m) for m in thang_list]
        
    chart_data = pd.DataFrame({
        "Tháng": thang_list,
        "Tổng số dư (VNĐ)": so_du_list
    })
    
    st.line_chart(chart_data, x="Tháng", y="Tổng số dư (VNĐ)", color="#FF69B4")

# Chân trang dễ thương
st.markdown("---")
<center style="color: #D87093; font-size: 0.9em;">Made with 💖 for your brilliant financial future!</center>
