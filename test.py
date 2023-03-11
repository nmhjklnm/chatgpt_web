import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def transcribe():
    r = sr.Recognizer()
    st.write("请开始说话")
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=5)
        st.write("识别中...")
        text = r.recognize_google(audio_data, language='zh-CN')
        st.write(f"识别结果：{text}")
    return text


def speak(text):
    tts = gTTS(text, lang='zh-cn')
    tts.save("output.mp3")
    sound = AudioSegment.from_mp3("output.mp3")
    play(sound)


st.title("语音转文本")

if st.button("录入"):
    text = transcribe()
    if st.button("播放"):
        if text:
            speak(text)
        else:
            st.write("请先录入文本")
