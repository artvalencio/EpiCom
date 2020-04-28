'''EpiCom
Simulador de epidemia em comunidade (toy model)


Este simulador é um toy-model de uma pequena comunidade (small-world)
composta de tres tipos de ambientes (áreas comuns, casas e locais de trabalho/escolas) e o impacto de
uma epidemia nesta comunidade.
Podem ser escolhidos os tamanhos padrão destes ambientes e o número de pessoas que abrigam.
A cada instante de tempo uma pessoa tem uma probabilidade pequena de se deslocar de ambiente, isto é,
ir da casa para o trabalho, por exemplo. Supõe-se que os deslocamentos em torno de 30".
O deslocamentos de uma pessoa é uma combinaçao de movimento aleatório (distribuiçao normal)
com movimento direcionado ao indivíduo mais próximo, replicando assim certos padrões de interaçao social
em diferentes espacialidades.
Em seguida, os parâmetros epidêmicos são adicionados ao modelo (tempo de incubação, probabilidade de contágio,
tempo de recuperacão, probabilidade de morte etc).

------------------------------------------------------------------------------------
ESTE MODELO É UMA APROXIMAÇAO BASTANTE SIMPLIFICADA E NÃO DEVE SER UTILIZADO PARA PREVISAO DE
CENÁRIOS EPIDEMIOLÓGICOS REAIS

Os propósitos desse modelo são EDUCATIVOS no sentido de avaliar como é possível, incrementalmente,
considerar variáveis socioespaciais e quais os impactos habituais no total de casos/mortes registradas.

------------------------------------------------------------------------------------

Arthur Valencio
Pós-doc, Instituto de Computação, Unicamp
CEPID NeuroMat
Bolsista de pós-doutorado, processo número 2017/09900-8, Fundaçao de Amparo à Pesquisa do Estado de
São Paulo (FAPESP)
Este trabalho foi produzido como parte das atividades do Centro de Pesquisa, Inovação e Difusão em
Neuromatemática (processo no. 2013/07699-0, FAPESP). As opiniões, hipóteses e conclusões ou recomendações
expressas neste material são de responsabilidade do autor e não necessariamente refletem a visão da FAPESP.


Norma Valencio
Professora Senior, Departamento de Ciencias Ambientais, UFSCar
Bolsista produtividade, processo número 310976/2017-0, Conselho Nacional de Desenvolvimento Científico e
Tecnológico (CNPq)

------------------------------------------------------------------------------------

Se útil, cite:
Valencio, A.; Valencio, N. Subsidios à uma discussão comunitária acerca de modelagem de epidemias.
In: Valencio, N.; Malan, C. COVID-19: Crises entremeadas no contexto de pandemia (antecedentes,
cenários e recomendações). São Carlos: CPOI-UFSCar, 2020.

Contato: arthur_valencio@physics.org
'''


import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import matplotlib.pyplot as plt

pessoas=[]

p_desenv_sintomatica=0.4
t_incubacao=20
t_recuperacao=100
p_morte=0.3
raio=5
p_assintomatico=0.4
p_sintomatico=0.7
total_casos=[]
total_mortos=[0]
total_curados=[0]
tempo=[0]
adiciona_casos=0
adiciona_mortos=0
adiciona_curados=0

class pessoa:
    def __init__(self,casa,trabalho,sz_casa,sz_trabalho,sz_cidade):
        self.casa=casa
        self.trabalho=trabalho
        if random.random()<0.6:
            self.localizacao="casa"
            self.x=random.random()*sz_casa
            self.y=random.random()*sz_casa
        #remover o comentario a seguir caso deseje populaçao inicial
        #nas áreas comuns da comunidade. (No caso, nao inserimos pois
        #pensamos em exemplificar o caso de lockdown, isto é,
        #p_transitar=0 implica áreas comuns vazias).
        #
        #elif random.random()<0.3:
        #    self.localizacao="cidade"
        #    self.x=random.random()*sz_cidade
        #    self.y=random.random()*sz_cidade
        else:
            self.localizacao="trabalho"
            self.x=random.random()*sz_trabalho
            self.y=random.random()*sz_trabalho
        self.status="nao infectado"
        self.conta_incubacao=-1
        self.conta_cura=-1
        self.sz_casa=sz_casa
        self.sz_trabalho=sz_trabalho
        self.sz_cidade=sz_cidade
        
    def move(self,pessoas,interacao,t_cura,p_transitar):        
        if random.random()>p_transitar:
            if self.localizacao=="casa":
                distancia=self.sz_casa**2
                for i in range(len(pessoas)):
                    if pessoas[i].localizacao=="casa":
                        if dist(self,pessoas[i])<distancia:
                            distancia=dist(self,pessoas[i])
                            idx=i                    
                dx=random.normalvariate(0,0.5*self.sz_casa)+10*interacao*(pessoas[idx].x-self.x)
                dy=random.normalvariate(0,0.5*self.sz_casa)+10*interacao*(pessoas[idx].y-self.y)
            elif self.localizacao=="trabalho":
                distancia=self.sz_trabalho**2
                for i in range(len(pessoas)):
                    if pessoas[i].localizacao=="trabalho":
                        if dist(self,pessoas[i])<distancia:
                            distancia=dist(self,pessoas[i])
                            idx=i   
                dx=random.normalvariate(0,0.05*self.sz_trabalho)+500*interacao*(pessoas[idx].x-self.x)
                dy=random.normalvariate(0,0.05*self.sz_trabalho)+500*interacao*(pessoas[idx].y-self.y)
            else:
                distancia=self.sz_cidade**2
                for i in range(len(pessoas)):
                    if pessoas[i].localizacao=="cidade":
                        if dist(self,pessoas[i])<distancia:
                            distancia=dist(self,pessoas[i])
                            idx=i
                dx=random.normalvariate(0,0.01*self.sz_cidade)+1000*interacao*(pessoas[idx].x-self.x)
                dy=random.normalvariate(0,0.01*self.sz_cidade)+1000*interacao*(pessoas[idx].y-self.y)
            self.x=self.x+dx
            self.y=self.y+dy
            if self.localizacao=="casa":
                if self.x>self.sz_casa:
                    self.x=self.x-(self.x-self.sz_casa)*(self.sz_casa/30)
                elif self.x<0:
                    self.x=-self.x*(self.sz_casa/30)
                if self.y>self.sz_casa:
                    self.y=self.y-(self.y-self.sz_casa)*(self.sz_casa/30)
                elif self.y<0:
                    self.y=-self.y*(self.sz_casa/30)
            elif self.localizacao=="trabalho":
                if self.x>self.sz_trabalho:
                    self.x=self.x-(self.x-self.sz_trabalho)*(self.sz_trabalho/30)
                elif self.x<0:
                    self.x=-self.x*(self.sz_trabalho/30)
                if self.y>self.sz_trabalho:
                    self.y=self.y-(self.y-self.sz_trabalho)*(self.sz_trabalho/30)
                elif self.y<0:
                    self.y=-self.y*(self.sz_trabalho/30)
            elif self.localizacao=="cidade":
                if self.x>self.sz_cidade:
                    self.x=self.x-(self.x-self.sz_cidade)*(self.sz_cidade/30)
                elif self.x<0:
                    self.x=-self.x*(self.sz_cidade/30)
                if self.y>self.sz_cidade:
                    self.y=self.y-(self.y-self.sz_cidade)*(self.sz_cidade/30)
                elif self.y<0:
                    self.y=-self.y*(self.sz_cidade/30)
        else:
            if random.random()<0.5:
                if self.localizacao=="casa":
                    self.localizacao="trabalho"
                    self.x=random.random()*self.sz_trabalho
                    self.y=random.random()*self.sz_trabalho
                elif self.localizacao=="trabalho":
                    self.localizacao="cidade"
                    self.x=random.random()*self.sz_cidade
                    self.y=random.random()*self.sz_cidade
                elif self.localizacao=="cidade":
                    self.localizacao="casa"
                    self.x=random.random()*self.sz_casa
                    self.y=random.random()*self.sz_casa
            else:
                if self.localizacao=="casa":
                    self.localizacao="cidade"
                    self.x=random.random()*self.sz_cidade
                    self.y=random.random()*self.sz_cidade
                elif self.localizacao=="trabalho":
                    self.localizacao="casa"
                    self.x=random.random()*self.sz_casa
                    self.y=random.random()*self.sz_casa
                elif self.localizacao=="cidade":
                    self.localizacao="trabalho"
                    self.x=random.random()*self.sz_trabalho
                    self.y=random.random()*self.sz_trabalho
        self.evolui_status(t_cura)

    def evolui_status(self,t_cura):
        global adiciona_curados
        global adiciona_mortos
        global adiciona_casos
        if self.status=="incubado" and self.conta_incubacao>0:
            self.conta_incubacao-=1
        elif self.status=="incubado" and self.conta_incubacao==0:
            self.conta_cura=t_cura
            self.conta_incubacao=-1
            if random.random()<p_desenv_sintomatica:
                self.status="sintomatico"
                adiciona_casos+=1
            else:
                self.status="assintomatico"
                self.conta_cura=t_cura
        elif self.status=="assintomatico":
            if t_cura==0:
                self.status="curado"                
                adiciona_curados+=1
            else:
                self.conta_cura-=1
        elif self.status=="sintomatico":
            if random.random()<p_morte:
                self.status="morto"
                self.localizacao="cemiterio"
                self.x=-1
                self.y=-1
                self.conta_cura=-1
                adiciona_mortos+=1
            elif self.conta_cura>0:
                self.conta_cura-=1
            else:
                self.status="curado"
                adiciona_curados+=1
                self.conta_cura=-1
        
def cria_cidade(n_pessoas,n_pessoas_trabalho,n_pessoas_casa,sz_casa,sz_trabalho,sz_cidade):
    trabalho=[]
    casa=[]
    conta_casa=n_pessoas_casa
    conta_trabalho=n_pessoas_trabalho
    c=0
    t=0
    for i in range(n_pessoas):
        casa.append(c)
        trabalho.append(t)
        conta_casa-=1
        conta_trabalho-=1
        if conta_casa<=0:
            conta_casa=n_pessoas_casa
            c=c+1
        if conta_trabalho<=0:
            conta_trabalho=n_pessoas_trabalho
            t=t+1
    random.shuffle(trabalho)
    for i in range(n_pessoas): 
        pessoas.append(pessoa(casa[i],trabalho[i],sz_casa,sz_trabalho,sz_cidade))

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def coluna(matriz,j):
    col=[]
    for i in range(len(matriz)-1):
        col.append(matriz[i][j])
    return col

def dist(p1,p2):
    if p1.localizacao==p2.localizacao:
        return ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**0.5
    else:
        return -1

def infecta(pessoas,raio,p_assintomatico,p_sintomatico,t_incubacao):
    l=len(pessoas)
    for i in range(l):
        if pessoas[i].status=="nao infectado":
            for j in range(l):
                if i!=j:
                    if pessoas[j].status=="nao infectado" or pessoas[j].status=="incubado" or pessoas[j]=="morto":
                        continue
                    elif pessoas[j].status=="assintomatico":
                        if dist(pessoas[i],pessoas[j])>=0 and dist(pessoas[i],pessoas[j])<raio:
                            if random.random()<p_assintomatico:
                                pessoas[i].status="incubado"
                                pessoas[i].conta_incubacao=t_incubacao
                    elif pessoas[j].status=="sintomatico":
                        if dist(pessoas[i],pessoas[j])>=0 and dist(pessoas[i],pessoas[j])<raio:
                            if random.random()<p_assintomatico:
                                pessoas[i].status="incubado"
                                pessoas[i].conta_incubacao=t_incubacao
                         
def main():

    sg.theme("SystemDefault")
    layout_params = [[ sg.Text('Insira os parametros')],
          [sg.Text('Variáveis socioespaciais:')],
          [sg.Text("1. Número de pessoas:"),sg.Slider((10,5000), key='n_pessoas', orientation='h', default_value=500, enable_events=True, disable_number_display=False),
          sg.Text("2. Número máximo de trabalhadores/estudantes em cada local:"),sg.Slider((1,500), key='n_trabalhos', orientation='h', default_value=30, enable_events=True, disable_number_display=False)],
          [sg.Text("3. Número total de moradores em cada casa:"),sg.Slider((1,15), key='n_casas', orientation='h', default_value=5, enable_events=True, disable_number_display=False),
          sg.Text("4. Tamanho das casas (m2):"),sg.Slider((5,300), key='sz_casa', orientation='h', default_value=40, enable_events=True, disable_number_display=False)],
          [sg.Text("5. Tamanho dos locais de trabalho/escolas (m2):"),sg.Slider((10,600), key='sz_trabalho', orientation='h',default_value=100, enable_events=True, disable_number_display=False),
          sg.Text("6. Tamanho da comunidade (áreas comuns) (m2):"),sg.Slider((50,10000), key='sz_cidade', orientation='h', default_value=1000, enable_events=True, disable_number_display=False)],
          [sg.Text("7. Interação social da populaçao:"),sg.Slider((0,100), key='interacao', orientation='h', default_value=50, enable_events=True, disable_number_display=False)],
          [sg.Text("8. Número médio de vezes por dia que um indivíduo transita entre ambientes interno-externo (ex: ir da casa para o trabalho):"),sg.Slider((0,4), key='p_transitar', resolution=0., orientation='h', default_value=2, enable_events=True, disable_number_display=False)],
          [sg.Text('Variáveis epidemiológicas:')],
          [sg.Text("10. Probabilidade de contágio a partir de contato com indivíduo assintomático (%):"),sg.Slider((0,100), key='p_assintomatico', default_value=10, orientation='h', resolution=1, enable_events=True, disable_number_display=False)],  
          [sg.Text("11. Probabilidade de contágio a partir de contato com indivíduo sintomático (%):"),sg.Slider((0,100), key='p_sintomatico', default_value=40, orientation='h', resolution=1, enable_events=True, disable_number_display=False)],  
          [sg.Text("12. Após o contágio, probabilidade de um indivíduo desenvolver forma sintomática (%):"),sg.Slider((0,100), default_value=40, resolution=1, key='p_desenv_sintomatica', orientation='h', enable_events=True, disable_number_display=False)],  
          [sg.Text("13. Tempo de incubação (dias):"),sg.Slider((1,100), key='t_incubacao', orientation='h', default_value=20, resolution=1, enable_events=True, disable_number_display=False),
          sg.Text("14. Tempo de recuperação (dias):"),sg.Slider((1,100), key='t_recuperacao', orientation='h', default_value=20, resolution=1, enable_events=True, disable_number_display=False)],
          [sg.Text("15. Probabilidade de morte (%):"),sg.Slider((0,100), key='p_morte', orientation='h', default_value=10, resolution=1, enable_events=True, disable_number_display=False),
          sg.Text("16. Raio de contágio (m):"),sg.Slider((0.1,10.0), key='raio', orientation='h', default_value=5, resolution=0.1, enable_events=True, disable_number_display=False)],
          [sg.Text("17. Percentual de pessoas inicialmente infectadas (%):"),sg.Slider((0.01,100), key='pc_infec', orientation='h', default_value=5, resolution=0.01, enable_events=True, disable_number_display=False)],
          [sg.Button('Iniciar simulaçao')],]
    
    win1 = sg.Window('EpiCom: Simulador de epidemia em comunidade (toy model)', layout_params)  
    win2_active=False

    while True:
        ev1, vals1 = win1.Read(timeout=100)  
        if ev1 is None:  
            win1.close()
            break

        global adiciona_casos
        global adiciona_mortos
        global adiciona_curados
        global p_desenv_sintomatica
        p_desenv_sintomatica=vals1["p_desenv_sintomatica"]/100
        global t_incubacao
        t_incubacao=int(vals1["t_incubacao"])*48
        global t_recuperacao
        t_recuperacao=int(vals1["t_recuperacao"])*48
        global p_morte
        p_morte=vals1["p_morte"]/(100*t_recuperacao)
        global raio
        raio=vals1["raio"]
        global p_assintomatico
        p_assintomatico=vals1["p_assintomatico"]/100
        global p_sintomatico
        p_sintomatico=vals1["p_sintomatico"]/100
        interacao=vals1["interacao"]
        p_transitar=vals1["p_transitar"]/48
        
        if ev1 == 'Iniciar simulaçao'  and not win2_active:  
            win2_active = True  
            
            cria_cidade(int(vals1["n_pessoas"]),int(vals1["n_trabalhos"]),
                    int(vals1["n_casas"]),int(vals1["sz_casa"]),
                        int(vals1["sz_trabalho"]),int(vals1["sz_cidade"]))

            n_infecta=int(vals1["n_pessoas"]*vals1["pc_infec"]/100)
            global total_casos
            total_casos.append(n_infecta)
            idx=list(range(len(pessoas)))
            random.shuffle(idx)

            while n_infecta>0:
                pessoas[idx[n_infecta]].status="sintomatico"
                pessoas[idx[n_infecta]].conta_cura=t_recuperacao
                n_infecta-=1
            casa_infectada=pessoas[idx[n_infecta]].casa
            trabalho_infectado=pessoas[idx[n_infecta]].trabalho
            
            tab1_layout = [[sg.Text('Visão aérea da comunidade (áreas comuns)', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS1-')],
              [sg.Button('Fechar', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]
            tab2_layout = [[sg.Text('Visão aérea de uma das casas', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS2-')],
              [sg.Button('Fechar', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]
            tab3_layout=[[sg.Text('Visão aérea de um dos locais de trabalho/escola', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS3-')],
              [sg.Button('Fechar', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]
            tab4_layout=[[sg.Text('Evolução do número de casos sintomáticos', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS4-')],
              [sg.Button('Fechar', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]
            tab5_layout=[[sg.Text('Evolução do número de mortos', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS5-')],
              [sg.Button('Fechar', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]
            tab6_layout=[[sg.Text('Evolução do número de curados', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS6-')],
              [sg.Button('Fechar', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]]
            layout = [[sg.TabGroup([[sg.Tab('Comunidade', tab1_layout, tooltip='tip'), sg.Tab('Casa', tab2_layout),
                sg.Tab('Local de trabalho/escola', tab3_layout),sg.Tab('Número de casos', tab4_layout),sg.Tab('Número de mortos', tab5_layout),
                sg.Tab('Número de curados', tab6_layout),]])]]
    
            win2 = sg.Window('Simulador', layout, finalize=True)

            canvas_elem1 = win2['-CANVAS1-']
            canvas1 = canvas_elem1.TKCanvas
            canvas_elem2 = win2['-CANVAS2-']
            canvas2 = canvas_elem2.TKCanvas
            canvas_elem3 = win2['-CANVAS3-']
            canvas3 = canvas_elem3.TKCanvas
            canvas_elem4 = win2['-CANVAS4-']
            canvas4 = canvas_elem4.TKCanvas
            canvas_elem5 = win2['-CANVAS5-']
            canvas5 = canvas_elem5.TKCanvas
            canvas_elem6 = win2['-CANVAS6-']
            canvas6 = canvas_elem6.TKCanvas

            fig1, ax1 = plt.subplots()
            fig2, ax2 = plt.subplots()
            fig3, ax3 = plt.subplots()
            fig4, ax4 = plt.subplots()
            fig5, ax5 = plt.subplots()
            fig6, ax6 = plt.subplots()
            ax1.grid(False)
            ax2.grid(False)
            ax3.grid(False)
            ax4.grid(False)
            ax5.grid(False)
            ax6.grid(False)
            fig_agg1 = draw_figure(canvas1, fig1)
            fig_agg2 = draw_figure(canvas2, fig2)
            fig_agg3 = draw_figure(canvas3, fig3)
            fig_agg4 = draw_figure(canvas4, fig4)
            fig_agg5 = draw_figure(canvas5, fig5)
            fig_agg6 = draw_figure(canvas6, fig6)

            while True:
                ev2, val2 = win2.read(timeout=1)
                if ev2 in ('Fechar', None):
                    win2.close()
                    win2_active=False
                    break
                
                dic_cidade={'g':[],'b':[],'y':[],'r':[],'c':[]}
                dic_casa={'g':[],'b':[],'y':[],'r':[],'c':[]}
                dic_trabalho={'g':[],'b':[],'y':[],'r':[],'c':[]}

                for i in range(len(pessoas)):
                    if pessoas[i].status!="morto":
                        pessoas[i].move(pessoas,interacao,t_recuperacao,p_transitar)
                
                infecta(pessoas,raio,p_assintomatico,p_sintomatico,t_incubacao)

                tempo.append(tempo[-1]+1/48)

                total_casos.append(total_casos[-1]+adiciona_casos)
                total_mortos.append(total_mortos[-1]+adiciona_mortos)
                total_curados.append(total_curados[-1]+adiciona_curados)
                adiciona_casos=0
                adiciona_mortos=0
                adiciona_curados=0

                ax1.cla()
                ax1.grid(False)
                ax2.cla()
                ax2.grid(False)
                ax3.cla()
                ax3.grid(False)
                ax4.cla()
                ax4.grid(False)
                ax5.cla()
                ax5.grid(False)
                ax6.cla()
                ax6.grid(False)

                for i in range(len(pessoas)):
                    if pessoas[i].status=="morto":
                        continue
                    if pessoas[i].localizacao=="cidade":
                        if pessoas[i].status=="nao infectado":
                            dic_cidade["g"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="incubado":
                            dic_cidade["b"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="assintomatico":
                            dic_cidade["y"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="sintomatico":
                            dic_cidade["r"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="curado":
                            dic_cidade["c"].append([pessoas[i].x,pessoas[i].y])
                    elif pessoas[i].casa==casa_infectada and pessoas[i].localizacao=="casa":
                        if pessoas[i].status=="nao infectado":
                            dic_casa["g"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="incubado":
                            dic_casa["b"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="assintomatico":
                            dic_casa["y"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="sintomatico":
                            dic_casa["r"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="curado":
                            dic_cidade["c"].append([pessoas[i].x,pessoas[i].y])
                    elif pessoas[i].localizacao=="trabalho" and pessoas[i].trabalho==trabalho_infectado:
                        if pessoas[i].status=="nao infectado":
                            dic_trabalho["g"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="incubado":
                            dic_trabalho["b"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="assintomatico":
                            dic_trabalho["y"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="sintomatico":
                            dic_trabalho["r"].append([pessoas[i].x,pessoas[i].y])
                        elif pessoas[i].status=="curado":
                            dic_trabalho["c"].append([pessoas[i].x,pessoas[i].y])

                ax1.scatter(coluna(dic_cidade["g"],0),coluna(dic_cidade["g"],1),c="g",alpha=0.3,label="não infectados",edgecolors='none')
                ax1.scatter(coluna(dic_cidade["b"],0),coluna(dic_cidade["b"],1),c="b",alpha=0.3,label="incubados",edgecolors='none')
                ax1.scatter(coluna(dic_cidade["y"],0),coluna(dic_cidade["y"],1),c="y",alpha=0.3,label="assintomáticos",edgecolors='none')
                ax1.scatter(coluna(dic_cidade["r"],0),coluna(dic_cidade["r"],1),c="r",alpha=0.3,label="sintomáticos",edgecolors='none')
                ax1.scatter(coluna(dic_cidade["c"],0),coluna(dic_cidade["c"],1),c="c",alpha=0.3,label="curados",edgecolors='none')
                ax1.legend(loc="upper right")
                ax2.scatter(coluna(dic_casa["g"],0),coluna(dic_casa["g"],1),c="g",alpha=0.3,label="não infectados",edgecolors='none')
                ax2.scatter(coluna(dic_casa["b"],0),coluna(dic_casa["b"],1),c="b",alpha=0.3,label="incubados",edgecolors='none')
                ax2.scatter(coluna(dic_casa["y"],0),coluna(dic_casa["y"],1),c="y",alpha=0.3,label="assintomáticos",edgecolors='none')
                ax2.scatter(coluna(dic_casa["r"],0),coluna(dic_casa["r"],1),c="r",alpha=0.3,label="sintomáticos",edgecolors='none')
                ax2.scatter(coluna(dic_casa["c"],0),coluna(dic_casa["c"],1),c="c",alpha=0.3,label="curados",edgecolors='none')
                ax2.legend(loc="upper right")
                ax3.scatter(coluna(dic_trabalho["g"],0),coluna(dic_trabalho["g"],1),c="g",alpha=0.3,label="não infectados",edgecolors='none')
                ax3.scatter(coluna(dic_trabalho["b"],0),coluna(dic_trabalho["b"],1),c="b",alpha=0.3,label="incubados",edgecolors='none')
                ax3.scatter(coluna(dic_trabalho["y"],0),coluna(dic_trabalho["y"],1),c="y",alpha=0.3,label="assintomáticos",edgecolors='none')
                ax3.scatter(coluna(dic_trabalho["r"],0),coluna(dic_trabalho["r"],1),c="r",alpha=0.3,label="sintomáticos",edgecolors='none')
                ax3.scatter(coluna(dic_trabalho["c"],0),coluna(dic_trabalho["c"],1),c="c",alpha=0.3,label="curados",edgecolors='none')
                ax3.legend(loc="upper right")
                ax4.plot(tempo,total_casos,c="r")
                ax5.plot(tempo,total_mortos,c="k")
                ax6.plot(tempo,total_curados,c="c")
                
                ax1.set_xlim((0,pessoas[0].sz_cidade))
                ax1.set_ylim((0,pessoas[0].sz_cidade))
                ax2.set_xlim((0,pessoas[0].sz_casa))
                ax2.set_ylim((0,pessoas[0].sz_casa))
                ax3.set_xlim((0,pessoas[0].sz_trabalho))
                ax3.set_ylim((0,pessoas[0].sz_trabalho))
                ax4.set_xlabel("Tempo (dias)")
                ax4.set_ylabel("Total de casos sintomáticos (cumulativo)")
                ax5.set_xlabel("Tempo (dias)")
                ax5.set_ylabel("Total de mortos (cumulativo)")
                ax6.set_xlabel("Tempo (dias)")
                ax6.set_ylabel("Total de curados (cumulativo)")
                

                fig_agg1.draw()
                fig_agg2.draw()
                fig_agg3.draw()
                fig_agg4.draw()
                fig_agg5.draw()
                fig_agg6.draw()
                
            win2.close()

if __name__ == '__main__':
    main()
