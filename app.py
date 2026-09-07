import io

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from scipy.io import wavfile
from scipy.signal import lfilter


def aplicar_filtro_z(audio_data, sample_rate):
	b = np.array([1.0, 0.4])
	a = np.array([1.0, -0.2, 0.01])

	return lfilter(b, a, np.asarray(audio_data), axis=0)


def graficar_comparacion(audio_orig, audio_filt, sample_rate):
	audio_orig = np.asarray(audio_orig)
	audio_filt = np.asarray(audio_filt)
	if audio_orig.ndim == 2:
		audio_orig = audio_orig[:, 0]
	if audio_filt.ndim == 2:
		audio_filt = audio_filt[:, 0]
	if audio_orig.dtype == np.int16:
		audio_orig = audio_orig.astype(np.float64) / 32768.0

	longitud = min(len(audio_orig), len(audio_filt))
	tiempo = np.arange(longitud) / sample_rate
	fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
	axes[0].plot(tiempo, audio_orig[:longitud], color="#147d92", linewidth=0.8)
	axes[0].set_title("Audio Original")
	axes[0].set_ylabel("Amplitud")
	axes[0].set_ylim(-1.0, 1.0)
	axes[0].grid(alpha=0.25)
	axes[1].plot(tiempo, audio_filt[:longitud], color="#d97706", linewidth=0.8)
	axes[1].set_title("Audio Filtrado")
	axes[1].set_xlabel("Tiempo (s)")
	axes[1].set_ylabel("Amplitud")
	axes[1].set_ylim(-1.0, 1.0)
	axes[1].grid(alpha=0.25)
	fig.tight_layout()
	return fig


st.set_page_config(
	page_title="Filtro IIR - Transformada Z",
	page_icon="🎵",
	layout="wide",
)

st.markdown(
	"""
	<style>
	    .stApp {
	        background: #f4f7fb;
	    }
	    [data-testid="stSidebar"] {
	        background: #102a43;
	    }
	    [data-testid="stSidebar"] * {
	        color: #e8f1f8;
	    }
	    .eyebrow {
	        color: #147d92;
	        font-size: 0.78rem;
	        font-weight: 700;
	        letter-spacing: 0.12em;
	        text-transform: uppercase;
	        margin-bottom: 0.35rem;
	    }
	    .hero-title {
	        color: #102a43;
	        font-size: 2.55rem;
	        font-weight: 800;
	        line-height: 1.1;
	        margin: 0;
	    }
	    .hero-copy {
	        color: #486581;
	        font-size: 1.05rem;
	        margin-top: 0.7rem;
	        max-width: 720px;
	    }
	    .card {
	        background: #ffffff;
	        border: 1px solid #d9e2ec;
	        border-radius: 8px;
	        box-shadow: 0 8px 24px rgba(16, 42, 67, 0.07);
	        padding: 1.35rem;
	        height: 100%;
	    }
	    .card-label {
	        color: #627d98;
	        font-size: 0.78rem;
	        font-weight: 700;
	        letter-spacing: 0.08em;
	        text-transform: uppercase;
	    }
	    .card-title {
	        color: #102a43;
	        font-size: 1.2rem;
	        font-weight: 750;
	        margin: 0.35rem 0 0.8rem;
	    }
	    .meta {
	        color: #627d98;
	        font-size: 0.9rem;
	        margin-top: 0.8rem;
	    }
	    .sidebar-heading {
	        color: #ffffff;
	        font-size: 1.05rem;
	        font-weight: 750;
	        margin-top: 1.2rem;
	    }
	</style>
	""",
	unsafe_allow_html=True,
)

with st.sidebar:
	st.markdown("## Filtro IIR")
	st.caption("Referencia matemática")

	st.markdown('<div class="sidebar-heading">Secuencia causal</div>', unsafe_allow_html=True)
	st.latex(r"f[n] = (0.1)^n + 0.5n(0.1)^{n-1}, \quad n \geq 0")
	st.write("La secuencia combina una exponencial decreciente con un término lineal ponderado. Al asumir causalidad, sus muestras comienzan en n = 0.")

	st.markdown('<div class="sidebar-heading">Dominio Z</div>', unsafe_allow_html=True)
	st.latex(r"H(z) = \frac{z^2 + 0.4z}{(z - 0.1)^2}")
	st.caption("Forma equivalente para lfilter: b = [1.0, 0.4] y a = [1.0, -0.2, 0.01].")

	st.markdown('<div class="sidebar-heading">Efecto sobre el audio</div>', unsafe_allow_html=True)
	st.write("El sistema actúa como un filtro IIR paso bajas y suavizador: atenúa las frecuencias agudas mientras conserva las componentes graves.")

with st.container():
	st.markdown('<div class="eyebrow">Procesamiento digital de señales</div>', unsafe_allow_html=True)
	st.markdown('<h1 class="hero-title">Filtro de Audio con Transformada Z</h1>', unsafe_allow_html=True)
	st.markdown('<p class="hero-copy">Carga una grabación WAV, escúchala y aplica el filtro IIR derivado de la secuencia causal.</p>', unsafe_allow_html=True)

st.write("")

with st.container():
	carga_col, estado_col = st.columns([1.55, 1], gap="large")
	with carga_col:
		st.markdown(
			'<div class="card"><div class="card-label">Paso 01</div><div class="card-title">Carga tu archivo</div>',
			unsafe_allow_html=True,
		)
		archivo_wav = st.file_uploader("Selecciona un archivo WAV", type=["wav"], label_visibility="collapsed")
		st.markdown('</div>', unsafe_allow_html=True)
	with estado_col:
		st.markdown(
			'<div class="card"><div class="card-label">Configuración</div><div class="card-title">Filtro establecido</div><div class="meta">IIR de segundo orden<br>Preserva la frecuencia de muestreo original</div></div>',
			unsafe_allow_html=True,
		)

if archivo_wav is not None:
	sample_rate, audio_data = wavfile.read(archivo_wav)
	canales = 2 if audio_data.ndim == 2 else 1
	tipo_canales = "Estéreo" if canales == 2 else "Mono"
	audio_procesado = None

	audio_original = io.BytesIO()
	wavfile.write(audio_original, sample_rate, audio_data)
	audio_original.seek(0)

	st.write("")
	with st.container():
		original_col, filtrado_col = st.columns(2, gap="large")
		with original_col:
			st.markdown(
				'<div class="card"><div class="card-label">Paso 02</div><div class="card-title">Audio Original</div>',
				unsafe_allow_html=True,
			)
			st.audio(audio_original.getvalue(), format="audio/wav")
			st.markdown(f'<div class="meta">{sample_rate:,} Hz · {tipo_canales}</div></div>', unsafe_allow_html=True)

		with filtrado_col:
			st.markdown(
				'<div class="card"><div class="card-label">Paso 03</div><div class="card-title">Audio Filtrado</div>',
				unsafe_allow_html=True,
			)
			if st.button("Aplicar Filtro IIR", type="primary", use_container_width=True):
				with st.spinner("Procesando señal de audio con la Transformada Z... Por favor espera"):
					audio_procesado = aplicar_filtro_z(audio_data, sample_rate)
				audio_procesado = np.asarray(audio_procesado, dtype=np.float64)
				audio_procesado = np.nan_to_num(audio_procesado, nan=0.0, posinf=1.0, neginf=-1.0)

				maximo = np.max(np.abs(audio_procesado), initial=0.0)
				if maximo > 1.0:
					audio_procesado = audio_procesado / maximo

				audio_procesado = np.clip(audio_procesado, -1.0, 1.0).astype(np.float32)
				audio_filtrado = io.BytesIO()
				wavfile.write(audio_filtrado, sample_rate, audio_procesado)
				audio_filtrado.seek(0)

				st.audio(audio_filtrado.getvalue(), format="audio/wav")
				st.success("¡Audio filtrado con éxito!")
				metrica_rate, metrica_canales = st.columns(2)
				with metrica_rate:
					st.metric("Sample Rate", f"{sample_rate:,} Hz")
				with metrica_canales:
					st.metric("Canales", tipo_canales)
				st.markdown('<div class="meta">Señal suavizada y normalizada</div>', unsafe_allow_html=True)
			else:
				st.info("Pulsa el botón para generar la versión filtrada.")
			st.markdown('</div>', unsafe_allow_html=True)

	if audio_procesado is not None:
		st.write("")
		st.markdown('<div class="card-label">Comparación temporal</div>', unsafe_allow_html=True)
		fig = graficar_comparacion(audio_data, audio_procesado, sample_rate)
		st.pyplot(fig)
