from pytube.innertube import _default_clients
from pytube import cipher
import re


_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]



def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    #logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            #logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )

cipher.get_throttling_function_name = get_throttling_function_name

from pytube import YouTube
import streamlit as st

def descargar_video(url, tipo='video'):
    yt = YouTube(url)
    
    if tipo == 'audio':
        stream = yt.streams.filter(only_audio=True).first()
        descarga = stream.download(filename=f"{yt.title}.mp3")
    else:
        stream = yt.streams.get_highest_resolution()
        descarga = stream.download(filename=f"{yt.title}.mp4")
    
    return descarga

st.title('Descargar MP3 y MP4 de YouTube')

url = st.text_input('Ingresa la URL del video de YouTube')

formato = st.radio('Selecciona el formato de descarga', ('video', 'audio'))

if st.button('Descargar'):
    if url:
        try:
            st.write('Descargando...')
            archivo = descargar_video(url, tipo=formato)
            st.success(f'Descarga completada: {archivo}')
        except Exception as e:
            st.error(f'Error durante la descarga: {e}')
    else:
        st.error('Por favor, ingresa una URL válida')

