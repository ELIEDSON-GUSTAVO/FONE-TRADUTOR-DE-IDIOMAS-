import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
import pygame
from googletrans import Translator

# Inicializa o mixer do Pygame
pygame.mixer.init()

def speak(text):
    """ Converte texto em fala e reproduz o áudio. """
    # Cria um arquivo temporário para o áudio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file_path = temp_file.name
        
    tts = gTTS(text=text, lang='pt')
    tts.save(temp_file_path)
    
    pygame.mixer.music.load(temp_file_path)
    pygame.mixer.music.play()
    
    # Espera a reprodução terminar
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Adiciona um delay antes de remover o arquivo
    pygame.time.wait(1000)
    
    # Remove o arquivo após a reprodução
    try:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    except PermissionError as e:
        print(f"Erro ao remover o arquivo: {e}")

def recognize_speech():
    """ Reconhece a fala e retorna o texto. """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Hola senhor, traduzirei o que o senhor precisar. Diga 'traduza' quando quiser que eu faça a tradução.")
        
        print("Pronto para traduzir. Fale agora ou diga 'traduza' quando quiser traduzir.")
        
        while True:
            speak("Estou ouvindo")
            audio = recognizer.listen(source)
            
            try:
                text = recognizer.recognize_google(audio, language='pt')
                print("Você disse: " + text)
                if 'traduza' in text.lower():
                    print("Comando 'traduza' detectado.")
                    return
                else:
                    print("Comando 'traduza' não detectado. Tente novamente.")
            except sr.UnknownValueError:
                print("Não consegui entender o áudio.")
            except sr.RequestError:
                print("Não foi possível solicitar resultados; verifique sua conexão com a Internet.")

def translate_and_speak(target_lang='en'):
    """ Traduz o texto reconhecido e fala a tradução. """
    recognizer = sr.Recognizer()
    translator = Translator()

    print("Fale o texto a ser traduzido.")
    speak("Fale o texto a ser traduzido.")
    speak("Estou ouvindo")

    with sr.Microphone() as source:
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='pt')
            print("Texto para tradução: " + text)
            
            translated = translator.translate(text, dest=target_lang)
            translated_text = translated.text
            
            print("Tradução: " + translated_text)
            speak(f"A tradução é: {translated_text}")
            speak("Ok")
        except sr.UnknownValueError:
            print("Não consegui entender o áudio.")
            speak("Não consegui entender o áudio.")
        except sr.RequestError:
            print("Não foi possível solicitar resultados; verifique sua conexão com a Internet.")

def main():
    """ Função principal para iniciar a tradução. """
    print("Pressione 'q' para sair.")
    speak("Pressione 'q' para sair.")
    
    while True:
        recognize_speech()
        translate_and_speak()
        
        # Pergunta ao usuário se deseja continuar
        print("Digite 's' para continuar ou 'q' para sair.")
        command = input("Digite o comando: ").strip().lower()
        
        if command == 'q':
            print("Saindo...")
            speak("Saindo...")
            break

if __name__ == "__main__":
    main()
