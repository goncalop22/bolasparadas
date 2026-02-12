import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Set-Piece Planner", page_icon="⛳", layout="wide")

# --- Título e Configuração ---
st.title("⛳ Mestre das Bolas Paradas")
st.markdown("Planeamento tático para Cantos e Livres. **Define quem vai onde.**")

# --- Lista de Jogadores (Editável) ---
if 'plantel' not in st.session_state:
    st.session_state['plantel'] = [
        "GR (Guarda-Redes)", "João (DC)", "Pedro (DC)", "Tiago (LE)", 
        "André (LD)", "Lucas (MDF)", "Mateus (MC)", "Rui (MC)", 
        "Simão (EXT)", "Nuno (EXT)", "Tomás (PL)"
    ]

# --- Sidebar: Configuração da Jogada ---
with st.sidebar:
    st.header("⚙️ Configurar Jogada")
    
    tipo_lanced = st.selectbox("Tipo de Lance", ["Canto Ofensivo (Esq)", "Canto Ofensivo (Dir)", "Livre Lateral"])
    
    st.divider()
    st.subheader("📍 Atribuição de Funções")
    
    # Dicionário para guardar as posições escolhidas
    posicoes = {}
    
    # Definição das zonas críticas num Canto/Livre
    zonas = [
        "Batedor (Na Bola)",
        "1º Poste (Curto)",
        "2º Poste (Longo)",
        "Marca de Penalti (Zona Central)",
        "Zona do Guarda-Redes (Estorvo)",
        "Rebordo da Área (Sobras)",
        "Equilíbrio Defensivo (Meio Campo)"
    ]
    
    # Criar um dropdown para cada zona
    jogadores_disponiveis = ["Ninguém"] + st.session_state['plantel']
    
    for zona in zonas:
        # Tenta adivinhar um jogador diferente para cada posição para ser mais rápido (opcional)
        escolha = st.selectbox(f"Quem vai para: {zona}?", jogadores_disponiveis, index=0)
        if escolha != "Ninguém":
            posicoes[zona] = escolha

    st.divider()
    notas = st.text_area("📝 Notas Táticas (ex: 'Sinal: Braço levantado')", "Atacar a bola no ponto mais alto.")

# --- FUNÇÃO DE DESENHO DO CAMPO (MATPLOTLIB) ---
def desenhar_campo(tipo, posicoes_jogadores):
    # Criar figura verde (o relvado)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor('#4CAF50') # Verde Relva
    
    # Desenhar as linhas do campo (Meio campo ofensivo)
    # Limites
    plt.plot([0, 100], [0, 0], color="white", linewidth=2) # Linha de fundo
    plt.plot([0, 100], [100, 100], color="white", linewidth=2) # Meio campo
    plt.plot([0, 0], [0, 100], color="white", linewidth=2) # Lateral Esq
    plt.plot([100, 100], [0, 100], color="white", linewidth=2) # Lateral Dir
    
    # Grande Área
    grande_area = patches.Rectangle((20, 0), 60, 16.5, linewidth=2, edgecolor='white', facecolor='none')
    ax.add_patch(grande_area)
    
    # Pequena Área
    pequena_area = patches.Rectangle((36, 0), 28, 5.5, linewidth=2, edgecolor='white', facecolor='none')
    ax.add_patch(pequena_area)
    
    # Baliza
    baliza = patches.Rectangle((45, -2), 10, 2, linewidth=3, edgecolor='black', facecolor='white')
    ax.add_patch(baliza)
    
    # Marca de Penalti
    plt.scatter([50], [11], color="white", s=50)
    
    # Meio Lua
    arc = patches.Arc((50, 16.5), 20, 20, angle=0, theta1=0, theta2=180, color='white', linewidth=2)
    ax.add_patch(arc)

    # --- Lógica de Coordenadas (Onde cada zona fica no gráfico X,Y) ---
    # X vai de 0 a 100 (Largura), Y vai de 0 a 100 (Comprimento)
    coords = {
        "1º Poste (Curto)": (40, 5),
        "2º Poste (Longo)": (60, 5),
        "Marca de Penalti (Zona Central)": (50, 11),
        "Zona do Guarda-Redes (Estorvo)": (50, 2),
        "Rebordo da Área (Sobras)": (50, 20),
        "Equilíbrio Defensivo (Meio Campo)": (50, 40)
    }
    
    # Ajustar posição do batedor dependendo do lado
    if "Esq" in tipo:
        coords["Batedor (Na Bola)"] = (0, 0) # Canto Inferior Esquerdo
    elif "Dir" in tipo:
        coords["Batedor (Na Bola)"] = (100, 0) # Canto Inferior Direito
    else: # Livre
        coords["Batedor (Na Bola)"] = (20, 25) # Lateral
        
    # --- Desenhar os Jogadores ---
    for zona, nome in posicoes_jogadores.items():
        if zona in coords:
            x, y = coords[zona]
            # Desenhar o círculo (jogador)
            circle = plt.Circle((x, y), 2.5, color='red', zorder=10)
            ax.add_patch(circle)
            # Escrever o nome do jogador
            plt.text(x, y+3.5, nome, color='white', ha='center', fontweight='bold', fontsize=10, zorder=11, 
                     bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', pad=1))

    # Ajustes finais do gráfico
    plt.xlim(-5, 105)
    plt.ylim(-5, 60) # Mostrar apenas meio campo ofensivo
    plt.axis('off') # Esconder eixos X/Y numéricos
    
    return fig

# --- Layout Principal ---
col1, col2 = st.columns([1, 2])

with col1:
    st.info(f"**Cenário:** {tipo_lanced}")
    st.markdown("### Resumo das Funções")
    if posicoes:
        for z, n in posicoes.items():
            st.write(f"**{n}**: {z}")
    else:
        st.warning("Define os jogadores na barra lateral!")
        
    st.success(f"**Instrução:** {notas}")

with col2:
    st.subheader("📋 Quadro Tático")
    # Gerar o gráfico
    figura_campo = desenhar_campo(tipo_lanced, posicoes)
    # Mostrar no Streamlit
    st.pyplot(figura_campo)
