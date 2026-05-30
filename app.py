import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Pengolahan Citra Digital",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stRadio > div { flex-direction: row; } 
    </style>
""", unsafe_allow_html=True)

st.title("📸 Aplikasi Pengolahan Citra Digital: Pictura")
st.markdown("---")

st.sidebar.header("🛠️ Menu Operasi")
kategori = st.sidebar.selectbox(
    "Pilih Kategori Proses",
    ["🏠 Beranda", "🎯 Operasi Dasar", "✨ Operasi Lanjutan"]
)

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("📂 Unggah Gambar (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    st.sidebar.image(img_rgb, caption="📌 Referensi Gambar Asli", use_container_width=True)

    # ------------------ BERANDA ------------------
    if kategori == "🏠 Beranda":
        st.success("### Selamat Datang di Sistem Pengolahan Citra Kelompok Kami!")
        st.write("Aplikasi ini dirancang untuk mendemonstrasikan berbagai teknik manipulasi matriks citra digital. Silakan manfaatkan menu navigasi di panel sebelah kiri untuk mulai mengeksplorasi.")
        
        col_beranda1, col_beranda2, col_beranda3 = st.columns([1, 2, 1])
        with col_beranda2:
            st.image(img_rgb, caption="Gambar Utama yang Siap Diproses", use_container_width=True)

    # ------------------ Operasi Dasar ------------------
    elif kategori == "🎯 Operasi Dasar":
        st.subheader("🎯 Operasi Dasar")
        
        opsi_wajib = st.selectbox(
            "Pilih Jenis Operasi:",
            [
                "Tampilkan Gambar Asli", 
                "Konversi Grayscale", 
                "Citra Biner", 
                "Operasi Aritmatika",
                "Operasi Logika"
            ]
        )
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.image(img_rgb, caption="Source: Gambar Asli", use_container_width=True)

        with col2:
            if opsi_wajib == "Tampilkan Gambar Asli":
                st.image(img_rgb, caption="Result: Gambar Asli", use_container_width=True)

            #Grayscale
            elif opsi_wajib == "Konversi Grayscale":
                weights = np.array([0.299, 0.587, 0.114])
                img_custom_gray = np.dot(img_rgb[..., :3], weights).astype(np.uint8)
                st.image(img_custom_gray, caption="Result: Grayscale Image", use_container_width=True)   
                
                with st.expander("Penjelasan & Kode Python"):
                    st.info("Mengonversi citra RGB menjadi intensitas keabuan menggunakan perkalian matriks bobot standar NTSC.")
                    st.code("weights = np.array([0.299, 0.587, 0.114])\nimg_custom_gray = np.dot(img_rgb[..., :3], weights).astype(np.uint8)", language="python")

            #Citra Biner
            elif opsi_wajib == "Citra Biner":
                h, w = img_gray.shape
                img_bw = np.zeros((h, w), dtype=np.uint8) 
                
                for i in range(h):
                    for j in range(w):
                        if img_gray[i, j] > 127:
                            img_bw[i, j] = 255
                        else:
                            img_bw[i, j] = 0
                            
                st.image(img_bw, caption="Result: Citra Biner (Manual Loop)", use_container_width=True)
                
                with st.expander("Penjelasan & Kode Python"):
                    st.info("Proses binerisasi manual menggunakan perulangan bersarang. Ambang batas (threshold) ditetapkan pada nilai 127.")
                    st.code("h, w = img_gray.shape\nimg_bw = np.zeros((h, w), dtype=np.uint8)\nfor i in range(h):\n    for j in range(w):\n        if img_gray[i, j] > 127:\n            img_bw[i, j] = 255\n        else:\n            img_bw[i, j] = 0", language="python")

            #Operasi Aritmatika
            elif opsi_wajib == "Operasi Aritmatika":
                st.markdown("Panel Kontrol Aritmatika")
                brightness = st.slider("☀️ Atur Kecerahan (Penjumlahan Skalar)", min_value=-100, max_value=100, value=0, step=5)
                contrast = st.slider("🌓 Atur Kontras (Perkalian Skalar)", min_value=0.0, max_value=3.0, value=1.0, step=0.1)

                img_aritmatika = cv2.convertScaleAbs(img_rgb, alpha=contrast, beta=brightness)
                st.image(img_aritmatika, caption=f"Result: Kontras ({contrast}x) | Kecerahan ({brightness})", use_container_width=True)
                
                with st.expander("Penjelasan & Kode Python"):
                    st.info("Operasi aritmatika pada tingkat piksel (Linear Point Operation). Perkalian memengaruhi kontras, penjumlahan memengaruhi kecerahan.")
                    st.markdown(r"$$g(x,y) = \alpha \cdot f(x,y) + \beta$$")
                    st.code("img_aritmatika = cv2.convertScaleAbs(img_rgb, alpha=contrast, beta=brightness)", language="python")

            #Operasi Logika
            elif opsi_wajib == "Operasi Logika":
                _, img_bin_logika = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
                
                h, w = img_bin_logika.shape
                img_mask = np.zeros((h, w), dtype=np.uint8)
                img_mask[int(h/4):int(h*3/4), int(w/4):int(w*3/4)] = 255 
                
                jenis_logika = st.radio("Pilih Operator (Gerbang Logika):", ["NOT (Inversi)", "AND (Irisan / Masking)", "OR (Gabungan)", "XOR (Eksklusif)"], horizontal=True)
                
                c_log1, c_log2 = st.columns(2)
                with c_log1:
                    st.image(img_bin_logika, caption="Gambar A (Target)", use_container_width=True)
                with c_log2:
                    st.image(img_mask, caption="Gambar B (Mask)", use_container_width=True)
                
                st.markdown("---")
                
                if jenis_logika == "NOT (Inversi)":
                    img_result = cv2.bitwise_not(img_bin_logika)
                    st.image(img_result, caption="Result: NOT Gambar A", use_container_width=True)
                    with st.expander("Penjelasan & Kode Python"):
                        st.info("Membalik semua nilai bit piksel. Hitam (0) menjadi Putih (255), dan sebaliknya.")
                        st.code("img_result = cv2.bitwise_not(img_bin_logika)", language="python")
                    
                elif jenis_logika == "AND (Irisan / Masking)":
                    img_result = cv2.bitwise_and(img_bin_logika, img_mask)
                    st.image(img_result, caption="Result: A AND B", use_container_width=True)
                    with st.expander("Penjelasan & Kode Python"):
                        st.info("Piksel bernilai putih (1) HANYA JIKA area di Gambar A DAN Gambar B sama-sama berwarna putih.")
                        st.code("img_result = cv2.bitwise_and(img_bin_logika, img_mask)", language="python")
                    
                elif jenis_logika == "OR (Gabungan)":
                    img_result = cv2.bitwise_or(img_bin_logika, img_mask)
                    st.image(img_result, caption="Result: A OR B", use_container_width=True)
                    with st.expander("Penjelasan & Kode Python"):
                        st.info("Piksel bernilai putih JIKA area di Gambar A ATAU Gambar B (atau keduanya) berwarna putih.")
                        st.code("img_result = cv2.bitwise_or(img_bin_logika, img_mask)", language="python")
                        
                elif jenis_logika == "XOR (Eksklusif)":
                    img_result = cv2.bitwise_xor(img_bin_logika, img_mask)
                    st.image(img_result, caption="Result: A XOR B", use_container_width=True)
                    with st.expander("Penjelasan & Kode Python"):
                        st.info("Piksel bernilai putih JIKA warna piksel di Gambar A dan Gambar B BERBEDA status bit-nya.")
                        st.code("img_result = cv2.bitwise_xor(img_bin_logika, img_mask)", language="python")

    # ------------------ Operasi Lanjutan ------------------
    elif kategori == "✨ Operasi Lanjutan":
        st.subheader("✨ Operasi Lanjutan")
        
        opsi_opsional = st.selectbox(
            "Pilih Eksplorasi Lanjutan:",
            [
                "Tampilkan Gambar Asli",
                "Histogram",
                "Blurring (Mean Filter)",
                "Penajaman (Sharpening)",
                "Edge Detector",
                "Morfologi (Erosi & Dilasi)"
            ]
        )
        st.markdown("---")
 
        col1, col2 = st.columns(2) 
        with col1:
            if opsi_opsional == "Morfologi (Erosi & Dilasi)":
                _, img_bin_preview = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                st.image(img_bin_preview, caption="Source: Citra Biner (Input Morfologi)", use_container_width=True)
            else:
                st.image(img_rgb, caption="Source: Gambar Asli", use_container_width=True)

        with col2:
            if opsi_opsional == "Tampilkan Gambar Asli":
                st.image(img_rgb, caption="Result: Gambar Asli", use_container_width=True)

            # Histogram 
            elif opsi_opsional == "Histogram":
                hist_asli = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
                
                fig_asli, ax_asli = plt.subplots(figsize=(6, 4))
                ax_asli.plot(hist_asli, color='#1f77b4', linewidth=2)
                ax_asli.set_title("Distribusi Histogram Grayscale")
                ax_asli.set_xlabel("Nilai Intensitas (0-255)")
                ax_asli.set_ylabel("Frekuensi Piksel")
                ax_asli.grid(True, linestyle='--', alpha=0.6)
                
                st.pyplot(fig_asli)
                
                with st.expander("Penjelasan & Kode Python"):
                    st.info("Histogram memetakan sebaran populasi piksel berdasarkan tingkat kecerahannya.")
                    st.code("hist_asli = cv2.calcHist([img_gray], [0], None, [256], [0, 256])\nplt.plot(hist_asli)\nplt.show()", language="python")

            #Mean Filter 
            elif opsi_opsional == "Blurring (Mean Filter)":
                kernel_dasar = np.array([
                    [1, 1, 1],
                    [1, 1, 1],
                    [1, 1, 1]
                ], dtype=np.float32)
                
                kernel_blur = kernel_dasar / 9.0
                img_blur = cv2.filter2D(src=img_rgb, ddepth=-1, kernel=kernel_blur)
                
                st.image(img_blur, caption="Result: Spatial Blurring (3x3)", use_container_width=True)
                
                with st.expander("Penjelasan & Kode Python"):
                    st.info("Filter low-pass yang menghaluskan gambar dengan membagi total nilai matriks 3x3 dengan luas kernelnya (9).")
                    st.code("kernel_dasar = np.array([\n    [1, 1, 1],\n    [1, 1, 1],\n    [1, 1, 1]\n], dtype=np.float32)\n\nkernel_blur = kernel_dasar / 9.0\nimg_blur = cv2.filter2D(src=img_rgb, ddepth=-1, kernel=kernel_blur)", language="python")

            #Sharpening 
            elif opsi_opsional == "Penajaman (Sharpening)":
                jenis_sharp = st.radio("Intensitas Penajaman:", ["Standar", "Extream"], horizontal=True)
                
                if jenis_sharp == "Standar":
                    kernel_sharp = np.array([
                        [0, -1, 0], 
                        [-1, 5, -1], 
                        [0, -1, 0]])
                else:
                    kernel_sharp = np.array([
                        [-1, -1, -1], 
                        [-1, 9, -1], 
                        [-1, -1, -1]])

                img_sharp = cv2.filter2D(src=img_rgb, ddepth=-1, kernel=kernel_sharp)
                st.image(img_sharp, caption=f"Result: Sharpened ({jenis_sharp})", use_container_width=True)
                
                with st.expander("Penjelasan & Kode Python"):
                    st.info("Filter high-pass yang mengekstraksi dan memperkuat detail tepi dengan mengurangkan piksel tetangga dari piksel pusat.")
                    st.code(f"kernel_sharp = np.array([\n   [0, -1, 0],\n   [-1, 5, -1], \n   [0, -1, 0]])\nelse:\n    kernel_sharp = np.array([\n        [-1, -1, -1], \n        [-1, 9, -1], \n        [-1, -1, -1]])\n\nimg_sharp = cv2.filter2D(src=img_rgb, ddepth=-1, kernel=kernel_sharp)", language="python")

            #Edge Filter 
            elif opsi_opsional == "Edge Detector":
                jenis_edge = st.selectbox("Jenis Matriks Deteksi:", [
                    "Sobel (Horizontal)", 
                    "Sobel (Vertikal)",
                    "Prewitt (Horizontal)",
                    "Prewitt (Vertikal)"
                ])
                
                if "Sobel" in jenis_edge and "X" in jenis_edge:
                    kernel_edge = np.array([
                        [-1, 0, 1], 
                        [-2, 0, 2], 
                        [-1, 0, 1]])
                elif "Sobel" in jenis_edge and "Y" in jenis_edge:
                    kernel_edge = np.array([
                        [-1, -2, -1], 
                        [0, 0, 0], 
                        [1, 2, 1]])
                elif "Prewitt" in jenis_edge and "X" in jenis_edge:
                    kernel_edge = np.array([
                        [-1, 0, 1], 
                        [-1, 0, 1], 
                        [-1, 0, 1]])
                else:
                    kernel_edge = np.array([
                        [-1, -1, -1], 
                        [0, 0, 0], 
                        [1, 1, 1]])

                img_edge = cv2.filter2D(src=img_gray, ddepth=-1, kernel=kernel_edge)
                st.image(img_edge, caption=f"Result: {jenis_edge}", use_container_width=True)
                
                with st.expander("Penjelasan & Kode Python"):
                    st.info("Kernel berbobot asimetris untuk mendeteksi lompatan gradien intensitas secara spasial.")
                    kode_edge = """if "Sobel" in jenis_edge and "X" in jenis_edge:
    kernel_edge = np.array([
        [-1, 0, 1], 
        [-2, 0, 2], 
        [-1, 0, 1]])
elif "Sobel" in jenis_edge and "Y" in jenis_edge:
    kernel_edge = np.array([
        [-1, -2, -1], 
        [0, 0, 0], 
        [1, 2, 1]])
elif "Prewitt" in jenis_edge and "X" in jenis_edge:
    kernel_edge = np.array([
        [-1, 0, 1], 
        [-1, 0, 1], 
        [-1, 0, 1]])
else:
    kernel_edge = np.array([
        [-1, -1, -1], 
        [0, 0, 0], 
        [1, 1, 1]])

img_edge = cv2.filter2D(src=img_gray, ddepth=-1, kernel=kernel_edge)"""
                    
                    st.code(kode_edge, language="python")

            #Morfologi 
            elif opsi_opsional == "Morfologi (Erosi & Dilasi)":
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    opsi_morfologi = st.radio("Operasi:", ["Erosi (Pengikisan)", "Dilasi (Penebalan)"])
                with col_m2:
                    opsi_se = st.radio("Structuring Element:", ["SE Cross (+)", "SE Diagonal (x)"])
                
                if "Cross" in opsi_se:
                    kernel_se = np.array([
                        [0, 1, 0], 
                        [1, 1, 1], 
                        [0, 1, 0]
                    ], dtype=np.uint8)
                else:
                    kernel_se = np.array([
                        [1, 0, 1], 
                        [0, 1, 0], 
                        [1, 0, 1]
                    ], dtype=np.uint8)

                _, img_bin = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                if "Erosi" in opsi_morfologi:
                    img_morph = cv2.erode(img_bin, kernel_se, iterations=1)
                    fungsi_cv2 = "erode"
                else:
                    img_morph = cv2.dilate(img_bin, kernel_se, iterations=1)
                    fungsi_cv2 = "dilate"
                    
                st.image(img_morph, caption=f"Result: {opsi_morfologi} [{opsi_se}]", use_container_width=True)
                
                with st.expander("Penjelasan & Kode Python"):
                    st.info("Memodifikasi struktur geometri objek biner menggunakan matriks probe (Structuring Element).")
                    
                    kode_morfologi = f"""if "Cross" in opsi_se:
    kernel_se = np.array([
        [0, 1, 0], 
        [1, 1, 1], 
        [0, 1, 0]
    ], dtype=np.uint8)
else:
    kernel_se = np.array([
        [1, 0, 1], 
        [0, 1, 0], 
        [1, 0, 1]
    ], dtype=np.uint8)

img_morph = cv2.{fungsi_cv2}(img_bin, kernel_se, iterations=1)"""
                    
                    st.code(kode_morfologi, language="python")

else:
    st.info("👋 Halo! Silakan unggah berkas gambar terlebih dahulu lewat panel di sebelah kiri untuk mulai menjalankan sistem.")