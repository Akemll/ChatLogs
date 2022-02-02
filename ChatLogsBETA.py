#Importações
import requests
import time
#Fim


#Váriaveis
try:
    token = str(input("Informe o token do seu discord:"))
    limite = str(input("Informe o numero de mensagem que vai ficar dentro do range do script em cada canal(Recomendado 50):"))
    canais = str(input("Informe os canais desejados, seguindo o exemplo (id de canal), (id de canal), (id de canal):")).split(", ")
    tempo = float(input("Quanto tempo quer de espera pra o script analisar os chats novamente? (Padrao:0.1)"))
except Exception:
      canais = []
contar = 0
conteudo = ""   
antigo = 0
co = 0
rosa = "\033[31m"
branco = "\033[0;0m"
textos = {}
canaisp = {}
listanomes = {}
attachment = {}
posi = {}
#Fim

#Anti-Bug
if tempo < 0.1:
    tempo = 0.1
#Fim

#Funções
def dinamico(palavra, rosaa=False):
    global antigo, listanomes, attachment
    conteudo = ""
    print(" "*antigo, end="\r")
    if rosaa:
        conteudo = f"{rosa}{palavra}{branco}"
        print(conteudo, end="\r")
    else:
        conteudo = palavra
        print(conteudo)
    antigo = len(conteudo)


def atualizacao(oi=False):
    global textos, listanomes, token, limite
    for e in canais:
        recebido = requests.get(f"https://discord.com/api/v9/channels/{e}/messages?limit={limite}", headers={"Authorization": f"{token}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"})
        if not oi:
            dinamico(f"Status de {e}: Analisando...", True)
        if recebido.status_code < 300 and recebido.status_code >= 200:
            conteudo = recebido.json()
            contar = 0
            contar1 = 0
            localizao = 0
            if not oi:
                dinamico(f"Status de {e}: Sucesso!", True)
            for _ in conteudo:
                contar += 1
            for oo in conteudo:
                if oo["attachments"] != []:
                    attachment[oo["id"]] = oo["attachments"][0]["url"]
                contar1 += 1
                posi[oo["id"]] = contar1
                if not oi:
                    dinamico(f"Tratando de textos do canal {e}: {contar1}/{contar}", True)
                if oo["channel_id"] not in textos:
                    textos[oo["channel_id"]] = {}
                if oo["id"] not in textos[oo["channel_id"]]:
                    textos[oo["channel_id"]][oo["id"]] = oo["content"]
                nome = oo["author"]["username"]
                tag = oo["author"]["discriminator"]
                listanomes[oo["id"]] = f"{nome}#{tag}"
        else:
            dinamico(f"Não foi possível estabelecer conexão com {e}, verifique as condições.")
            canais.remove(e)
#Fim

if token and limite:
     atualizacao()
     dinamico("Sistema atualizado com sucesso!", True)
     print("", end="\n")
try:
   while True:
       if not canais or not token or not limite or not limite.isnumeric() or limite < 5 or not tempo:
           dinamico("Argumentos faltando para continuacao, verifice os argumentos de canais,token, e limite.", True)
           break
       time.sleep(tempo)
       for e in canais:
           recebido = requests.get(f"https://discord.com/api/v9/channels/{e}/messages?limit={limite}", headers={"Authorization": f"{token}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"})
           if recebido.status_code < 300 and recebido.status_code >= 200:
                 conteudo = recebido.json()
                 listap = {}
                 for oo in conteudo:
                     if not oo["channel_id"] in listap:
                        listap[oo["channel_id"]] = {}
                        listap[oo["channel_id"]][oo["id"]] = oo["content"]
                        nome = oo["author"]["username"]
                        tag = oo["author"]["discriminator"]
                        listanomes[oo["id"]] = f"{nome}#{tag}"
                 if e in textos:
                     for pp in textos[e]:
                         if pp in listap[e]:
                            if listap[e][pp] != textos[e][pp] and textos[e][pp] is not None:
                                if pp in attachment:
                                     dinamico(f"Mensagem alterada: \nUsuário:{listanomes[pp]}\nConteudo antigo:{textos[e][pp]}\nConteudo novo:{listap[e][pp]}\nAttachment:{attachment[pp]}", True)
                                else:
                                     dinamico(f"Mensagem alterada: \nUsuário:{listanomes[pp]}\nConteudo antigo:{textos[e][pp]}\nConteudo novo:{listap[e][pp]}", True)
                                     textos[e][pp] = listap[e][pp]
                                     print("", end="\n\n")
                            else:
                               if posi[pp] < (limite - 4) and textos[e][pp] is not None:
                                  if pp in attachment:
                                     dinamico(f"Mensagem deletada: \nUsuário:{listanomes[pp]}\nConteudo:{textos[e][pp]}\nAttachment:{attachment[pp]}", True)
                                  else:
                                      dinamico(f"Mensagem deletada: \nUsuário:{listanomes[pp]}\nConteudo:{textos[e][pp]}", True)
                                      textos[e][pp] = None
                                      print("", end="\n\n")
                 else:       
                     dinamico(f"Não foi possível estabelecer conexão com {e}, verifique as condições.")
                     canais.remove(e)
                     atualizacao(True)
except KeyboardInterrupt:
	print("Obrigada por usar o script, volte sempre!")
