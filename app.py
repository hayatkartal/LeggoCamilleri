import streamlit as st
import re

st.set_page_config(page_title="Leggo Camilleri", layout="wide")

def metni_yukle():
    try:
        with open("kitap.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def bolumlere_ayir(metin):
    if not metin: return {}
    sayi_basliklari = ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto", "Nove", "Dieci"]
    satirlar = metin.split('\n')
    bolumler = {}
    su_anki_bolum = "Giriş"
    gecici_metin = []

    for satir in satirlar:
        temiz_satir = satir.strip().capitalize()
        if temiz_satir in sayi_basliklari:
            if gecici_metin:
                bolumler[su_anki_bolum] = "\n".join(gecici_metin).strip()
            su_anki_bolum = temiz_satir
            gecici_metin = []
        else:
            gecici_metin.append(satir)
    if gecici_metin:
        bolumler[su_anki_bolum] = "\n".join(gecici_metin).strip()
    return bolumler

def aralikli_karakter_analizi(bolum_sozlugu):
    # BAK BURASI İÇERİDEN BAŞLIYOR (TAB)
    analiz_araligi = ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto", "Nove", "Dieci"]
    taranacak_metin = ""
    for b in analiz_araligi:
        if b in bolum_sozlugu:
            taranacak_metin += bolum_sozlugu[b] + " "

    if not taranacak_metin: return []

    cumleler = re.split(r'[.!?]', taranacak_metin)
    ham_isimler = []
    
    # Yasaklı listesi (Gereksiz isimleri eledik)
    yasakli = ["Vigata", "Montelusa", "Sicilia", "Italia", "Commissariato", "Questura", "Marinella", "Mentre", "Ancora", "Invece", "Allora", "Quando", "Dopo", "Tuttavia", "Sempre", "Cosi", "Dunque", "Eppure", "Dottore", "Commissario", "Era", "Disse", "Ando", "Aveva"]
    gramer = ["Il", "Lo", "La", "I", "Gli", "Le", "Un", "Una", "Uno", "Ma", "Non", "Che", "Chi", "Per", "Veda", "Vedi", "Guarda"]

    for cumle in cumleler:
        kelimeler = cumle.strip().split()
        if len(kelimeler) > 1:
            for k in kelimeler[1:]: # Cümle başı fiilleri ele
                temiz = re.sub(r'[^\w]', '', k)
                if temiz and temiz[0].isupper() and len(temiz) > 2:
                    if temiz not in yasakli and temiz not in gramer:
                        ham_isimler.append(temiz)

    # En az 1 kez geçen ama filtrelerden kurtulanları al
    return sorted(list(set(ham_isimler)))

# --- ARAYÜZ (BURASI DA EN SOLDA OLMALI) ---
st.title("🔍 Leggo Camilleri: Uno - Dieci Analizi")

ham_metin = metni_yukle()
bolumler = bolumlere_ayir(ham_metin)

mod = st.sidebar.radio("Menü", ["Okuma Paneli", "Karakter Analizi (Uno-Dieci)"])

if mod == "Okuma Paneli":
    liste = list(bolumler.keys())
    if liste:
        secilen = st.selectbox("Bölüm Seç:", liste)
        st.write(bolumler[secilen])

elif mod == "Karakter Analizi (Uno-Dieci)":
    st.header("👥 Uno'dan Dieci'ye Karakter Tespiti")
    isimler = aralikli_karakter_analizi(bolumler)
    
    if isimler:
        karakter = st.selectbox("Gerçek Karakterler:", isimler)
        taranacak_alan = " ".join([bolumler[b] for b in bolumler if b in ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto", "Nove", "Dieci"]])
        
        bulunan = [c.strip() + "." for c in taranacak_alan.split('.') if karakter in c]
        if bulunan:
            st.success(f"**{karakter}** metinde şöyle geçiyor:")
            st.write(bulunan[0])
    else:
        st.warning("Bu aralıkta özel isim bulunamadı.")
        import streamlit as st
import re

# Sayfa Yapılandırması
st.set_page_config(page_title="Leggo Camilleri - DTCF", layout="wide")

# --- 1. VERİ HAZIRLIĞI (SENİN LİSTEN) ---

KARAKTERLER = {
    "Ana Karakterler": [
        "Salvo Montalbano", "Mimì Augello", "Giuseppe Fazio", 
        "Agatino Catarella", "Livia Burlando"
    ],
    "Olayla Bağlantılı Karakterler": [
        "Silvio Luparello", "Giorgio Saitta", "Ingrid Sjöström", 
        "Rino Barbera", "Gegè Gullotta", "Avvocato Rizzo", "Marchese di Villabianca"
    ],
    "Diğer Yan Karakterler": [
        "Dottor Pasquano", "Questore", "Bonetti-Alderighi"
    ]
}

# --- 2. FONKSİYONLAR ---

def metni_yukle():
    try:
        with open("kitap.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def bolumlere_ayir(metin):
    if not metin: return {}
    # Sadece 1-10 arası bölümler
    sayi_basliklari = ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto", "Nove", "Dieci"]
    satirlar = metin.split('\n')
    bolumler = {}
    su_anki_bolum = "Giriş"
    gecici_metin = []

    for satir in satirlar:
        temiz = satir.strip()
        if temiz.capitalize() in sayi_basliklari:
            if gecici_metin:
                bolumler[su_anki_bolum] = "\n".join(gecici_metin).strip()
            su_anki_bolum = temiz.capitalize()
            gecici_metin = []
        else:
            gecici_metin.append(satir)
    if gecici_metin:
        bolumler[su_anki_bolum] = "\n".join(gecici_metin).strip()
    return bolumler

# --- 3. ANA ARAYÜZ ---

st.header("🔍 Leggo Camilleri: La Forma dell'Acqua")
st.markdown("---")

ham_metin = metni_yukle()
bolumler = bolumlere_ayir(ham_metin)

# Sidebar
menu = st.sidebar.radio("Menü", ["📖 Kitabı Oku", "👥 Karakter Analizi"])

if menu == "📖 Kitabı Oku":
    if bolumler:
        secilen = st.selectbox("Bölüm Seç:", list(bolumler.keys()))
        st.subheader(f"📍 {secilen}")
        st.write(bolumler[secilen])
    else:
        st.error("Kanka 'kitap.txt' boş veya bulunamadı!")

elif menu == "👥 Karakter Analizi":
    st.info("Bu panel, senin belirlediğin özel karakter listesini Uno-Dieci arasında arar.")
    
    # Kategori Seçimi
    kategori = st.selectbox("Karakter Kategorisi:", list(KARAKTERLER.keys()))
    secilen_isim = st.selectbox("İsim Seç:", KARAKTERLER[kategori])
    
    st.divider()
    
    # Arama Aralığını Birleştir (Sadece 1-10)
    analiz_metni = " ".join([bolumler[b] for b in bolumler if b in ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto", "Nove", "Dieci"]])
    
    # Sadece soyadını veya adını da içerecek şekilde akıllı arama yapalım (Örn: Sadece 'Montalbano' geçse de bulsun)
    arama_kelimesi = secilen_isim.split()[-1] # Soyadını al (Montalbano, Fazio vb.)
    
    # Metni cümlelere bölüp ismi arayalım
    cumleler = [c.strip() + "." for c in analiz_metni.split('.') if arama_kelimesi in c]
    
    if cumleler:
        st.success(f"**{secilen_isim}** karakteri 1-10. bölümler arasında bulundu!")
        st.write(f"**Örnek Pasaj:**")
        st.write(f"*{cumleler[0]}*")
        
        with st.expander("Tüm geçtiği yerleri listele"):
            for c in cumleler:
                st.write(f"- {c}")
    else:
        st.warning(f"**{secilen_isim}** ismi Uno-Dieci arasındaki bölümlerde geçmiyor.")