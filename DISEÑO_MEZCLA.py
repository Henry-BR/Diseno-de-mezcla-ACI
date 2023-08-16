    #DATOS RESISTENCIA
lista = [175,
         210,
         245]
for i in lista:
    fc_base = i#float(input("f'c Solicitado: "))
        #DATOS CEMENTO
    I = 3080
    ICO = 2940
    MS = 2960
    cemento_fabrica = "NACIONAL"
    tmn_tex = "1_2"
    cemento_peso_especifico = ICO #float(input("Ingrese el peso específico del cemento: "))
    tipo = "ICo"

        #DATOS AGREGADO FINO
    af_MF = 2.978#float(input("Ingresa el MF del agregado fino: "))
    af_humedad = 0.95#float(input("Ingresa la humedad del agregado fino (%): "))
    af_absorcion = 1.46#float(input("Ingresa la absorción del agregado fino (%): "))
    af_peso_especifico = 2374#float (input("Ingresa el peso especifico del agregado fino (kg/m3): "))
    af_peso_suelto = 1641#float(input("Ingresa el peso seco suelto del agregado fino (kg/m3): "))
    af_peso_compactado = 1877#float (input("Ingresa el peso seco compactado del agregado fino (kg/m3): "))

        #DATOS AGREGADO GRUESO
    ag_MF = 6.92#float(input("Ingresa el MF del agregado grueso: "))
    TMN= "1/2"#input("Ingrese el TMN del agregado grueso (plg): ")
    ag_humedad = 0.77#float(input("Ingresa la humedad del agregado grueso (%): "))
    ag_absorcion = 1.08#float(input("Ingresa la absorción del agregado grueso (%): "))
    ag_peso_especifico =2341.33 #float (input("Ingresa el peso específico del agregado grueso (kg/m3): "))
    ag_peso_suelto = 1491.74#float(input("Ingresa el peso seco suelto del agregado grueso (kg/m3): "))
    ag_peso_compactado = 1552.47#float (input("Ingresa el peso seco compactado del agregado grueso (kg/m3): "))

    #1.- Cálculo del f'c requerido
    def calcular_fc_required(fc_base):
        fc_required = 0
        sumado = 0
        if fc_base <210:
            fc_required = fc_base+70
            sumado =70
        elif 210<=fc_base<350:
            fc_required = fc_base+85
            sumado = 85
        elif fc_base>=350:
            fc_required = fc_base*1.1+50
            fc_required = round(fc_required,2)
            sumado = 50
        return (fc_required, sumado)

    fc_required, sumado = calcular_fc_required(fc_base)

    # 2.- Selección del tamaño máximo nominal del agregado
    #TMN= input("Ingrese el TMN del agregado en plg: ")

    # 3.- Selección del asentamiento (slump)
    slump = "4"#input("Ingrese el Slump deseado en plg: ")
    slump_int = int(slump)

    # 4.- Determinar el contenido de aire atrapado
    trapped_air_dict = {"3/8": 0.03, "1/2": 0.025, "3/4": 0.02, "1": 0.015, "1 1/2": 0.01, "2": 0.005, "3": 0.003, "6": 0.002}
    trapped_air = trapped_air_dict.get(TMN, 0)

    # 5.- Determinar el contenido de agua
    import pandas as pd

    water_content_table = pd.DataFrame({"3/8":[207,228,243],"1/2":[199,216,228],"3/4":[190,205,216],"1":[179,193,202],
                                        "1 1/2":[179,193,202], "2":[154,169,178],"3":[130,145,160],"6":[113,124,0]},
                                        index = ["1 a 2", "3 a 4", "5 a 6"])
    slump_dict = {1: "1 a 2", 2: "1 a 2", 3: "3 a 4", 4: "3 a 4", 5: "5 a 6", 6: "5 a 6"}
    slump_str = slump_dict.get(slump_int, "Valor no válido")
    agua = water_content_table.loc[slump_str,TMN]
    agua_m3 = agua/1000

    # 6.- Para el calculo del a/c
    import numpy as np
    fc_array = np.array([140, 150, 200, 210, 250, 280, 300, 350, 400, 420, 450])
    air_array = np.array([0.82, 0.8, 0.7, 0.68, 0.62, 0.57, 0.55, 0.48, 0.43, 0.41, 0.38])
    def interpolar (a , b , c):
        relacion_a_c = np.interp(a , b , c)
        return relacion_a_c

    # 7.- Para el calculo del cemento
    cemento = agua/interpolar(fc_required , fc_array , air_array)
    cemento_kg = round(cemento,2)
    cemento_bls = round(cemento_kg /42.5,2)
    cemento_m3 = round(cemento_kg/cemento_peso_especifico,3)

    # 8.-  CALCULO PARA LOS AGREGADOS
    def calcular_array_b_b0(a):
        valores = {3/8: 0.50,"1/2": 0.61,"3/4": 0.68,"1": 0.73,
                    "1 1/2": 0.78,"2": 0.80,"3": 0.83,"6": 0.89}
        lista_mf = [2.40, 2.60, 2.80, 3.00]
        array_b_bo = [valores[a] - (i + 1) * 0.02 for i in range(4)]
        b_bo = np.interp(af_MF,lista_mf,array_b_bo)
        return b_bo
    ag_seco = round(calcular_array_b_b0(TMN) * ag_peso_compactado,2)
    ag_seco_volumen = round(ag_seco/ag_peso_especifico,3)

    af_seco_volumen = round(1-cemento_m3-ag_seco_volumen-agua_m3-trapped_air,3)
    af_seco = round(af_seco_volumen * af_peso_especifico,2)

    # 9.- CALCULO PARA CORRECIÓN DE HUMEDAD
    # 9.1.- CALCULO PARA EL AGREGADO FINO
    peso_humedo_af = round(af_seco*(1+af_humedad/100),2)
    # 9.2.- CALCULO PARA EL AGREGADO GRUESO
    peso_humedo_ag = round(ag_seco*(1+ag_humedad/100),2)

    # 10.- CALCULO DE AGUA EFETIVA
    # 10.1.- CALCULO PARA EL AGREGADO FINO
    aporte_agua_af = af_seco*(af_humedad/100-af_absorcion/100)
    # 10.2.- CALCULO PARA EL AGREGADO GRUESO
    aporte_agua_ag = ag_seco*(ag_humedad/100-ag_absorcion/100)
    # 10.3.- APORTE TOTAL DE AGUA
    aporte_agua_total = aporte_agua_af + aporte_agua_ag
    # 10.4.- CALCULO DE AGUA CORREGIDA
    def corregida_agua(agua, aporte_agua_total):
        if aporte_agua_total >=0:
            a = agua - aporte_agua_total
            return round(a,2)
        else:
            a = agua + aporte_agua_total
            return round(a,2)
    agua_corregida = corregida_agua(agua, aporte_agua_total)
    agua_corregida_m3 = round(agua_corregida/1000,3)

    # 11.- CALCULO DE LA DOSIFICACIÓN EN PESO
    dosificacion_peso_cemento = round(cemento_kg/cemento_kg,2)
    dosificacion_peso_af = round(peso_humedo_af/cemento_kg,2)
    dosificacion_peso_ag = round(peso_humedo_ag/cemento_kg,2)
    dosififacion_agua = round(agua_corregida/cemento_bls,2)

    # 12.- CALCULO DE LA DOSIFICACIÓN EN VOLÚMEN
    # 12.1.- AGREGADOS POR BOLSA DE CEMENTO
    af_por_bolsa_cemento = round(dosificacion_peso_af*42.50,2)
    ag_por_bolsa_cemento = round(dosificacion_peso_ag*42.50,2)
    cemento_por_bolsa_cemento = round(42.50,2)
    # 12.2.- AGREGADOS EN KG POR PIE CÚBICO
    af_kg_por_metro_cubico = round(af_peso_suelto*(1+af_humedad/100),2)
    af_kg_por_pie_cubico = round(af_kg_por_metro_cubico/35.315,2)
    ag_kg_por_metro_cubico = round(ag_peso_suelto*(1+ag_humedad/100),2)
    ag_kg_por_pie_cubico = round(ag_kg_por_metro_cubico/35.315,2)
    # 12.3.- DOSIFICACIÓN EN VOLÚMEN
    dosificacion_volumen_cemento = round(42.50/42.50,2)
    dosificacion_volumen_af = round(af_por_bolsa_cemento/af_kg_por_pie_cubico,2)
    dosificacion_volumen_ag = round(ag_por_bolsa_cemento/ag_kg_por_pie_cubico,2)

    # 13.- CANTIDAD DE MATERIALES POR METRO CÚBICO DE CONCRETO
    material_m3_af_volumen = round(peso_humedo_af/af_kg_por_metro_cubico,3)
    material_m3_ag_volumen = round(peso_humedo_ag/ag_kg_por_metro_cubico,3)
    material_m3_agua_volumen = round(agua_corregida/1000,3)


    # 14.- CANTIDAD DE MATERIALES PARA UN TESTIGO DE CONCRETO
    from math import pi
    v_testigo = pi*(0.15**2)/4*0.3
    testigo_cemento_bls = round(cemento_bls*v_testigo,3)
    testigo_cemento_kg = round(cemento_kg*v_testigo,3)

    testigo_af_m3 = round(material_m3_af_volumen*v_testigo,3)
    testigo_af_kg = round(peso_humedo_af*v_testigo,3)

    testigo_ag_m3 = round(material_m3_ag_volumen*v_testigo,3)
    testigo_ag_kg = round(peso_humedo_ag*v_testigo,3)

    testigo_agua = round(material_m3_agua_volumen*v_testigo,3)

    from fpdf import FPDF

    #CREAR PDF
    doc = FPDF(orientation='P', unit ='mm', format='A4')

    #DECLARAMOS LA PAGINA
    doc.add_page()

    #DEFINIMOS EL TIPO Y TAMAÑO DE TEXTO
    doc.set_font('Courier', 'BU', 14)

    #CALCULO DE ANCHO DEL TEXTO PARA CENTRAR
    texto_ancho = doc.get_string_width(f"DISEÑO DE MEZCLA DE CONCRETO {fc_base}kg/cm\u0032 - MÉTODO ACI")
    pos_x = (doc.w - texto_ancho) / 2

    #COLOCAMOS EL TEXTO EN EL PDF
    doc.text(x=pos_x, y=20, txt=f"DISEÑO DE MEZCLA DE CONCRETO {fc_base}kg/cm\u0032 - MÉTODO ACI")

    #COLOCAMOS LA IMAGEN
    #doc.image("Y:/Downloads/bob.jpg", x=150, y=25, w=50, h=80)

    #DATOS
    doc.set_font('Courier', 'BU', 12)
    doc.text(x=20, y= 28, txt="DATOS PARA EL DISEÑO:")
    doc.text(x=22, y= 36, txt="CEMENTO")
    doc.text(x=22, y= 60, txt="AGREGADO GRUESO")
    doc.text(x=22, y= 124, txt="AGREGADO FINO")
    doc.text(x=22, y= 180, txt="ADITIVOS")

    #PARA EL CEMENTO
    doc.set_font('Courier', '', 12)
    doc.text(x=24, y= 44, txt=f"Tipo                          :    {tipo} - {cemento_fabrica}")
    doc.text(x=24, y= 52, txt=f"Peso específico               :    {cemento_peso_especifico}kg/m\u00B3")

    #PARA EL AGREGADO GRUESO
    doc.text(x=24, y= 68, txt=f'TMN                           :    {TMN}"')
    doc.text(x=24, y= 76, txt=f"Módulo de fineza              :    {ag_MF}")
    doc.text(x=24, y= 84, txt=f"Porcentaje de humedad         :    {ag_humedad}%")
    doc.text(x=24, y= 92, txt=f"Porcentaje de absoción        :    {ag_absorcion}%")
    doc.text(x=24, y= 100,txt=f"Peso específico               :    {ag_peso_especifico}kg/m\u00B3")
    doc.text(x=24, y= 108,txt=f"Peso unitario seco suelto     :    {ag_peso_suelto}kg/m\u00B3")
    doc.text(x=24, y= 116,txt=f"Peso unitario seco compactado :    {ag_peso_compactado}kg/m\u00B3")

    #PARA EL AGREGADO fINO
    doc.text(x=24, y= 132,txt=f"Módulo de fineza              :    {af_MF}")
    doc.text(x=24, y= 140,txt=f"Porcentaje de humedad         :    {af_humedad}%")
    doc.text(x=24, y= 148,txt=f"Porcentaje de absoción        :    {af_absorcion}%")
    doc.text(x=24, y= 156,txt=f"Peso específico               :    {af_peso_especifico}kg/m\u00B3")
    doc.text(x=24, y= 164,txt=f"Peso unitario seco suelto     :    {af_peso_suelto}kg/m\u00B3")
    doc.text(x=24, y= 172,txt=f"Peso unitario seco compactado :    {af_peso_compactado}kg/m\u00B3")

    #ADITIVOS
    doc.text(x=24, y= 188,txt=f"Aditivo retardante            :   SIN DATOS ")
    doc.text(x=24, y= 196,txt=f"Aditivo acelerante            :   SIN DATOS ")
    doc.text(x=24, y= 204,txt=f"Aditivo plastificante         :   SIN DATOS ")
    doc.text(x=24, y= 212,txt=f"Aditivo superplastificantes   :   SIN DATOS ")
    doc.text(x=24, y= 220,txt=f"Aditivo incorporador de aire  :   SIN DATOS ")

    doc.add_page()

    #Titulo del procedimiento de calculos
    doc.set_font('Courier', 'BU', 14)
    doc.text(x=pos_x, y=20, txt="PROCEDIMIENTO DE LOS CALCULOS")

    #PARA TITULOS DE LOS CALCULOS
    doc.set_font('Courier', 'B', 12)
    doc.text(x=20, y= 28, txt="f'c requerido: ")
    doc.text(x=20, y= 44, txt="TMN: ")
    doc.text(x=20, y= 60, txt="Slump : ")
    doc.text(x=20, y= 76, txt="Contenido de aire: ")
    doc.text(x=20, y= 92, txt="Contenido de agua: ")
    doc.text(x=20, y= 108, txt="Relación agua acemento (a/c): ")
    doc.text(x=20, y= 124, txt="Cemento a usar en kg y bls: ")
    doc.text(x=20, y= 148, txt="AGREGADOS")
    doc.text(x=24, y= 156,txt="Condiciones secas")
    doc.text(x=20, y= 204,txt="Condiciones húmedas")


    #PARA LOS PASOS
    doc.set_font('Courier', '', 12)
    paso1 = str
    #PASO 1
    if fc_base>350:
        paso1 = f"f'cr = (1.1 x {fc_base}kg/cm\u00B2) + {sumado}kg/cm\u00B2 = {fc_required}kg/cm\u00B2"
    else:
        paso1 = f"f'cr = {fc_base}kg/cm\u00B2 + {sumado}kg/cm\u00B2 = {fc_required}kg/cm\u00B2"
    doc.text(x=24, y= 36,txt=paso1)

    #PASO 2
    doc.text(x=24, y= 52,txt=f"TMN = {TMN} plg")

    #PASO 3
    doc.text(x=24, y= 68,txt=f"Slump = {slump} plg")

    #PASO 4
    doc.text(x=24, y= 84,txt=f"Contenido de aire atrapado = {trapped_air*100} %")

    #PASO 5
    doc.text(x=24, y= 100,txt=f"Volumen de agua: {agua} lts ")

    #PASO 6
    doc.text(x=24, y= 116,txt=f"La relación a/c es {round(interpolar(fc_required , fc_array , air_array),3)} ")

    #PASO 7
    doc.text(x=24, y= 132,txt=f"La cantidad de cemento es {cemento_kg} kg")
    doc.text(x=24, y= 140,txt=f"La cantidad de cemento es {cemento_bls} bls")

    #PASO 8

    doc.text(x=24, y= 164,txt=f"- Cemento: {cemento_kg} kg - {cemento_m3} m\u00B3")
    doc.text(x=24, y= 172,txt=f"- Agua: {agua} lts - {agua_m3} m\u00B3")
    doc.text(x=24, y= 180,txt=f"- Aire: {trapped_air*100} % - {trapped_air} m\u00B3")
    doc.text(x=24, y= 188,txt=f"- Agregado grueso: {ag_seco} kg - {ag_seco_volumen} m\u00B3")
    doc.text(x=24, y= 196,txt=f"- Agregado fino: {af_seco} kg - {af_seco_volumen} m\u00B3")

    #PASO 9
    doc.text(x=24, y= 212,txt=f"- Cemento: {cemento_kg} kg")
    doc.text(x=24, y= 220,txt=f"- Agua: {agua_corregida} lts")
    doc.text(x=24, y= 228,txt=f"- Agregado grueso: {peso_humedo_ag} kg")
    doc.text(x=24, y= 236,txt=f"- Agregado fino: {peso_humedo_af} kg")

    #AGREGAMOS UNA PAGINA
    doc.add_page()
    doc.set_font('Courier', 'B', 12)
    doc.text(x=20, y= 20,txt="Dosificación en peso")
    doc.text(x=20, y= 44,txt="Dosificación en volumen")
    doc.text(x=20, y= 68,txt="Materiales por m\u00B3 de concreto")
    doc.text(x=20, y= 108,txt="Materiales para un testigo de concreto + 15% DE DESPERDICIO")
    doc.set_font('Courier', '', 12)

    #PASO 10
    doc.text(x=24, y= 28,txt="   C    :   AF   :   AG   /  AGUA   ")
    doc.text(x=24, y= 36,txt=f"   {dosificacion_peso_cemento}  :  {dosificacion_peso_af}  :  {dosificacion_peso_ag}  /  {dosififacion_agua}   ")

    #PASO 11
    doc.text(x=24, y= 52,txt="   C    :   AF   :   AG   /  AGUA   ")
    doc.text(x=24, y= 60,txt=f"   {dosificacion_volumen_cemento}  :  {dosificacion_volumen_af}  :  {dosificacion_volumen_ag}  /  {dosififacion_agua}   ")

    #PASO 12
    doc.text(x=24, y= 76,txt=f"- Cemento: {cemento_kg} kg - {cemento_bls} bls")
    doc.text(x=24, y= 84,txt=f"- Agregado fino: {peso_humedo_af} kg - {material_m3_af_volumen} m\u00B3")
    doc.text(x=24, y= 92,txt=f"- Agregado grueso: {peso_humedo_ag} kg - {material_m3_ag_volumen} m\u00B3")
    doc.text(x=24, y= 100,txt=f"- Agua: {agua_corregida} lts - {material_m3_agua_volumen} m\u00B3")

    #PASO 13
    doc.text(x=24, y= 116,txt=f"- Cemento: {round(testigo_cemento_kg*1.15,5)} kg - {round(testigo_cemento_bls*1.15,5)} bls - {round(v_testigo,5)}" )
    doc.text(x=24, y= 124,txt=f"- Agregado fino: {round(testigo_af_kg*1.15,5)} kg - {round(testigo_af_m3*1.15,5)} m\u00B3")
    doc.text(x=24, y= 132,txt=f"- Agregado grueso: {round(testigo_ag_kg*1.15,5)} kg - {round(testigo_ag_m3*1.15,5)} m\u00B3")
    doc.text(x=24, y= 140,txt=f"- Agua: {round(testigo_agua*1000*1.15,5)} lts - {round(testigo_agua*1.15,5)} m\u00B3")

    #GUARDAR PDF
    doc.output(f'Y:/Downloads/Documents/DISEÑO_{fc_base}_TMN_{tmn_tex}_{cemento_fabrica}_{tipo}.pdf')
    '''import pandas as pd
    data = pd.read_excel("Z:\TESIS - PYTHON\Formato_datos.xlsx",sheet_name="ENTRENAMIENTO")
    cantidad_cemento = []
    for i in range(100):
        data["Cantidad cemento"]=[20,20,10,10,20]
    data.to_excel('data_modificado.xlsx', index=False)'''
