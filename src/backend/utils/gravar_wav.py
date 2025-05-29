# gravar_audio_terminal.py
import sounddevice as sd
import soundfile as sf

DURACAO = 10  # segundos
FS = 16000    # taxa de amostragem
CANAIS = 1    # mono

print(f"Gravando áudio por {DURACAO} segundos. Fale: 'Minha voz é minha senha'...")
audio = sd.rec(int(DURACAO * FS), samplerate=FS, channels=CANAIS, dtype='int16')
sd.wait()
sf.write('voz_usuario.wav', audio, FS, subtype='PCM_16')
print("Áudio salvo como voz_usuario.wav")