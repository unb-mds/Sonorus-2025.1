import soundfile as sf
from fastapi import HTTPException
from src.backend.models.modelo_ecapa import ModeloECAPA
import numpy as np
import os

# Inicializa o modelo ECAPA
modelo_ecapa = ModeloECAPA()

# Simulação de um banco de dados de embeddings, substituir pelo banco real depois
embeddings_usuarios = {
        "lemes": np.array([
          2.65768700e+01, 3.55227203e+01, -2.72377338e+01, -4.03870487e+00,
    -2.56373310e+01, 2.29106693e+01, -4.14702511e+00, 4.18712044e+01,
    9.10071182e+00, -1.32153015e+01, 5.75514717e+01, 1.01087656e+01,
    1.18733156e+00, 7.24860802e-02, -4.87236977e+01, -2.78101749e+01,
    5.03241777e+00, -2.43647194e+00, -7.45445395e+00, 2.72088909e+01,
    -2.44719982e+01, 1.52680933e+00, 2.08661723e+00, 4.82032433e+01,
    1.04364033e+01, -4.50871325e+00, -8.93338978e-01, -2.15620956e+01,
    2.64766884e+01, -3.43110108e+00, 1.29528904e+01, 2.78706479e+00,
    -1.16477890e+01, 5.21680489e+01, 2.07219715e+01, -5.40619326e+00,
    9.69308090e+00, 2.26251125e+01, -1.04366722e+01, -3.26818466e+01,
    1.83976841e+01, 8.47472477e+00, -2.75806694e+01, 3.08830338e+01,
    -3.94237556e+01, -2.90479450e+01, -5.42752743e-01, 1.18120947e+01,
    1.34867296e+01, -7.73005629e+00, -8.91311741e+00, 4.30066414e+01,
    -6.70246363e+00, 1.67101192e+01, -3.85816879e+01, 2.69851055e+01,
    1.15400381e+01, 1.37915287e+01, -1.93783607e+01, -6.34299278e+00,
    -2.26835327e+01, -1.74760952e+01, 3.10650959e+01, -3.79506836e+01,
    -2.73880787e+01, 2.80058842e+01, 2.71812325e+01, 1.70044690e-01,
    -2.43920059e+01, -2.12165966e+01, -3.68457103e+00, 6.56594849e+00,
    4.84898643e+01, -1.19323273e+01, -1.15086603e+01, -3.46695786e+01,
    -1.07629004e+01, -3.58184204e+01, 2.82098026e+01, -9.56253815e+00,
    2.01325855e+01, 2.52887611e+01, 2.76115417e+01, -9.14652824e+00,
    3.66710091e+01, 2.96593056e+01, -1.85802460e+01, 2.03537025e+01,
    -4.22342072e+01, -2.29996090e+01, -3.64978123e+00, 2.82971916e+01,
    -1.45208025e+01, 9.58923149e+00, -1.45848866e+01, -1.31656837e+00,
    3.48407402e+01, 4.75209522e+00, -1.29996815e+01, -1.44885902e+01,
    -3.38469207e-01, 2.61519833e+01, -9.88358593e+00, -2.38678513e+01,
    -3.48138356e+00, -8.00583661e-01, -1.39592705e+01, -2.85664062e+01,
    -8.01647091e+00, -3.24774780e+01, 4.00465393e+01, 1.31090994e+01,
    -1.43806820e+01, -2.15523949e+01, -2.75325317e+01, 4.44370747e+00,
    -5.29344654e+00, -9.00728035e+00, -2.33237419e+01, 3.73035698e+01,
    -1.23100872e+01, -5.79808617e+01, -1.26206141e+01, -1.56156912e+01,
    -5.10016251e+01, 4.88783360e+00, -5.05995117e-02, 2.10484619e+01,
    -1.93322430e+01, 3.32891560e+00, 2.58451481e+01, 4.23883855e-01,
    2.33246593e+01, -2.42799549e+01, 2.26760912e+00, 4.92846603e+01,
    -1.02735960e+00, 5.83005953e+00, 1.18300123e+01, -8.82695580e+00,
    -3.04425297e+01, -7.08404236e+01, 1.78954754e+01, -4.02715797e+01,
    1.48931494e+01, 4.44565344e+00, 1.76892567e+00, -9.76894945e-02,
    -3.77388687e+01, -2.54385986e+01, -1.31712162e+00, 2.59366627e+01,
    1.39311543e+01, -3.52250433e+00, 6.99579697e+01, -3.77792511e+01,
    3.57757301e+01, 8.95842075e+00, 2.34673519e+01, 1.93544502e+01,
    2.10658646e+01, 3.08296623e+01, 1.94161434e+01, 4.36083908e+01,
    -2.58373489e+01, 9.09092546e-01, 1.12059298e+01, -2.25409317e+01,
    3.62085533e+01, -9.65522766e+00, 4.64462727e-01, 1.11750281e+00,
    3.00598216e+00, -1.82855740e+01, -2.89164009e+01, 7.53389168e+00,
    1.27517712e+00, -2.45595398e+01, 7.24384022e+00, -2.74588013e+01,
    9.31502819e+00, -3.67341852e+00, 1.20071974e+01, 3.37131157e+01,
    9.83623600e+00, 4.03396785e-01, -8.57043934e+00, -9.48885307e-02,
    -1.35723057e+01, -4.24814339e+01, -2.38172512e+01, 1.78297579e+00
    ])
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")

# Certifica-se de que o diretório "audios" existe
os.makedirs(AUDIOS_DIR, exist_ok=True)

def processar_e_verificar_voz(login: str, arquivo) -> float:
    """
    Processa o áudio recebido e retorna a pontuação de similaridade.
    """
    if login not in embeddings_usuarios:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    try:
        # Lê o arquivo de áudio enviado
        dados_audio, taxa_amostragem = sf.read(arquivo.file)
        print(f"Áudio recebido com taxa de amostragem: {taxa_amostragem}")
        
        # Define o caminho para salvar o áudio temporário
        caminho_audio_temporario = os.path.join(AUDIOS_DIR, f"temp_{login}.wav")
        sf.write(caminho_audio_temporario, dados_audio, taxa_amostragem)
        print(f"Áudio salvo temporariamente em: {caminho_audio_temporario}")

        # Calcula a pontuação de similaridade
        pontuacao_similaridade = modelo_ecapa.verificar_falante(
            caminho_audio_temporario, embeddings_usuarios[login]
        )
        print(f"Pontuação de similaridade: {pontuacao_similaridade}")
    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    finally:
        # Remove o arquivo temporário após o processamento
        if os.path.exists(caminho_audio_temporario):
            os.remove(caminho_audio_temporario)
            print(f"Arquivo temporário removido: {caminho_audio_temporario}")

    return pontuacao_similaridade