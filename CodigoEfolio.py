#!/usr/bin/env python3
#Codigo de Bruno Ricardo de Sa ferreira
#Numero de estudante 2201529

import tkinter as tk
import tkinter.messagebox as messagebox
import random
import os
import datetime

class ApostaInterface:
	def __init__(self, master, aposta_reader, data_storage, conferir_button, numeros_sorteados_interface):
		self.frame = tk.Frame(master) #cria um novo frame
		self.frame.pack() #empacota p frame 
		
		self.label = tk.Label(self.frame, text="Digite a aposta (4 números até 99 separados por vírgula):") #cria label com instruções
		self.label.pack() #empacota
		
		self.entry = tk.Entry(self.frame) #campo de entrada para usuário
		self.entry.pack()
		
		self.button = tk.Button(self.frame, text="Salvar Aposta", command=self.salvar_aposta)#botão que chama o metodo salvar aposta
		self.button.pack() #empacota para que seja exibido
		
		self.aposta_reader = aposta_reader
		self.data_storage = data_storage
		self.conferir_button = conferir_button
		self.numeros_sorteados_interface = numeros_sorteados_interface #armazena as variaveis acima para usar mais tarde
		self.contador_apostas = 0 #contador de apostar iniciado em zero
		
	def salvar_aposta(self):
		#contador para verificar se já foi feita aposta
		if self.contador_apostas == 0:
			entrada = self.entry.get()#entrada do usuário
			if not entrada: #erro pra entrada vazia 
				messagebox.showerror("Erro", "Por favor, insira 4 números separados por vírgulas.")
				return
			try:
				numeros_entrada = entrada.split(',') #divide a entrada do usuario em listas 
				if not all(item.isdigit() for item in numeros_entrada):#verifica se tudo na lista sao digitos
					raise ValueError("Só são válidos números. Caracteres inválidos foram inseridos.")
				aposta = list(map(int, numeros_entrada)) #converte lista de strings para lista de inteiros
				if len(aposta) != 4:
					raise ValueError("A aposta deve conter exatamente 4 números.")
				if any(numero > 99 for numero in aposta): #numeros na aposta tem de ser menores que 100, 2 digitos
					raise ValueError("Só são permitidos números até dois algarismos.")
				self.aposta_reader.salvar_aposta(aposta)#salva a aposta
				messagebox.showinfo("Sucesso", "Aposta salva com sucesso!")
				self.entry.delete(0, tk.END)#limpa entrada de texto
				self.contador_apostas += 1
				self.numeros_sorteados_interface.aposta_realizada()#indica que aposta foi realizada
				self.conferir_button['state'] = 'normal'  #Ativa o botão "Conferir"
				self.button['state'] = 'disabled'  #Desativa o botão "Salvar Aposta"
			except ValueError as e:
				messagebox.showerror("Erro", str(e))
		else:
			messagebox.showerror("Erro", "Você já salvou uma aposta. Clique em 'Conferir' para ver o resultado.")
			
	def resetar_apostas(self):
		#metodo que vai reinicar o estado da aposta
		self.contador_apostas = 0
		self.entry.delete(0, tk.END)  #Limpa a entrada de texto
		self.button['state'] = 'normal'  #Reativa o botão "Salvar Aposta"
		self.conferir_button['state'] = 'disabled'  # Desativa o botão "Conferir"
		self.numeros_sorteados_interface.resetar_interface()  #Chama o método para reset a interface dos numeros sorteados
		
class DataStorage:
	def __init__(self, arquivo): 
		self._arquivo = None
		self.arquivo = arquivo  #nome do arquivo com setter
		
	@property
	def arquivo(self):  #Getter _arquivo
		return self._arquivo
	
	@arquivo.setter
	def arquivo(self, valor):  #Setter _arquivo
		if not isinstance(valor, str): #verifica se o arquivo é string, na class megasenna
			raise ValueError("O nome do arquivo deve ser uma string.")
		if not valor.endswith('.txt'):
			raise ValueError("O arquivo deve ter a extensão .txt.") #verifica se e um txt
		self._arquivo = valor
		
	def salvar_aposta(self, aposta): #vamos salvar as apostas no arquivo
		agora = datetime.datetime.now() #data e horas atuais
		linha = f'Aposta feita em {agora.strftime("%d/%m/%Y às %H:%M")} - Aposta: {", ".join(map(str, aposta))}\n' #escreve no arquivo 
		with open(self.arquivo, 'a') as f:
			f.write(linha)
			
	def salvar_resultado(self, acertos, numeros_sorteados): #mesmo processo para salvar os resultados no arquivo
		linha = f"Resultado: {acertos} acertos - Sorteio: {', '.join(map(str, numeros_sorteados))}\n"
		with open(self.arquivo, 'a') as f: #abre o arquivo em append 
			f.write(linha)
			
		#def limpar_arquivo(self):#caso queiramos limpar o arquivo. 
		#open(self.arquivo, 'w').close()
		
class ApostaReader:
	def __init__(self, data_storage):
		self.data_storage = data_storage
		self.apostas = []  #lista vazia pata armazenar apostas
		
	def salvar_aposta(self, aposta):#metod para salvar aposta
		self.apostas.append(aposta)  #Acessa as apostas a lista 
		self.data_storage.salvar_aposta(aposta)  #salva a aposta atual
		
class NumeroConferente:
	def __init__(self, apostas):
		self.apostas = apostas
		
	@property
	def premio_4_acertos(self): #getter para premio
		return self.__premio_4_acertos
	
	@premio_4_acertos.setter #setter para premio
	def premio_4_acertos(self, valor):
		if isinstance(valor, int) and valor > 0: #verifica se o valor é inteiro positivo
			self.__premio_4_acertos = valor #define valor do premio
		else:
			raise ValueError("O prêmio deve ser um número inteiro positivo.")
			
	@property #mesma logica
	def premio_3_acertos(self):
		return self.__premio_3_acertos
	
	@premio_3_acertos.setter
	def premio_3_acertos(self, valor):
		if isinstance(valor, int) and valor > 0:
			self.__premio_3_acertos = valor
		else:
			raise ValueError("O prêmio deve ser um número inteiro positivo.")
			
	@property
	def premio_2_acertos(self):
		return self.__premio_2_acertos
	
	@premio_2_acertos.setter
	def premio_2_acertos(self, valor):
		if isinstance(valor, int) and valor > 0:
			self.__premio_2_acertos = valor
		else:
			raise ValueError("O prêmio deve ser um número inteiro positivo.")
			
	@property
	def premio_1_acerto(self):
		return self.__premio_1_acerto
	
	@premio_1_acerto.setter
	def premio_1_acerto(self, valor):
		if isinstance(valor, int) and valor > 0:
			self.__premio_1_acerto = valor
		else:
			raise ValueError("O prêmio deve ser um número inteiro positivo.")
			
	def conferir(self, aposta, numeros_sorteados):
		acertos = len(set(numeros_sorteados) & set(aposta))
		premio = 0 #define os premios de acordo com os acertos na classe regiao
		if acertos == 4:
			premio = self.premio_4_acertos
		elif acertos == 3:
			premio = self.premio_3_acertos
		elif acertos == 2:
			premio = self.premio_2_acertos
		elif acertos == 1:
			premio = self.premio_1_acerto
		return acertos, numeros_sorteados, premio
	
class ResultadoDisplay:
	def __init__(self, master):
		self.frame = tk.Frame(master)#novo frame
		self.frame.pack()
		
		self.label = tk.Label(self.frame, text="Resultados das Apostas:") #label com texto
		self.label.pack()
		
		self.text = tk.Text(self.frame, height=10, width=50, state='disabled')  #criacao campo de texto e restricao de escrita nele 
		self.text.pack()
		
	def mostrar_resultados(self, resultados, numeros_sorteados, aposta): #mostrar resultados
		self.text.config(state='normal')  # ativa a exibicao de resultado
		self.text.delete('1.0', tk.END)#apaga o texto existente da tela para entrar um novo
		for i, acertos in enumerate(resultados):
			numeros_acertados = set(numeros_sorteados) & set(aposta) #calcula numeros acertados
			self.text.insert(tk.END, f"Aposta {i+1}: {acertos} acertos\n") #insere a aposta do usuário
			self.text.insert(tk.END, f"Sua aposta: {', '.join(map(str, aposta))}\n") 
			self.text.insert(tk.END, f"Resultado do Sorteio: {', '.join(map(str, numeros_sorteados))}\n")
			if numeros_acertados:
				self.text.insert(tk.END, f"Você acertou os números: {', '.join(map(str, numeros_acertados))}\n\n")
		self.text.config(state='disabled')  #desativa a edicao de texto no display "resultado apostas"
		
class NumerosSorteadosInterface:
	def __init__(self, master, numero_conferente, data_storage, resultado_display, conferir_button):
		self.frame = tk.Frame(master)
		self.frame.pack()
		
		self.label = tk.Label(self.frame, text="Clique para verificar o sorteio:") #label com instrucoes
		self.label.pack()
		
		self.sorteio_entry = tk.Entry(self.frame, state='readonly')  #campo de entrada mas so funcional para leitura para exibir os sorteios
		self.sorteio_entry.pack()
		
		self.conferir_button = conferir_button #armazena o botao conferir
		self.conferir_button['command'] = self.conferir  
		self.conferir_button.pack() #empacota o botao conferir
		
		self.numero_conferente = numero_conferente
		self.data_storage = data_storage
		self.resultado_display = resultado_display
		self._aposta_feita = False  #atributo para verificar se uma aposta foi feita, comeca com false
		
	@property
	def aposta_feita(self):  #getter para aposta_feita
		return self._aposta_feita
	
	@aposta_feita.setter
	def aposta_feita(self, valor):  #setter para aposta_feita
		if not isinstance(valor, bool):
			raise ValueError("O valor atribuído a 'aposta_feita' deve ser um booleano (True ou False).")
		self._aposta_feita = valor
		
	def conferir(self):
		if self.aposta_feita:  # Usa o getter para acessar aposta_feita
			numeros_sorteados = self.gerar_sorteio()
			self.sorteio_entry.config(state='normal')
			self.sorteio_entry.delete(0, tk.END)
			self.sorteio_entry.insert(0, ', '.join(map(str, numeros_sorteados)))
			self.sorteio_entry.config(state='readonly')
		
			aposta_atual = self.numero_conferente.apostas[-1]  # A última aposta feita
			acertos, numeros_usados, premio = self.numero_conferente.conferir(aposta_atual, numeros_sorteados)
			self.data_storage.salvar_resultado(acertos, numeros_sorteados)
			if premio > 0:
				messagebox.showinfo("Parabéns!", f"Você ganhou {premio} euros!")
			self.resultado_display.mostrar_resultados([acertos], numeros_usados, aposta_atual)
		
			self.conferir_button['state'] = 'disabled'  #desativa o botão "Conferir" aposs o uso
			self.aposta_feita = False  #usa o setter para modificar aposta_feita
		else:
			messagebox.showinfo("Aviso", "Você precisa salvar pelo menos uma aposta antes de conferir.")
			
	def gerar_sorteio(self): #gerar sorteio, lista de 4 nmeros unicos de 1 a 99
		return random.sample(range(1, 99), 4)
	
	def aposta_realizada(self):
		self.aposta_feita = True  #Usa o setter para modificar aposta_feita, se for usada um string por ex, dara erro. 
		
	def resetar_interface(self): #resetar a interface, 
		self.sorteio_entry.config(state='normal')
		self.sorteio_entry.delete(0, tk.END)#limpa o campo de entrada 
		self.sorteio_entry.config(state='readonly') 
		self.conferir_button['state'] = 'disabled' #desativa o botao conferir para respeitar as regras

class Regiao:
	def __init__(self, nome, premio_4_acertos, premio_3_acertos, premio_2_acertos, premio_1_acerto): #construtor da classe recebe nome de paises e premios diferentes
		self.nome = nome #armazena regiao 
		self.premio_4_acertos = premio_4_acertos#armazena premios
		self.premio_3_acertos = premio_3_acertos
		self.premio_2_acertos = premio_2_acertos
		self.premio_1_acerto = premio_1_acerto
		
	def configurar_premios(self, numero_conferente): #configura os premios no objeto numero_conferente
		numero_conferente.premio_4_acertos = self.premio_4_acertos
		numero_conferente.premio_3_acertos = self.premio_3_acertos
		numero_conferente.premio_2_acertos = self.premio_2_acertos
		numero_conferente.premio_1_acerto = self.premio_1_acerto
		
# cria instancias da classe Regiao para  europa e américa do Sul
europa = Regiao("Europa", 2000000, 50000, 10000, 500)
america_sul = Regiao("América do Sul", 1000000, 50000, 10000, 500)

				
class MegaSenaApp:
	def __init__(self):
		self.root = tk.Tk()#janela principal da aplicacao
		self.root.title("Ganhe Milhões")
		
		self.data_storage = DataStorage('apostas_e_resultados.txt')#aqui em caso de erro o professor pode mudar o nome do arquivo que vai guardar todos os movimentos da app
		
		self.aposta_reader = ApostaReader(self.data_storage)#objeto para ler apostas
		self.numero_conferente = NumeroConferente(self.aposta_reader.apostas)#objeto para conferir apostas
		self.resultado_display = ResultadoDisplay(self.root) #displat para exibir resultados 
		
		#botão 'conferir' que comeca como desabilitado
		self.conferir_button = tk.Button(self.root, text="Conferir", state='disabled')
		self.conferir_button.pack()
		
		# interfaces passando os componentes necessarios
		self.numeros_sorteados_interface = NumerosSorteadosInterface(
			self.root, 
			self.numero_conferente, 
			self.data_storage, 
			self.resultado_display,
			self.conferir_button
		)
		
		self.aposta_interface = ApostaInterface(
			self.root, 
			self.aposta_reader, 
			self.data_storage, 
			self.conferir_button,
			self.numeros_sorteados_interface
		)
		
		#botoes para "Jogar Novamente" ou "Abandonar o Jogo"
		self.botao_jogar_novamente = tk.Button(self.root, text="Jogar Novamente", command=self.jogar_novamente)
		self.botao_jogar_novamente.pack(side=tk.LEFT)
		
		self.botao_abandonar_jogo = tk.Button(self.root, text="Abandonar Jogo", command=self.abandonar_jogo)
		self.botao_abandonar_jogo.pack(side=tk.RIGHT)
		
	def jogar_novamente(self):
		#jogar novamente 
		self.numeros_sorteados_interface.resetar_interface()
		self.aposta_interface.resetar_apostas()
		
	def abandonar_jogo(self):
		#abandona o jogo
		self.numeros_sorteados_interface.resetar_interface()
		self.aposta_interface.resetar_apostas()
		self.root.quit() 
		
	def run(self):
		self.root.mainloop()
		
if __name__ == "__main__":
	#isstncia da classe MegaSenaApp para a Europa
	app = MegaSenaApp()
	europa.configurar_premios(app.numero_conferente)
	app.run()#correr app
	