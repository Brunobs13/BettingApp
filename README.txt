README.TXT - Instruções para Execução do Programa MegaSenaApp

Pré-Requisitos

A aplicação foi desenvolvida e testada com a versão Python 3.11.5. Deve ter a versão correta antes de prosseguir.

Execução do Programa

	Abra um terminal ou prompt de comando.
	Navegue até o diretório onde os ficheiros do MegaSenaApp foram extraídos.
	Execute o seguinte comando para iniciar o programa: 
             python MegaSenaApp.py 
 Certifique-se de que o caminho para o Python está corretamente configurado no seu sistema para que este comando funcione.

Uso do Programa


	Inserir Aposta: Na interface principal, insira sua aposta (4 números de 1 a 99) no campo fornecido.
	Salvar Aposta: Após inserir sua aposta, clique no botão "Salvar Aposta".
	Verificar Sorteio: Clique no botão "Conferir" para verificar o resultado do sorteio.
	Reiniciar Jogo: Para fazer uma nova aposta, clique no botão "Jogar Novamente".
	Encerrar o Jogo: Para encerrar o programa, clique no botão "Abandonar Jogo".




Notas Adicionais para o programador

As apostas e os resultados do sorteio são salvos automaticamente num ficheiro de texto ou CSV, dependendo da configuração do programa.

Para alterar o nome do arquivo em que as apostas e resultados são armazenados, é necessário fazer essa alteração manualmente na classe MegaSenaApp. Para isso, localize a linha 318 do código e modifique o nome do arquivo na criação do objeto DataStorage. Por exemplo:
#Antes
self.data_storage = DataStorage('apostas_e_resultados.txt')
#Depois
self.data_storage = DataStorage(‘novo_nome_do_arquivo.txt’)

O programa pode ser personalizado para diferentes regiões com diferentes prémios, conforme definido nas instâncias da classe Região.

Para utilizar plenamente as funcionalidades do programa, é necessário instalar a biblioteca multipledispatch. Essa biblioteca é usada para implementar a sobrecarga de métodos no código, permitindo que um mesmo nome de método seja utilizado para diferentes tipos de argumentos. Para instalar a biblioteca multipledispatch, deve-se executar o seguinte comando no terminal ou na linha de comando:
   pip install multipledispatch

