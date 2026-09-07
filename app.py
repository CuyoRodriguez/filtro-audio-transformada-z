<<<<<<< HEAD
import io

import numpy as np
import streamlit as st
from scipy.io import wavfile
from scipy.signal import lfilter


def aplicar_filtro_z(audio_data, sample_rate):
	b = np.array([1.0, 0.4])
	a = np.array([1.0, -0.2, 0.01])

	return lfilter(b, a, np.asarray(audio_data), axis=0)


st.title("Filtro de Audio con Transformada Z")

archivo_wav = st.file_uploader("Carga un archivo de audio WAV", type=["wav"])

if archivo_wav is not None:
	sample_rate, audio_data = wavfile.read(archivo_wav)

	audio_original = io.BytesIO()
	wavfile.write(audio_original, sample_rate, audio_data)
	audio_original.seek(0)

	st.audio(audio_original.getvalue(), format="audio/wav")

	if st.button("Aplicar Filtro IIR"):
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
=======
import io

import numpy as np
import streamlit as st
from scipy.io import wavfile
from scipy.signal import lfilter


def aplicar_filtro_z(audio_data, sample_rate):
	b = np.array([1.0, 0.4])
	a = np.array([1.0, -0.2, 0.01])

	return lfilter(b, a, np.asarray(audio_data), axis=0)


st.title("Filtro de Audio con Transformada Z")

archivo_wav = st.file_uploader("Carga un archivo de audio WAV", type=["wav"])

if archivo_wav is not None:
	sample_rate, audio_data = wavfile.read(archivo_wav)

	audio_original = io.BytesIO()
	wavfile.write(audio_original, sample_rate, audio_data)
	audio_original.seek(0)

	st.audio(audio_original.getvalue(), format="audio/wav")

	if st.button("Aplicar Filtro IIR"):
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
>>>>>>> 9f0b37dc7d4ee9e184139783357b30332339e9fd
