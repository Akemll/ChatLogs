#Importações
import requests
import time
#Fim


#Váriaveis
contar = 0
conteudo = ""   
antigo = 0
co = 0
rosa = "\033[1;95m"
branco = "\033[0;0m"
textos = {}
canais = ["884831545448349719", "884831545448349720", "895124208743506000", "923682865353461790"]
canaisp = {}
listanomes = {}
attachment = {}
posi = {}
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
#Fim

def atualizacao(oi=False):
    global textos, listanomes
    for e in canais:
        recebido = requests.get(f"https://discord.com/api/v9/channels/{e}/messages?limit=50", headers={"Authorization": "ODUzNDc2NjQ5NTg4NzUyMzg0.YdHmuA.xufnJnhEuV84k5pJSkOTqSFboso", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"})
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
    return None

atualizacao()
dinamico("Sistema atualizado com sucesso!", True)
print("", end="\n")
while True:
    time.sleep(0.1)
    for e in canais:
        recebido = requests.get(f"https://discord.com/api/v9/channels/{e}/messages?limit=100", headers={"Authorization": "ODUzNDc2NjQ5NTg4NzUyMzg0.YdHmuA.xufnJnhEuV84k5pJSkOTqSFboso", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"})
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
                        if posi[pp] < 46 and textos[e][pp] is not None:
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