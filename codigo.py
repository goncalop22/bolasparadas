import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
# Import necessário para ler imagens da web
try:
    from skimage import io
except ImportError:
    st.error("Precisas de instalar o scikit-image: pip install scikit-image")
    st.stop()

st.set_page_config(page_title="Set-Piece Planner Pro", page_icon="⛳", layout="wide")

# --- Título e Configuração ---
st.title("⛳ Mestre das Bolas Paradas (Modo Realista)")
st.markdown("Planeamento tático com fundo de relvado real.")

# --- Lista de Jogadores ---
if 'plantel' not in st.session_state:
    st.session_state['plantel'] = [
        "GR (Guarda-Redes)", "João (DC)", "Pedro (DC)", "Tiago (LE)", 
        "André (LD)", "Lucas (MDF)", "Mateus (MC)", "Rui (MC)", 
        "Simão (EXT)", "Nuno (EXT)", "Tomás (PL)"
    ]

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configurar Jogada")
    tipo_lanced = st.selectbox("Tipo de Lance", ["Canto Ofensivo (Esq)", "Canto Ofensivo (Dir)", "Livre Lateral"])
    st.divider()
    st.subheader("📍 Atribuição de Funções")
    
    posicoes = {}
    zonas = [
        "Batedor (Na Bola)", "1º Poste (Curto)", "2º Poste (Longo)",
        "Marca de Penalti (Zona Central)", "Zona do Guarda-Redes (Estorvo)",
        "Rebordo da Área (Sobras)", "Equilíbrio Defensivo (Meio Campo)"
    ]
    jogadores_disponiveis = ["Ninguém"] + st.session_state['plantel']
    for zona in zonas:
        escolha = st.selectbox(f"Quem vai para: {zona}?", jogadores_disponiveis, index=0)
        if escolha != "Ninguém":
            posicoes[zona] = escolha
    st.divider()
    notas = st.text_area("📝 Notas Táticas", "Atacar a bola no ponto mais alto.")

# --- FUNÇÃO DE DESENHO COM FUNDO REALISTA ---
def desenhar_campo_realista(tipo, posicoes_jogadores):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # --- 1. CARREGAR A IMAGEM DE FUNDO (RELVA) ---
    # URL de uma textura de relva (podes trocar por um ficheiro local teu)
    url_relva = "https://st2.depositphotos.com/3901183/6758/i/950/depositphotos_67586169-stock-photo-green-grass-texture-background.jpg"
    
    try:
        # Tenta ler a imagem da internet
        relva_img = io.imread(url_relva)
        # Desenha a imagem no fundo (zorder=0 é a camada mais atrás)
        # 'extent' define que a imagem deve esticar para cobrir todo o campo que vamos desenhar
        ax.imshow(relva_img, extent=[-10, 110, -10, 110], zorder=0)
    except Exception as e:
        # Se falhar (sem internet, etc.), usa cor sólida como plano B
        st.warning(f"Não foi possível carregar a textura de relva. A usar cor sólida.")
        ax.set_facecolor('#4CAF50')

    # --- 2. DESENHAR AS LINHAS DO CAMPO (Camada zorder=1) ---
    # Usamos zorder=1 para as linhas ficarem por cima da relva
    linha_style = {'color': 'white', 'linewidth': 3, 'zorder': 1, 'alpha': 0.8}
    
    plt.plot([0, 100], [0, 0], **linha_style) # Linha de fundo
    plt.plot([0, 100], [100, 100], **linha_style) # Meio campo
    plt.plot([0, 0], [0, 100], **linha_style) # Lateral Esq
    plt.plot([100, 100], [0, 100], **linha_style) # Lateral Dir
    
    # Áreas (com preenchimento transparente para se ver a relva por baixo)
    grande_area = patches.Rectangle((20, 0), 60, 16.5, linewidth=3, edgecolor='white', facecolor=(1,1,1,0.1), zorder=1)
    ax.add_patch(grande_area)
    pequena_area = patches.Rectangle((36, 0), 28, 5.5, linewidth=3, edgecolor='white', facecolor=(1,1,1,0.1), zorder=1)
    ax.add_patch(pequena_area)
    
    # Baliza e Marcas
    baliza = patches.Rectangle((45, -2.5), 10, 2.5, linewidth=3, edgecolor='black', facecolor='white', zorder=1)
    ax.add_patch(baliza)
    plt.scatter([50], [11], color="white", s=80, zorder=1) # Penalti
    
    arc = patches.Arc((50, 16.5), 20, 20, angle=0, theta1=0, theta2=180, color='white', linewidth=3, zorder=1)
    ax.add_patch(arc)

    # --- 3. COORDENADAS E JOGADORES (Camada zorder=2 - Topo) ---
    coords = {
        "1º Poste (Curto)": (40, 6),
        "2º Poste (Longo)": (60, 6),
        "Marca de Penalti (Zona Central)": (50, 11),
        "Zona do Guarda-Redes (Estorvo)": (50, 3),
        "Rebordo da Área (Sobras)": (50, 22),
        "Equilíbrio Defensivo (Meio Campo)": (50, 45)
    }
    
    if "Esq" in tipo: coords["Batedor (Na Bola)"] = (0, 0)
    elif "Dir" in tipo: coords["Batedor (Na Bola)"] = (100, 0)
    else: coords["Batedor (Na Bola)"] = (20, 25)
        
    for zona, nome in posicoes_jogadores.items():
        if zona in coords:
            x, y = coords[zona]
            # Círculo do jogador com sombra para destacar do relvado
            shadow = plt.Circle((x+0.5, y-0.5), 2.8, color='black', alpha=0.3, zorder=2)
            ax.add_patch(shadow)
            circle = plt.Circle((x, y), 2.8, color='#FF5252', ec='white', lw=2, zorder=3)
            ax.add_patch(circle)
            
            # Texto com fundo escuro para leitura fácil sobre a relva
            plt.text(x, y+4, nome, color='white', ha='center', fontweight='bold', fontsize=11, zorder=4, 
                     bbox=dict(facecolor='black', alpha=0.7, edgecolor='none', pad=2))

    # Ajustes finais
    plt.xlim(-10, 110)
    plt.ylim(-10, 60) # Foco no meio campo ofensivo
    plt.axis('off')
    return fig

# --- Layout Principal ---
col1, col2 = st.columns([1, 2])
with col1:
    st.info(f"**Cenário:** {tipo_lanced}")
    st.markdown("### Funções")
    if posicoes:
        for z, n in posicoes.items(): st.write(f"**{n}**: {z}")
    else: st.warning("Define os jogadores na barra lateral!")
    st.success(f"**Instrução:** {notas}")

with col2:
    figura_campo = desenhar_campo_realista(tipo_lanced, posicoes)
    st.pyplot(figura_campo)
