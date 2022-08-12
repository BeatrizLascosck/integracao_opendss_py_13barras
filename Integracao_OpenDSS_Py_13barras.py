
import py_dss_interface
dss = py_dss_interface.DSSDLL()


def modelo_padrao_Gerador():

    print('________________________________________________________________')
    print('\nANOMALIA DE REDE | MODELO DE GERADOR COMO APROXIMAÇÃO PARA UM PV')
    print('\nEm casos de anomalia de rede, usa-se um modelo de gerador como aproximação para um PV.\nSerá necessário entrar com alguns valores do Gerador modelado.\n')

    dss.text("New Transformer.Gen Phases=3 Windings=2   XHL=2")

    kVA = float(input('Digite o valor da potência aparente do gerador em kVA\n'))
    pf = float(input('Digite o valor do fator de potência\n'))
    Vminpu = float(input('Digite o valor da tensão mínima em pu\n'))

    dss.text(f'~ wdg=1 bus=Gerador   conn=wye    kv=4.16  kva={kVA}   %r=.5  XHT=1')
    dss.text(f'~ wdg=2 bus=671       conn=delta  kv=4.16  kva={kVA}  %r=.5   XLT=1')

    dss.text(f"New generator.PvGenerator basefreq=60 phases=3 kv=4.16 kva={kVA} pf={pf} bus1=Gerador model=7")
    dss.text(f"~ Vminpu={Vminpu} Conn=wye  Balanced=yes ")

#________________________________________________________________________________

def modelo_padrao_PVSystem():
    # SEM ANOMALIA
    # MODELO PADRÃO PVSYSTEM
    dss.text('New XYCurve.Eff npts=4 xarray=[.1 .2 .4 1.0] yarray=[1 1 1 1]')
    dss.text('New XYCurve.FatorPvsT npts=4 xarray=[0 25 75 100] yarray=[1 1 1 1]')

    dss.text('New Loadshape.Irrad npts=24 interval=1')
    dss.text('~ mult=[0 0 0 0 0 0 .1 .2 .3 .5 .8 .9 1.0 1.0 .99 .9 .7 .4 .1 0 0 0 0 0]')
    dss.text('New Tshape.Temp npts=24 interval=1')
    dss.text('~ temp=[25 25 25 25 25 25 25 25 35 40 45 50 60 60 55 40 35 30 25 25 25 25 25 25]')
    #____________________________________________________________
    #CONJUNTO DE 3 PVSYSTEM
    if modo_de_op <= 3:
        kvar = ' '
        PF = ' '
        kvar1 = ' '
        kvar2 = ' '
        kvar3 = ' '

    if modo_de_op == 4:
        kvar = ' '
        pf = float(input('Digite o valor do fator de potência constante\n'))
        PF = f' PF={pf} '
        kvar1 = ' '
        kvar2 = ' '
        kvar3 = ' '

    if modo_de_op == 5:
        kvar = ' '
        kvar1 = f' kvar=370.92'
        kvar2 = f' kvar=508.2'
        kvar3 = f' kvar=176'
        PF = ' PF=0.1 '

    dss.text(f'New PVSystem.PV1 phases=3 bus1=675{kvar1}{kvar}Pmpp=1000{PF}kV=4.16  KVA=843  conn=wye effcurve=Eff')
    dss.text("~ P-TCurve=FatorPvsT %Pmpp=100 irradiance=1 daily=Irrad Tdaily=Temp VarFollowInverter=true")

    dss.text(f"New PVSystem.PV2 phases=3 bus1=671{kvar2}{kvar}Pmpp=1000{PF}kV=4.16  KVA=1155  conn=wye effcurve=Eff")
    dss.text("~ P-TCurve=FatorPvsT %Pmpp=100 irradiance=1 daily=Irrad Tdaily=Temp VarFollowInverter=true")

    dss.text(f"New PVSystem.PV3 phases=3 bus1=634{kvar3}{kvar}Pmpp=1000{PF}kV=0.48  KVA=400  conn=wye effcurve=Eff")
    dss.text("~ P-TCurve=FatorPvsT %Pmpp=100 irradiance=1 daily=Irrad Tdaily=Temp VarFollowInverter=true")

    return
#________________________________________________________________________________

def usuario_voltvar_voltwatt_wattvar():
    V=[]
    Q=[]
    P=[]

    if modo_de_op == 1:  # VOLTVAR
        mode = 'VOLTVAR'
        npts= 5
        print(f'PREENCHA OS {npts} PONTOS DA CURVA DO MODO DE OPERAÇÃO {mode} DE ACORDO COM A ORDEM SOLICITADA')
        for i in range(npts):
            V.append(float(input(f'Digite o valor de V{i}\n')))
            Q.append(float(input(f'Digite o valor de Q{i}\n')))

        mode = 'VOLTVAR'
        valores = [npts] + Q + V + [mode]

    if modo_de_op == 2:  # VOLTWATT
        npts = 3
        mode = 'VOLTWATT'
        print(f'PREENCHA OS {npts} PONTOS DA CURVA DO MODO DE OPERAÇÃO {mode} DE ACORDO COM A ORDEM SOLICITADA')
        for i in range(npts):
            V.append(float(input(f'Digite o valor de V{i}\n')))
            P.append(float(input(f'Digite o valor de P{i}\n')))

        valores = [npts] + P + V + [mode]

    if modo_de_op == 3:  # WATTVAR
        npts = 4
        mode = 'WATTVAR'
        print(f'PREENCHA OS {npts} PONTOS DA CURVA DO MODO DE OPERAÇÃO {mode} DE ACORDO COM A ORDEM SOLICITADA')
        for i in range(npts):
            Q.append(float(input(f'Digite o valor de V{i}\n')))
            P.append(float(input(f'Digite o valor de P{i}\n')))

        valores = [npts] + Q + P + [mode]

    return valores
#________________________________________________________________________________

def default():
    if modo_de_op == 1 and categoria == 1:
        #default_VOLTVAR_Categoria_A()
        # valores = [npts]+ Q + V + [mode]
        # npts, Q1,Q2,...Qn, V1,V2,...Vn,mode
        valores = [5, 0.25, 0, 0, 0, -0.25, 0.9, 1, 1, 1, 1.1, 'VOLTVAR']  # Valores categoria A Tabela 8

    if modo_de_op == 1 and categoria == 2:
        #default_VOLTVAR_Categoria_B()
        # valores = [npts]+ Q + V + [mode]
        # npts, Q1,Q2,...Qn, V1,V2,...Vn,mode
        valores = [5, 0.44, 0, 0, 0, -0.44, 0.92, 0.98, 1, 1.02, 1.08, 'VOLTVAR']  # Valores categoria B Tabela 8

    if modo_de_op == 2:
        # VOLTWATT
        #default_voltwatt()
        valores = [3, 1, 0.2, 0.2, 1.06, 1.1, 1.1, 'VOLTWATT']  # Valores categoria A e B Tabela 10


    if modo_de_op == 3 and categoria == 1:
        # WATTVAR
        #default_WATTVAR_Categoria_A()

        valores = [4, 0, 0, 0, -0.25, 0, 0.2, 0.5, 1, 'WATTVAR']  # Valores categoria A Tabela 9

    if modo_de_op == 3 and categoria == 2:
        #default_WATTVAR_Categoria_B()
      #ABSORÇÃO
        valores = [4, 0, 0, 0, -0.44, 0, 0.2, 0.5, 1, 'WATTVAR']  # Valores categoria B Tabela 9

    return valores

def MONITORES_GD_PV():
    # MONITORES

    if Anomalia == 1: #Tem anomalia
        dss.text("New monitor.Generator_power element=generator.PvGenerator terminal=1 mode=1 ppolar=no")
        dss.text("New monitor.Generator_voltage element=generator.PvGenerator terminal=1 mode=0")

    if Anomalia == 2: #Não tem anomalia
        dss.text("New Monitor.PV_currents1 element=PVSystem.PV1 terminal=1 mode=0")
        dss.text("New Monitor.PV_powers1 element=PVSystem.PV1 terminal=1 mode=1 ppolar=no")
        dss.text("New Monitor.PV_v1 element=PVSystem.PV1 terminal=1 mode=3")


        dss.text("New Monitor.PV_currents2 element=PVSystem.PV2 terminal=1 mode=0")
        dss.text("New Monitor.PV_powers2 element=PVSystem.PV2 terminal=1 mode=1 ppolar=no")
        dss.text("New Monitor.PV_v2 element=PVSystem.PV2 terminal=1 mode=3")


        dss.text("New Monitor.PV_currents3 element=PVSystem.PV3 terminal=1 mode=0")
        dss.text("New Monitor.PV_powers3 element=PVSystem.PV3 terminal=1 mode=1 ppolar=no")
        dss.text("New Monitor.PV_v3 element=PVSystem.PV3 terminal=1 mode=3")

        dss.text("set maxcontroli = 2000")

def MEDIDOR_DE_ENERGIA():
    print('________________________________________________________________')
    print('\nMEDIDOR DE ENERGIA\n')
    line = input('Linha em que deseja posicionar o medidor de energia\nline.')
    terminal = input('Extremidade da linha que deseja monitorar\nterminal=')
    dss.text(f"New energymeter.medidor element=line.{line} terminal={terminal}")
    #energymeter
    dss.text(f"New monitor.linhamonitorada_power element=line.{line}  terminal={terminal}  mode=1 ppolar=no")
    dss.text(f"New monitor.linhamonitorada_voltage element=line.{line}  terminal={terminal}  mode=0")


def INVCONTROL():

    if modo_de_op == 1: #VOLTVAR
        # InvControl com um conjunto de 3 PV para VOLTVAR
        dss.text(f"New XYcurve.generic npts= {V[0]} yarray=[{V[1]} {V[2]} {V[3]} {V[4]} {V[5]}] xarray=[{V[6]} {V[7]} {V[8]} {V[9]} {V[10]}]")
        dss.text(f"New InvControl.VoltVar mode={V[11]} voltage_curvex_ref=rated vvc_curve1=generic")
        dss.text(f"~ deltaQ_factor=0.2 RefReactivePower=VARMAX varchangetolerance=0.0001")

    if modo_de_op == 2: #VOLTWATT
        # InvControl com um conjunto de 3 PV para VOLTWATT
        #npts = 3
        #mode = VOLTWATT
        dss.text(f"New XYcurve.generic npts= {V[0]} yarray=[{V[1]} {V[2]} {V[3]} ] xarray=[{V[4]} {V[5]} {V[6]}]")
        dss.text(f"New InvControl.VoltWatt mode={V[7]} voltage_curvex_ref=rated ")
        dss.text(f"~ voltwatt_curve=generic VoltwattYAxis=PMPPPU DeltaP_factor=0.45")

    if modo_de_op == 3:  # WATTVAR

        dss.text(f"New XYcurve.generic npts= {V[0]} yarray=[{V[1]} {V[2]} {V[3]} {V[4]} ] xarray=[{V[5]} {V[6]} {V[7]} {V[8]} ]")
        dss.text(f"New InvControl.WattVar mode={V[9]} wattvar_curve=generic refReactivepower=varmax")

#____________________________________________________________________________________________________________________________________________________________________________________________________________
#____________________________________________________________________________________________________________________________________________________________________________________________________________
#____________________________________________________________________________________________________________________________________________________________________________________________________________


print('________________________________________________________________________________________________________________')
print('PROGRAMA\n')
print('Este programa interage de forma objetiva com o OpenDSS,\nutiliza da Rede 13 Barras para aplicar o estudo \nde fluxo de potência ou de faltas na rede, conforme a escolha do usuário.')
print('________________________________________________________________________________________________________________')

print('________________________________________________________________________________________________________________')
print('ATENÇÃO\n')
print('Caso tenha aparecido erro na procura do arquivo de 13 barras, verifique se os arquivos estão presentes no diretório em que o programa localiza. \nSe não estiverem, mude-os e rode novamente o programa.\n ')
print('________________________________________________________________________________________________________________')


# REDE QUE SERÁ SUBMETIDA
dss.text("Redirect IEEE13Nodeckt.dss")
#___________________________________________________
#CONDIÇÕES DE ANOMALIA?
Anomalia=int(input('\nDIGITE\n 1 para "Estudo de aplicação de faltas | Anomalia de rede"\n 2 para "Estudo de modos de operação | Condições normais de operação"\n'))

if Anomalia == 1:
    modelo_padrao_Gerador()

else:
    if Anomalia == 2:
        print('________________________________________________________________')
        print('MODOS DE OPERAÇÃO')
        modo_de_op = int(input('\nDIGITE\n 1 para "Tensão - Potência Reativa | VOLTVAR"\n 2 para "Tensão - Potência Ativa | VOLTWATT"\n 3 para "Potência Ativa - Potência Reativa | WATTVAR"\n 4 para "Fator de Potência Constante | FP CONSTANTE"\n 5 para "Potência Reativa Constante | KVAR CONSTANTE"\n'))

        modelo_padrao_PVSystem()

        if modo_de_op <= 3:
            if modo_de_op == 1:  # VOLTVAR
                escolher = int(input('DIGITE\n 1 para "Entrar com valores da curva"\n 2 para "Utilizar valores padrões da norma IEEE 1547-2018 desse modo de operação"\n'))
                if escolher == 1:
                    V = usuario_voltvar_voltwatt_wattvar()
                if escolher == 2:
                    categoria = int(input('DIGITE\n 1 para "Utilizar valores padrões da Categoria A"\n 2 para "Utilizar valores padrões da Categoria B"\n'))
                    V = default()

            if modo_de_op == 2:  # VOLTWATT
                escolher = int(input('DIGITE\n 1 para "Entrar com valores da curva"\n 2 para "Utilizar valores padrões da norma IEEE 1547-2018 desse modo de operação"\n'))
                if escolher == 1:
                    V = usuario_voltvar_voltwatt_wattvar()
                if escolher == 2:
                    V = default()

            if modo_de_op == 3:  # WATTVAR
                escolher = int(input('DIGITE\n 1 para "Entrar com valores da curva"\n 2 para "Utilizar valores padrões da norma IEEE 1547-2018 desse modo de operação"\n'))
                if escolher == 1:
                    V = usuario_voltvar_voltwatt_wattvar()
                if escolher == 2:
                    categoria = int(input('DIGITE\n 1 para "Utilizar valores padrões da Categoria A"\n 2 para "Utilizar valores padrões da Categoria B"\n'))
                    V = default()

            INVCONTROL()

# _________________________________________________________________________

MONITORES_GD_PV()

# _________________________________________________________________________

print('________________________________________________________________')
print('Deseja posicionar um medidor de energia em uma linha específica da rede?')
energymeter = int(input('\nDIGITE\n 1 para "SIM"\n 2 para "NÃO"\n'))
if energymeter == 1:
    MEDIDOR_DE_ENERGIA()

# _________________________________________________________________________

# _________________________________________________________________________
if Anomalia == 1:
    n_falta = int(input('\nEscolha qual tipo de falta deseja efetuar\nDIGITE\n 1 para "Monofásica"\n 2 para "Bifásica"\n 3 para "Trifásica"\n'))
    bus1= str(input('Barra em que deseja aplicar a falta\n bus1='))
    dss.text(f'New Fault.{n_falta}Fcurto phases={n_falta} bus1={bus1} bus2=680.0.0.0 r=0.5 enable=no')

    dss.text('solve mode=dynamics stepsize=0.01667 number=100')
    dss.text(f'Fault.{n_falta}Fcurto.enable=yes')
    dss.text(f'solve number=100')
    dss.text(f'Fault.{n_falta}Fcurto.enable=no')
    dss.text('solve number=100')

if Anomalia == 2:
    dss.text('set mode=daily')
    dss.text('set stepsize=1h')
    dss.text('set number=24')

dss.text("Solve")
dss.text("BusCoords   IEEE13Node_BusXY.csv")


if Anomalia == 1:
    dss.text('Plot monitor object= generator_power channels=(1 3 5 )')
    dss.text('Plot monitor object= generator_power channels=(2 4 6 )')
    dss.text('Plot monitor object= generator_voltage channels=(9 11 13)')

else:
    if Anomalia == 2:
        print('________________________________________________________________')
        print('Deseja plotar os gráficos referentes as quais PVs')
        plotar_PV = int(input('\nDIGITE\n 1 para "Apenas do PV2"\n 2 para "Todos os PVs"\n'))
        if plotar_PV == 1:
            dss.text(f'Plot monitor object= pv_powers2 channels=(1 3 5 )')
            dss.text(f'Plot monitor object= pv_powers2 channels=(2 4 6 )')
            dss.text(f'Plot monitor object= pv_currents2 channels=(1 3 5)')
            dss.text(f'Plot monitor object= pv_v2 channels=(1)')

        if plotar_PV == 2:
            for n in range(3):
                dss.text(f'Plot monitor object= pv_powers{n+1} channels=(1 3 5 )')
                dss.text(f'Plot monitor object= pv_powers{n+1} channels=(2 4 6 )')
                dss.text(f'Plot monitor object= pv_currents{n+1} channels=(9 11 13)')
                dss.text(f'Plot monitor object= pv_currents{n+1} channels=(1 3 5)')
                dss.text(f'Plot monitor object= pv_v{n+1} channels=(7)')

        if energymeter == 1:
            dss.text(f'Plot monitor object= linhamonitorada_power channels=(1 3 5)')
            dss.text(f'Plot monitor object= linhamonitorada_power channels=(2 4 6)')
            dss.text(f'Plot monitor object= linhamonitorada_voltage channels=(2 4 6)')

# =====================================================================================================