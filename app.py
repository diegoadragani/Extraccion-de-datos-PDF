import streamlit as st
import google.generativeai as genai
import PyPDF2

# Título de la Web App
st.set_page_config(page_title="Extractor Envíos ML", layout="wide")
st.title("📦 Extractor de Datos de Envío #62292832")

# Configurar API Key (la pondremos en un paso secreto luego)
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader("Cargá el PDF del Listado Inicial", type="pdf")

if uploaded_file:
    # 1. Leer texto del PDF
    reader = PyPDF2.PdfReader(uploaded_file)
    texto_pdf = ""
    for page in reader.pages:
        texto_pdf += page.extract_text()

    # 2. Tu Prompt Maestro con validaciones
    prompt = f"""
    Extraé y valida los datos del siguiente texto de envío:
    REGLAS DE SKU:
    - Estándar: 3 letras + 5 números (ej. SIC11000)[cite: 22].
    - KIT: "KIT" + 3 letras + 3 números (ej. KITSIC040)[cite: 22].
    - FULL: "KIT" + 3 letras + 3 números + "FULL" (ej. KITMHH004FULL).
    
    INSTRUCCIONES:
    - Generá una tabla con SKU, Cantidad y Código ML.
    - Protocolo Anti-Error: No confundas I con 1 ni O con 0.
    - Validación: Sumá las unidades y compará con el 'Total de unidades' del PDF[cite: 24].
    - Conteo: Verificá que el número de filas sea igual a 'Productos del envio'[cite: 24].
    
    TEXTO DEL PDF:
    {texto_pdf}
    """

    if st.button("Procesar y Validar Datos"):
        with st.spinner('Analizando envío...'):
            response = model.generate_content(prompt)
            st.markdown(response.text)
