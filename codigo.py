import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Tenta importar a biblioteca de imagem. Se falhar, avisa o utilizador.
try:
    from skimage import io
except ImportError:
    st.error("⚠️ Faltam bibliotecas! Vai ao terminal e corre: pip install scikit-image matplotlib")
    st.stop()

st.set_page_config(page_title="Set-Piece Planner Pro", page_icon="⛳", layout="wide")

# --- Título ---
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

# --- FUNÇÃO DE DESENHO REALISTA ---
def desenhar_campo_realista(tipo, posicoes_jogadores):
    # Cria a figura
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # 1. CARREGAR RELVA (FUNDO)
    # Link direto para uma textura de relva
    url_relva = "https://images.unsplash.com/photo-1529900748604-07564a03e7a6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    
    try:
        relva_img = io.imread(url_relva)
        # extent define os limites [Xmin, Xmax, Ymin, Ymax]
        ax.imshow(relva_img, extent=[-10, 110, -10, 110], zorder=0)
    except Exception:
        # Se falhar a net, pinta de verde
        ax.set_facecolor('#4CAF50')

    # 2. LINHAS DO CAMPO (Brancas)
    style = {'color': 'white', 'linewidth': 3, 'zorder': 1, 'alpha': 0.9}
    
    plt.plot([0, 100], [0, 0], **style) # Fundo
    plt.plot([0, 100], [100, 100], **style) # Meio
    plt.plot([0, 0], [0, 100], **style) # Lateral E
    plt.plot([100, 100], [0, 100], **style) # Lateral D
    
    # Áreas
    ax.add_patch(patches.Rectangle((20, 0), 60, 16.5, lw=3, ec='white', fc=(1,1,1,0.1), zorder=1))
    ax.add_patch(patches.Rectangle((36, 0), 28, 5.5, lw=3, ec='white', fc=(1,1,1,0.1), zorder=1))
    
    # Baliza e Penalti
    ax.add_patch(patches.Rectangle((45, -2.5), 10, 2.5, lw=3, ec='black', fc='white', zorder=1))
    plt.scatter([50], [11], color="white", s=80, zorder=1)
    
    # Meio Lua
    ax.add_patch(patches.Arc((50, 16.5), 20, 20, theta1=0, theta2=180, color='white', lw=3, zorder=1))

    # 3. JOGADORES (Topo)
    coords = {
        "1º Poste (Curto)": (40, 6),
        "2º Poste (Longo)": (60, 6),
        "Marca de Penalti (Zona Central)": (50, 11),
        "Zona do Guarda-Redes (Estorvo)": (50, 3),
        "Rebordo da Área (Sobras)": (50, 22),
        "Equilíbrio Defensivo (Meio Campo)": (50, 45)
    }
    
    # Posição do Batedor
    if "Esq" in tipo: coords["Batedor (Na Bola)"] = (0, 0)
    elif "Dir" in tipo: coords["Batedor (Na Bola)"] = (100, 0)
    else: coords["Batedor (Na Bola)"] = (20, 25)
        
    for zona, nome in posicoes_jogadores.items():
        if zona in coords:
            x, y = coords[zona]
            # Sombra do jogador
            ax.add_patch(plt.Circle((x+1, y-1), 3, color='black', alpha=0.4, zorder=2))
            # Jogador (Vermelho)
            ax.add_patch(plt.Circle((x, y), 3, color='#FF5252', ec='white', lw=2, zorder=3))
            # Nome (Caixa preta)
            plt.text(x, y+4.5, nome, color='white', ha='center', fontweight='bold', fontsize=10, zorder=4, 
                     bbox=dict(facecolor='black', alpha=0.6, edgecolor='none', pad=1))

    # Limites visuais
    plt.xlim(-10, 110)
    plt.ylim(-10, 60)
    plt.axis('off')
    return fig

# --- Layout ---
col1, col2 = st.columns([1, 2])
with col1:
    st.info(f"**Lance:** {tipo_lanced}")
    if posicoes:
        st.write("📋 **Jogadores:**")
        for z, n in posicoes.items(): st.write(f"- {n}: {z}")
    else: st.warning("Define os jogadores na lateral!")
    st.success(f"**Instrução:** {notas}")

with col2:
    figura = desenhar_campo_realista(tipo_lanced, posicoes)
    st.pyplot(figura)
