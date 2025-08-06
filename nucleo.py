import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import os
import time

# Configurações do Wikipedia para português
wikipedia.set_lang("pt")

# Inicializa pyttsx3 usando o eSpeak
engine = pyttsx3.init(driverName='sapi5')  # Força o uso do espeak

# Procura uma voz em português disponível
voice_found = False
for v in engine.getProperty('voices'):
    # Imprime todas as vozes disponíveis para debug:
    print(v.id)
    if 'pt' in v.id or 'brazil' in v.id or 'portuguese' in v.id:
        engine.setProperty('voice', v.id)
        voice_found = True
        break

if not voice_found:
    print("Voz em português não encontrada! O Atlas vai falar com voz padrão do eSpeak.")

engine.setProperty('rate', 160)  # Velocidade da fala


def falar(texto):
    print(f"Atlas: {texto}")
    engine.say(texto)
    engine.runAndWait()
    engine.stop()


def ouvir():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Aguardando...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        comando = r.recognize_google(audio, language="pt-BR")
        print("Você disse:", comando)
        return comando.lower()
    except:
        return ""


def pesquisar_wikipedia(pergunta):
    try:
        resultado = wikipedia.summary(pergunta, sentences=2)
        return resultado
    except Exception:
        return "Desculpe, não encontrei resultados para sua pesquisa."


def executar_comando(comando):
    if "horas" in comando:
        hora_atual = time.strftime('%H:%M')
        falar(f"Agora são {hora_atual}")
    elif "procure por" in comando or "pesquisar por" in comando:
        termo = comando.split("por")[-1].strip()
        falar(f"Procurando por {termo} na Wikipedia.")
        resultado = pesquisar_wikipedia(termo)
        falar(resultado)
    elif "abrir" in comando:
        site = comando.split("abrir")[-1].strip()
        if "youtube" in site:
            webbrowser.open("https://youtube.com")
            falar("Abrindo YouTube.")
        elif "google" in site:
            webbrowser.open("https://google.com")
            falar("Abrindo Google.")
        else:
            webbrowser.open("https://"+site)
            falar(f"Abrindo {site}.")
    elif "tocar música" in comando:
        falar("Tocando uma música de exemplo.")
        # Edite o caminho da sua música ou troque o player se preferir
        os.system('espeak "Tocando música!"')
    elif "piada" in comando:
        falar("Por que o programador foi ao médico? Porque estava com um vírus!")
    elif "parar" in comando or "sair" in comando:
        falar("Até logo!")
        exit()
    else:
        falar("Comando não reconhecido. Pode repetir, por favor?")


ativo = False
falar("Olá, meu nome é Atlas. Para começar, diga 'Atlas'.")

while True:
    if not ativo:
        comando = ouvir()
        if "atlas" in comando:
            if "pare de ouvir" in comando:
                falar("Já estou em modo de espera.")
            else:
                ativo = True
                falar("Estou ouvindo, pode falar!")
    else:
        comando = ouvir()
        if "atlas" in comando and "pare de ouvir" in comando:
            ativo = False
            falar("Ok, parei de ouvir. Diga 'Atlas' para me chamar novamente.")
        elif "atlas" in comando:
            falar("Estou ouvindo, pode falar!")
        elif comando:
            executar_comando(comando)
