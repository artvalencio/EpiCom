# EpiCom
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
