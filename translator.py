import speech_recognition as sr
from googletrans import Translator
import pyttsx3

# Configuração do reconhecimento de fala
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Configuração da tradução
translator = Translator()

# Configuração da síntese de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Ajuste a velocidade da fala

def listen_and_translate(target_language='pt'):
    with mic as source:
        print("Estou escutando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Reconhecimento de fala
        text = recognizer.recognize_google(audio)
        print(f"Você disse: {text}")

        # Tradução
        translated_text = translator.translate(text, dest=target_language).text
        print(f"Tradução: {translated_text}")

        # Síntese de voz
        engine.say(translated_text)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Não entendi o que foi dito.")
    except sr.RequestError as e:
        print(f"Erro no serviço de reconhecimento de fala: {e}")

if __name__ == "__main__":
    while True:
        listen_and_translate(target_language='pt')
