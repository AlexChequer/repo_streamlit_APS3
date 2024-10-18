import streamlit as st
import requests as rq  

URL = 'https://api-bicicletas-j9e8.onrender.com'

def tela_inicial():
    st.title("Tela Inicial")

def fetch_data(endpoint):
    try:
        response = rq.get(f'{URL}/{endpoint}')
        response.raise_for_status()
        return response.json()
    except rq.exceptions.HTTPError as err:
        st.error(f"Erro ao acessar {endpoint}: {err}")
        return None

def display_table(data):
    if data:
        st.table(data)

def minhas_bikes():
    bikes = fetch_data('bicicletas')
    display_table(bikes)

def meus_usuarios():
    usuarios = fetch_data('usuarios')
    display_table(usuarios)

def meus_emprestimos():
    emprestimos = fetch_data('emprestimos')
    display_table(emprestimos)

def cadastrar_bike():
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    cidade = st.text_input("Cidade")
 
    if st.button('Cadastrar'):
        response = rq.post(f'{URL}/bicicletas', json={"marca": marca, "modelo": modelo, "cidade": cidade})
        if response.status_code == 201:
            st.success('Bicicleta cadastrada com sucesso')
        else:
            st.error('Erro ao cadastrar bicicleta')

def cadastrar_usuario():
    cpf = st.text_input("CPF")
    data_nascimento = st.text_input("Data de Nascimento")
    nome = st.text_input("Nome")
    if st.button('Cadastrar'):
        response = rq.post(f'{URL}/usuarios', json={"cpf": cpf, "data_nascimento": data_nascimento, "nome": nome})
        if response.status_code == 201:
            st.success('Usuário cadastrado com sucesso')
        else:
            st.error('Erro ao cadastrar usuário')

def cadastrar_emprestimo():
    id_usuario = st.text_input('Id do Usuário')
    id_bike = st.text_input('Id da Bike')
    data_aluguel = st.text_input("Data de Aluguel")
    if st.button("Cadastrar"):
        usuario_response = rq.get(f'{URL}/usuarios/{id_usuario}')
        bike_response = rq.get(f'{URL}/bicicletas/{id_bike}')
        
        if usuario_response.status_code != 200 or bike_response.status_code != 200:
            st.error('Usuário ou bike não encontrados')
        else:
            response = rq.post(f'{URL}/emprestimos/usuarios/{id_usuario}/bicicletas/{id_bike}', json={'data_aluguel': data_aluguel})
            if response.status_code == 201:
                st.success("Empréstimo cadastrado com sucesso")
            else:
                st.error('Erro ao cadastrar empréstimo')

def dados_usuario():
    id_usuario = st.text_input('Id do Usuário')
    if st.button('Buscar Usuário'):
        usuario_data = fetch_data(f'usuarios/{id_usuario}')
        display_table(usuario_data)
        
        if usuario_data:
            cpf = st.text_input("CPF", value=usuario_data.get("cpf"))
            nome = st.text_input("Nome", value=usuario_data.get("nome"))
            data_nascimento = st.text_input("Data de Nascimento", value=usuario_data.get("data_nascimento"))
            if st.button('Atualizar Usuário'):
                response = rq.put(f'{URL}/usuarios/{id_usuario}', json={"cpf": cpf, "data_nascimento": data_nascimento, "nome": nome})
                if response.status_code == 200:
                    st.success('Usuário atualizado com sucesso')
                else:
                    st.error('Erro ao atualizar usuário')
            if st.button('Apagar Usuário'):
                response = rq.delete(f'{URL}/usuarios/{id_usuario}')
                if response.status_code == 204:
                    st.success('Usuário apagado com sucesso')
                else:
                    st.error('Erro ao apagar usuário')

def dados_bike():
    id_bike = st.text_input('Id da Bike')
    if st.button('Buscar Bike'):
        bike_data = fetch_data(f'bicicletas/{id_bike}')
        display_table(bike_data)
        
        if bike_data:
            marca = st.text_input("Marca", value=bike_data.get("marca"))
            modelo = st.text_input("Modelo", value=bike_data.get("modelo"))
            cidade = st.text_input("Cidade", value=bike_data.get("cidade"))
            status = st.text_input("Status", value=bike_data.get("status"))
            if st.button('Atualizar Bike'):
                response = rq.put(f'{URL}/bicicletas/{id_bike}', json={"marca": marca, "modelo": modelo, "cidade": cidade, "status": status})
                if response.status_code == 200:
                    st.success('Bike atualizada com sucesso')
                else:
                    st.error('Erro ao atualizar bike')
            if st.button('Apagar Bike'):
                response = rq.delete(f'{URL}/bikes/{id_bike}')
                if response.status_code == 204:
                    st.success('Bike apagada com sucesso')
                else:
                    st.error('Erro ao apagar bike')

def apaga_emprestimo():
    id_emprestimo = st.text_input('Id do Empréstimo')
    if st.button('Apagar Empréstimo'):
        response = rq.delete(f'{URL}/emprestimos/{id_emprestimo}')
        if response.status_code == 204:
            st.success('Empréstimo apagado com sucesso')
        else:
            st.error('Erro ao apagar empréstimo')

if __name__ == "__main__":
    tela_inicial()
    st.sidebar.subheader("Menu")
    
    opcao = st.sidebar.selectbox(
        "Selecione uma opção:",
        ["Minhas Bikes", "Meus Usuários", "Meus Empréstimos", "Nova Bike", "Novo Usuário", "Novo Empréstimo", "Dados Usuário", "Dados Bike", "Apagar Empréstimo"]
    )
    
    menu_functions = {
        "Minhas Bikes": minhas_bikes,
        "Meus Usuários": meus_usuarios,
        "Meus Empréstimos": meus_emprestimos,
        "Nova Bike": cadastrar_bike,
        "Novo Usuário": cadastrar_usuario,
        "Novo Empréstimo": cadastrar_emprestimo,
        "Dados Usuário": dados_usuario,
        "Dados Bike": dados_bike,
        "Apagar Empréstimo": apaga_emprestimo
    }
    
    menu_functions[opcao]()
