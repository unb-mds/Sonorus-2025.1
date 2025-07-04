import pytest
from unittest.mock import patch, MagicMock

import src.backend.utils.gravar_wav as gravar_wav

def test_gravacao_audio_sucesso(monkeypatch):
    # Mock sd.rec, sd.wait e sf.write
    fake_audio = MagicMock()
    monkeypatch.setattr(gravar_wav.sd, "rec", lambda *a, **kw: fake_audio)
    monkeypatch.setattr(gravar_wav.sd, "wait", lambda: None)
    monkeypatch.setattr(gravar_wav.sf, "write", lambda filename, audio, fs, subtype: None)

    # Simula execução do script
    try:
        exec(
            "audio = sd.rec(int(DURACAO * FS), samplerate=FS, channels=CANAIS, dtype='int16')\n"
            "sd.wait()\n"
            "sf.write('voz_usuario.wav', audio, FS, subtype='PCM_16')",
            gravar_wav.__dict__
        )
    except Exception:
        pytest.fail("Não deveria lançar exceção em cenário de sucesso.")

def test_gravacao_audio_falha_rec(monkeypatch):
    # Simula erro ao iniciar gravação
    monkeypatch.setattr(gravar_wav.sd, "rec", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("Erro no microfone")))
    monkeypatch.setattr(gravar_wav.sd, "wait", lambda: None)
    monkeypatch.setattr(gravar_wav.sf, "write", lambda filename, audio, fs, subtype: None)

    with pytest.raises(RuntimeError, match="Erro no microfone"):
        exec(
            "audio = sd.rec(int(DURACAO * FS), samplerate=FS, channels=CANAIS, dtype='int16')\n"
            "sd.wait()\n"
            "sf.write('voz_usuario.wav', audio, FS, subtype='PCM_16')",
            gravar_wav.__dict__
        )

def test_gravacao_audio_falha_write(monkeypatch):
    # Mock sd.rec e sd.wait para sucesso, sf.write para falha
    fake_audio = MagicMock()
    monkeypatch.setattr(gravar_wav.sd, "rec", lambda *a, **kw: fake_audio)
    monkeypatch.setattr(gravar_wav.sd, "wait", lambda: None)
    monkeypatch.setattr(gravar_wav.sf, "write", lambda *a, **kw: (_ for _ in ()).throw(IOError("Falha ao salvar arquivo")))

    with pytest.raises(IOError, match="Falha ao salvar arquivo"):
        exec(
            "audio = sd.rec(int(DURACAO * FS), samplerate=FS, channels=CANAIS, dtype='int16')\n"
            "sd.wait()\n"
            "sf.write('voz_usuario.wav', audio, FS, subtype='PCM_16')",
            gravar_wav.__dict__
        )