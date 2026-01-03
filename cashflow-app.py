import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="Cashflow Tracker Pro", 
    page_icon="💰", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg, [data-testid="stSidebar"] .st-emotion-cache-1cypcdb {
        color: white;
    }
    
    /* Card styling */
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Button styling with gradient */
    .stButton>button {
        border-radius: 15px;
        font-weight: bold;
        border: none;
        padding: 15px 24px;
        transition: all 0.3s;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        font-size: 24px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(79, 172, 254, 0.4);
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Form container */
    .stForm {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f0f2f6;
        border-radius: 10px;
        font-weight: bold;
    }
    
    /* Title styling */
    h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        padding: 20px 0;
    }
    
    h2, h3 {
        color: white;
    }
    
    /* Data display */
    .data-row {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s;
    }
    
    .data-row:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
    }
    
    /* Download button special styling */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize CSV files
PEMASUKAN_FILE = 'pemasukan.csv'
PENGELUARAN_FILE = 'pengeluaran.csv'
INVESTASI_FILE = 'investasi.csv'

# Kategori default
KATEGORI_PEMASUKAN = ['Gaji Pokok', 'Tunjangan Kinerja', 'Uang Perjalanan Dinas', 'Bonus', 'Lain-lain']
KATEGORI_PENGELUARAN = ['Listrik', 'Makan', 'Minum', 'Transportasi', 'Pulsa', 'Kuota Internet', 'Persembahan', 'Kasih Ortu', 'Belanja', 'Hiburan', 'Lain-lain']
KATEGORI_INVESTASI = ['Reksadana', 'BBRI', 'BBCA', 'BBNI', 'BMRI', 'Gold', 'APPL', 'GOOG', 'MSFT', 'TSLA']

# Initialize session state for custom categories
if 'custom_pemasukan' not in st.session_state:
    st.session_state.custom_pemasukan = []
if 'custom_pengeluaran' not in st.session_state:
    st.session_state.custom_pengeluaran = []
if 'custom_investasi' not in st.session_state:
    st.session_state.custom_investasi = []

# Functions to handle CSV
def init_csv(filename, columns):
    """Initialize CSV file if it doesn't exist"""
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)

def load_data(filename):
    """Load data from CSV file"""
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        if not df.empty:
            return df
    return pd.DataFrame()

def save_data(filename, data):
    """Save data to CSV file"""
    df = pd.DataFrame([data])
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

def delete_row(filename, index):
    """Delete a row from CSV file"""
    df = load_data(filename)
    if not df.empty:
        df = df.drop(index)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(filename, index=False)

# Initialize CSV files
init_csv(PEMASUKAN_FILE, ['Tanggal', 'Kategori', 'Jumlah', 'Keterangan'])
init_csv(PENGELUARAN_FILE, ['Tanggal', 'Kategori', 'Jumlah', 'Keterangan'])
init_csv(INVESTASI_FILE, ['Tanggal', 'Kategori', 'Jumlah', 'Keterangan'])

# Helper function to format currency
def format_currency(amount):
    """Format number to Indonesian Rupiah"""
    return f"Rp {amount:,.0f}".replace(",", ".")

# Sidebar navigation with icons
st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: white; font-size: 2.5em;'>💰</h1>
        <h2 style='color: white; margin: 0;'>Cashflow Tracker</h2>
        <p style='color: #b8c6db; margin-top: 5px;'>Kelola Keuangan Lebih Mudah</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Initialize session state for menu
if 'menu' not in st.session_state:
    st.session_state.menu = "📊 Dashboard"

# Custom styled navigation buttons
st.sidebar.markdown("<h3 style='color: white; text-align: center; margin-bottom: 20px;'>📍 NAVIGASI</h3>", unsafe_allow_html=True)

# Dashboard button
if st.sidebar.button("📊", key="nav_dashboard", use_container_width=True):
    st.session_state.menu = "📊 Dashboard"
st.sidebar.markdown("""
<div style='margin-top: -10px; margin-bottom: 15px;'>
    <p style='color: {}; text-align: center; font-size: 14px; font-weight: bold;'>Dashboard</p>
</div>
""".format('#4facfe' if st.session_state.menu == "📊 Dashboard" else '#b8c6db'), unsafe_allow_html=True)

# Pemasukan button
if st.sidebar.button("📈", key="nav_pemasukan", use_container_width=True):
    st.session_state.menu = "📈 Pemasukan"
st.sidebar.markdown("""
<div style='margin-top: -10px; margin-bottom: 15px;'>
    <p style='color: {}; text-align: center; font-size: 14px; font-weight: bold;'>Pemasukan</p>
</div>
""".format('#4facfe' if st.session_state.menu == "📈 Pemasukan" else '#b8c6db'), unsafe_allow_html=True)

# Pengeluaran button
if st.sidebar.button("📉", key="nav_pengeluaran", use_container_width=True):
    st.session_state.menu = "📉 Pengeluaran"
st.sidebar.markdown("""
<div style='margin-top: -10px; margin-bottom: 15px;'>
    <p style='color: {}; text-align: center; font-size: 14px; font-weight: bold;'>Pengeluaran</p>
</div>
""".format('#4facfe' if st.session_state.menu == "📉 Pengeluaran" else '#b8c6db'), unsafe_allow_html=True)

# Investasi button
if st.sidebar.button("💎", key="nav_investasi", use_container_width=True):
    st.session_state.menu = "💎 Investasi"
st.sidebar.markdown("""
<div style='margin-top: -10px; margin-bottom: 15px;'>
    <p style='color: {}; text-align: center; font-size: 14px; font-weight: bold;'>Investasi</p>
</div>
""".format('#4facfe' if st.session_state.menu == "💎 Investasi" else '#b8c6db'), unsafe_allow_html=True)

menu = st.session_state.menu

# PEMASUKAN PAGE
if menu == "📈 Pemasukan":
    col_title1, col_title2 = st.columns([3, 1])
    with col_title1:
        st.title("📈 Catat Pemasukan")
        st.markdown("*Transparansi keuangan dimulai dari pencatatan yang baik*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("form_pemasukan", clear_on_submit=True):
        st.markdown("### 📝 Form Input Pemasukan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tanggal = st.date_input("📅 Tanggal", datetime.now())
            kategori_list = KATEGORI_PEMASUKAN + st.session_state.custom_pemasukan
            kategori = st.selectbox("🏷️ Kategori", kategori_list)
            
        with col2:
            jumlah = st.number_input("💵 Jumlah (Rp)", min_value=0, step=10000, format="%d")
            keterangan = st.text_area("📋 Keterangan (Opsional)", height=100)
        
        col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
        with col_btn1:
            submitted = st.form_submit_button("💾 Simpan Pemasukan", use_container_width=True, type="primary")
        
        if submitted:
            if jumlah > 0:
                data = {
                    'Tanggal': tanggal.strftime('%Y-%m-%d'),
                    'Kategori': kategori,
                    'Jumlah': jumlah,
                    'Keterangan': keterangan
                }
                save_data(PEMASUKAN_FILE, data)
                st.success("✅ Pemasukan berhasil disimpan!")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Jumlah harus lebih dari 0!")
    
    # Add custom category
    with st.expander("➕ Tambah Kategori Pemasukan Baru"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_kategori = st.text_input("Nama Kategori Baru", key="new_pemasukan", placeholder="Contoh: Freelance, Bonus, dll")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Tambah", key="btn_add_pemasukan", use_container_width=True):
                kategori_list = KATEGORI_PEMASUKAN + st.session_state.custom_pemasukan
                if new_kategori and new_kategori.strip() != "":
                    if new_kategori not in kategori_list:
                        st.session_state.custom_pemasukan.append(new_kategori)
                        st.success(f"✅ Kategori '{new_kategori}' berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Kategori sudah ada!")
                else:
                    st.error("⚠️ Nama kategori tidak boleh kosong!")
    
    st.markdown("---")
    
    # Display data with better styling
    df_pemasukan = load_data(PEMASUKAN_FILE)
    if not df_pemasukan.empty:
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown("### 📋 Riwayat Pemasukan")
        with col_h2:
            total = df_pemasukan['Jumlah'].sum()
            st.metric("Total", format_currency(total))
        
        df_pemasukan['Tanggal'] = pd.to_datetime(df_pemasukan['Tanggal'])
        df_pemasukan = df_pemasukan.sort_values('Tanggal', ascending=False)
        
        for idx, row in df_pemasukan.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
                col1.markdown(f"**📅** {row['Tanggal'].strftime('%d/%m/%Y')}")
                col2.markdown(f"**🏷️** {row['Kategori']}")
                col3.markdown(f"**💰** {format_currency(row['Jumlah'])}")
                col4.markdown(f"**📝** {row['Keterangan'] if pd.notna(row['Keterangan']) and row['Keterangan'] != '' else '-'}")
                if col5.button("🗑️", key=f"del_pemasukan_{idx}"):
                    delete_row(PEMASUKAN_FILE, idx)
                    st.success("✅ Data berhasil dihapus!")
                    st.rerun()
                st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)
    else:
        st.info("📝 Belum ada data pemasukan. Yuk mulai catat pemasukan pertamamu!")

# PENGELUARAN PAGE
elif menu == "📉 Pengeluaran":
    col_title1, col_title2 = st.columns([3, 1])
    with col_title1:
        st.title("📉 Catat Pengeluaran")
        st.markdown("*Pantau setiap rupiah yang keluar dari kantong*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("form_pengeluaran", clear_on_submit=True):
        st.markdown("### 📝 Form Input Pengeluaran")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tanggal = st.date_input("📅 Tanggal", datetime.now())
            kategori_list = KATEGORI_PENGELUARAN + st.session_state.custom_pengeluaran
            kategori = st.selectbox("🏷️ Kategori", kategori_list)
            
        with col2:
            jumlah = st.number_input("💵 Jumlah (Rp)", min_value=0, step=5000, format="%d")
            keterangan = st.text_area("📋 Keterangan (Opsional)", height=100)
        
        col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
        with col_btn1:
            submitted = st.form_submit_button("💾 Simpan Pengeluaran", use_container_width=True, type="primary")
        
        if submitted:
            if jumlah > 0:
                data = {
                    'Tanggal': tanggal.strftime('%Y-%m-%d'),
                    'Kategori': kategori,
                    'Jumlah': jumlah,
                    'Keterangan': keterangan
                }
                save_data(PENGELUARAN_FILE, data)
                st.success("✅ Pengeluaran berhasil disimpan!")
                st.rerun()
            else:
                st.error("⚠️ Jumlah harus lebih dari 0!")
    
    # Add custom category
    with st.expander("➕ Tambah Kategori Pengeluaran Baru"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_kategori = st.text_input("Nama Kategori Baru", key="new_pengeluaran", placeholder="Contoh: Gym, Skincare, dll")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Tambah", key="btn_add_pengeluaran", use_container_width=True):
                kategori_list = KATEGORI_PENGELUARAN + st.session_state.custom_pengeluaran
                if new_kategori and new_kategori.strip() != "":
                    if new_kategori not in kategori_list:
                        st.session_state.custom_pengeluaran.append(new_kategori)
                        st.success(f"✅ Kategori '{new_kategori}' berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Kategori sudah ada!")
                else:
                    st.error("⚠️ Nama kategori tidak boleh kosong!")
    
    st.markdown("---")
    
    # Display data
    df_pengeluaran = load_data(PENGELUARAN_FILE)
    if not df_pengeluaran.empty:
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown("### 📋 Riwayat Pengeluaran")
        with col_h2:
            total = df_pengeluaran['Jumlah'].sum()
            st.metric("Total", format_currency(total))
        
        df_pengeluaran['Tanggal'] = pd.to_datetime(df_pengeluaran['Tanggal'])
        df_pengeluaran = df_pengeluaran.sort_values('Tanggal', ascending=False)
        
        for idx, row in df_pengeluaran.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
                col1.markdown(f"**📅** {row['Tanggal'].strftime('%d/%m/%Y')}")
                col2.markdown(f"**🏷️** {row['Kategori']}")
                col3.markdown(f"**💸** {format_currency(row['Jumlah'])}")
                col4.markdown(f"**📝** {row['Keterangan'] if pd.notna(row['Keterangan']) and row['Keterangan'] != '' else '-'}")
                if col5.button("🗑️", key=f"del_pengeluaran_{idx}"):
                    delete_row(PENGELUARAN_FILE, idx)
                    st.success("✅ Data berhasil dihapus!")
                    st.rerun()
                st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)
    else:
        st.info("📝 Belum ada data pengeluaran. Mulai tracking pengeluaranmu!")

# INVESTASI PAGE
elif menu == "💎 Investasi":
    col_title1, col_title2 = st.columns([3, 1])
    with col_title1:
        st.title("💎 Catat Investasi")
        st.markdown("*Investasi adalah kunci kebebasan finansial*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("form_investasi", clear_on_submit=True):
        st.markdown("### 📝 Form Input Investasi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tanggal = st.date_input("📅 Tanggal", datetime.now())
            kategori_list = KATEGORI_INVESTASI + st.session_state.custom_investasi
            kategori = st.selectbox("🏷️ Instrumen Investasi", kategori_list)
            
        with col2:
            jumlah = st.number_input("💵 Jumlah (Rp)", min_value=0, step=50000, format="%d")
            keterangan = st.text_area("📋 Keterangan (Opsional)", height=100, placeholder="Contoh: Beli 10 lot, DCA bulan ini")
        
        col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 1])
        with col_btn1:
            submitted = st.form_submit_button("💾 Simpan Investasi", use_container_width=True, type="primary")
        
        if submitted:
            if jumlah > 0:
                data = {
                    'Tanggal': tanggal.strftime('%Y-%m-%d'),
                    'Kategori': kategori,
                    'Jumlah': jumlah,
                    'Keterangan': keterangan
                }
                save_data(INVESTASI_FILE, data)
                st.success("✅ Investasi berhasil disimpan!")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Jumlah harus lebih dari 0!")
    
    # Add custom category
    with st.expander("➕ Tambah Instrumen Investasi Baru"):
        col1, col2 = st.columns([3, 1])
        with col1:
            new_kategori = st.text_input("Nama Instrumen Baru", key="new_investasi", placeholder="Contoh: TLKM, UNVR, Bitcoin, ETF")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Tambah", key="btn_add_investasi", use_container_width=True):
                kategori_list = KATEGORI_INVESTASI + st.session_state.custom_investasi
                if new_kategori and new_kategori.strip() != "":
                    if new_kategori not in kategori_list:
                        st.session_state.custom_investasi.append(new_kategori)
                        st.success(f"✅ Instrumen '{new_kategori}' berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Instrumen sudah ada!")
                else:
                    st.error("⚠️ Nama instrumen tidak boleh kosong!")
    
    st.markdown("---")
    
    # Display data
    df_investasi = load_data(INVESTASI_FILE)
    if not df_investasi.empty:
        col_h1, col_h2 = st.columns([3, 1])
        with col_h1:
            st.markdown("### 📋 Riwayat Investasi")
        with col_h2:
            total = df_investasi['Jumlah'].sum()
            st.metric("Total", format_currency(total))
        
        df_investasi['Tanggal'] = pd.to_datetime(df_investasi['Tanggal'])
        df_investasi = df_investasi.sort_values('Tanggal', ascending=False)
        
        for idx, row in df_investasi.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
                col1.markdown(f"**📅** {row['Tanggal'].strftime('%d/%m/%Y')}")
                col2.markdown(f"**🏷️** {row['Kategori']}")
                col3.markdown(f"**📈** {format_currency(row['Jumlah'])}")
                col4.markdown(f"**📝** {row['Keterangan'] if pd.notna(row['Keterangan']) and row['Keterangan'] != '' else '-'}")
                if col5.button("🗑️", key=f"del_investasi_{idx}"):
                    delete_row(INVESTASI_FILE, idx)
                    st.success("✅ Data berhasil dihapus!")
                    st.rerun()
                st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)
    else:
        st.info("📝 Belum ada data investasi. Mulai investasi untuk masa depan!")

# DASHBOARD PAGE
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard Keuangan")
    st.markdown("*Visualisasi lengkap kondisi keuangan Anda*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Load all data
    df_pemasukan = load_data(PEMASUKAN_FILE)
    df_pengeluaran = load_data(PENGELUARAN_FILE)
    df_investasi = load_data(INVESTASI_FILE)
    
    # Convert date columns
    if not df_pemasukan.empty:
        df_pemasukan['Tanggal'] = pd.to_datetime(df_pemasukan['Tanggal'])
    if not df_pengeluaran.empty:
        df_pengeluaran['Tanggal'] = pd.to_datetime(df_pengeluaran['Tanggal'])
    if not df_investasi.empty:
        df_investasi['Tanggal'] = pd.to_datetime(df_investasi['Tanggal'])
    
    # Get available months
    all_dates = []
    if not df_pemasukan.empty:
        all_dates.extend(df_pemasukan['Tanggal'].tolist())
    if not df_pengeluaran.empty:
        all_dates.extend(df_pengeluaran['Tanggal'].tolist())
    if not df_investasi.empty:
        all_dates.extend(df_investasi['Tanggal'].tolist())
    
    if all_dates:
        all_dates = pd.to_datetime(all_dates)
        unique_months = sorted(all_dates.dt.strftime('%Y-%m').unique(), reverse=True)
        
        # Month filter with better styling
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            selected_month = st.selectbox("🗓️ Filter Bulan", options=unique_months, index=0)
    else:
        st.warning("⚠️ Belum ada data. Silakan tambahkan transaksi terlebih dahulu!")
        st.stop()
    
    # Filter data by month
    df_pemasukan_filtered = df_pemasukan[df_pemasukan['Tanggal'].dt.strftime('%Y-%m') == selected_month] if not df_pemasukan.empty else pd.DataFrame()
    df_pengeluaran_filtered = df_pengeluaran[df_pengeluaran['Tanggal'].dt.strftime('%Y-%m') == selected_month] if not df_pengeluaran.empty else pd.DataFrame()
    df_investasi_filtered = df_investasi[df_investasi['Tanggal'].dt.strftime('%Y-%m') == selected_month] if not df_investasi.empty else pd.DataFrame()
    
    # Calculate totals
    total_pemasukan = df_pemasukan_filtered['Jumlah'].sum() if not df_pemasukan_filtered.empty else 0
    total_pengeluaran = df_pengeluaran_filtered['Jumlah'].sum() if not df_pengeluaran_filtered.empty else 0
    total_investasi = df_investasi_filtered['Jumlah'].sum() if not df_investasi_filtered.empty else 0
    saldo = total_pemasukan - total_pengeluaran - total_investasi
    
    # Summary cards with gradient
    st.markdown("### 💼 Ringkasan Keuangan")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
            <h4 style='margin: 0; font-size: 14px; opacity: 0.9;'>💰 Total Pemasukan</h4>
            <h2 style='margin: 10px 0 0 0; font-size: 20px;'>{}</h2>
        </div>
        """.format(format_currency(total_pemasukan)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 25px; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
            <h4 style='margin: 0; font-size: 14px; opacity: 0.9;'>💸 Total Pengeluaran</h4>
            <h2 style='margin: 10px 0 0 0; font-size: 20px;'>{}</h2>
        </div>
        """.format(format_currency(total_pengeluaran)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 25px; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
            <h4 style='margin: 0; font-size: 14px; opacity: 0.9;'>📈 Total Investasi</h4>
            <h2 style='margin: 10px 0 0 0; font-size: 20px;'>{}</h2>
        </div>
        """.format(format_currency(total_investasi)), unsafe_allow_html=True)
    
    with col4:
        saldo_color = "#43e97b" if saldo >= 0 else "#fa709a"
        st.markdown("""
        <div style='background: linear-gradient(135deg, {} 0%, {} 100%); 
                    padding: 25px; border-radius: 15px; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
            <h4 style='margin: 0; font-size: 14px; opacity: 0.9;'>💵 Saldo Akhir</h4>
            <h2 style='margin: 10px 0 0 0; font-size: 20px;'>{}</h2>
        </div>
        """.format(saldo_color, saldo_color, format_currency(saldo)), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Pie charts section
    st.markdown("### 📊 Distribusi per Kategori")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 💰 Pemasukan")
        if not df_pemasukan_filtered.empty:
            pemasukan_by_kategori = df_pemasukan_filtered.groupby('Kategori')['Jumlah'].sum().reset_index()
            fig_pemasukan = px.pie(
                pemasukan_by_kategori, 
                values='Jumlah', 
                names='Kategori',
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig_pemasukan.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Jumlah: Rp %{value:,.0f}<br>Persentase: %{percent}<extra></extra>'
            )
            fig_pemasukan.update_layout(
                height=350, 
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12)
            )
            st.plotly_chart(fig_pemasukan, use_container_width=True)
        else:
            st.info("Tidak ada data")
    
    with col2:
        st.markdown("#### 💸 Pengeluaran")
        if not df_pengeluaran_filtered.empty:
            pengeluaran_by_kategori = df_pengeluaran_filtered.groupby('Kategori')['Jumlah'].sum().reset_index()
            fig_pengeluaran = px.pie(
                pengeluaran_by_kategori, 
                values='Jumlah', 
                names='Kategori',
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            fig_pengeluaran.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Jumlah: Rp %{value:,.0f}<br>Persentase: %{percent}<extra></extra>'
            )
            fig_pengeluaran.update_layout(
                height=350, 
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12)
            )
            st.plotly_chart(fig_pengeluaran, use_container_width=True)
        else:
            st.info("Tidak ada data")
    
    with col3:
        st.markdown("#### 📈 Investasi")
        if not df_investasi_filtered.empty:
            investasi_by_kategori = df_investasi_filtered.groupby('Kategori')['Jumlah'].sum().reset_index()
            fig_investasi = px.pie(
                investasi_by_kategori, 
                values='Jumlah', 
                names='Kategori',
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig_investasi.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Jumlah: Rp %{value:,.0f}<br>Persentase: %{percent}<extra></extra>'
            )
            fig_investasi.update_layout(
                height=350, 
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12)
            )
            st.plotly_chart(fig_investasi, use_container_width=True)
        else:
            st.info("Tidak ada data")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Line chart for daily expenses
    st.markdown("### 📈 Tren Pengeluaran Harian")
    if not df_pengeluaran_filtered.empty:
        daily_expenses = df_pengeluaran_filtered.groupby('Tanggal')['Jumlah'].sum().reset_index()
        daily_expenses = daily_expenses.sort_values('Tanggal')
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=daily_expenses['Tanggal'],
            y=daily_expenses['Jumlah'],
            mode='lines+markers',
            name='Pengeluaran',
            line=dict(color='#FF6B6B', width=4),
            marker=dict(size=10, color='#FF6B6B', line=dict(color='white', width=2)),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.3)',
            hovertemplate='<b>Tanggal:</b> %{x|%d/%m/%Y}<br><b>Pengeluaran:</b> Rp %{y:,.0f}<extra></extra>'
        ))
        
        fig_line.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.1)',
            font=dict(color='white', size=12),
            xaxis=dict(
                title="Tanggal",
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                title="Jumlah (Rp)",
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)'
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: white; margin: 0;'>📊 Rata-rata Harian</h4>
                <h3 style='color: #4facfe; margin: 10px 0 0 0;'>{}</h3>
            </div>
            """.format(format_currency(daily_expenses['Jumlah'].mean())), unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: white; margin: 0;'>📈 Tertinggi</h4>
                <h3 style='color: #f5576c; margin: 10px 0 0 0;'>{}</h3>
            </div>
            """.format(format_currency(daily_expenses['Jumlah'].max())), unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; text-align: center;'>
                <h4 style='color: white; margin: 0;'>📉 Terendah</h4>
                <h3 style='color: #43e97b; margin: 10px 0 0 0;'>{}</h3>
            </div>
            """.format(format_currency(daily_expenses['Jumlah'].min())), unsafe_allow_html=True)
    else:
        st.info("📝 Tidak ada data pengeluaran harian untuk bulan ini")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export section
    st.markdown("### 📥 Ekspor Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not df_pemasukan.empty:
            csv_pemasukan = df_pemasukan.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Pemasukan CSV",
                data=csv_pemasukan,
                file_name=f'pemasukan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )
    
    with col2:
        if not df_pengeluaran.empty:
            csv_pengeluaran = df_pengeluaran.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Pengeluaran CSV",
                data=csv_pengeluaran,
                file_name=f'pengeluaran_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )
    
    with col3:
        if not df_investasi.empty:
            csv_investasi = df_investasi.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Investasi CSV",
                data=csv_investasi,
                file_name=f'investasi_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )
    
    with col4:
        if not df_pemasukan.empty or not df_pengeluaran.empty or not df_investasi.empty:
            all_data = []
            
            if not df_pemasukan.empty:
                df_p = df_pemasukan.copy()
                df_p['Tipe'] = 'Pemasukan'
                all_data.append(df_p)
            
            if not df_pengeluaran.empty:
                df_e = df_pengeluaran.copy()
                df_e['Tipe'] = 'Pengeluaran'
                all_data.append(df_e)
            
            if not df_investasi.empty:
                df_i = df_investasi.copy()
                df_i['Tipe'] = 'Investasi'
                all_data.append(df_i)
            
            df_all = pd.concat(all_data, ignore_index=True)
            df_all = df_all.sort_values('Tanggal', ascending=False)
            
            csv_all = df_all.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Semua Data CSV",
                data=csv_all,
                file_name=f'cashflow_lengkap_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 10px;'>
    <h4 style='color: white; margin: 0;'>📊 Cashflow Tracker Pro</h4>
    <p style='color: #b8c6db; font-size: 12px; margin: 10px 0 0 0;'>Version 2.0</p>
    <p style='color: #b8c6db; font-size: 11px; margin: 5px 0 0 0;'>Kelola keuangan dengan bijak</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border-left: 4px solid #4facfe;'>
    <p style='color: white; font-size: 12px; margin: 0;'>
        💡 <b>Tips Finansial:</b><br>
        Alokasikan 50% kebutuhan,<br>
        30% keinginan, 20% investasi
    </p>
</div>
""", unsafe_allow_html=True)