# -*- coding: utf-8 -*-
import os
import shutil as sh
import subprocess
import time
import csv

class Document:

    def __init__(self, tituloDoc, lugar_geografico, ruta_salida, anio = 2014):
        self.titulo_documento = tituloDoc
        self.lugar_geografico = lugar_geografico
        self.ruta_salida = ruta_salida
        self.anio_evento = anio
        self.no_capitulos = []
        self.capitulos = []
        self.titulo_seccion = []
        self.descripcion = []
        self.titulo_grafica = []
        self.desagregacion_grafica = []
        self.grafica = []
        self.fuente = []
        self.tipo_descriptor = []
        self.incluir_presentacion = []

    def crear_directorio(self):
        try:
            os.makedirs(self.ruta_salida)
        except OSError:
            print "El directorio ya existe"

    def copiar_utilidades(self):
        errors = []
        src = os.path.join(os.getcwd(),"Utilidades")
        names = os.listdir( src )
        for name in names:
            srcname = os.path.join(src , name )
            dstname = os.path.join(self.ruta_salida, name)
            try:
                sh.copy(srcname, dstname)
            except (IOError, os.error) as why:
                errors.append((srcname, dstname, str(why)))
            except Error as err:
                errors.extend(err.args[0])

    def crear_documento(self):
        self.ruta_compilacion = self.ruta_salida.strip().replace(" ", "\\ ")
        self.documento = open( os.path.join( self.ruta_salida,
        self.titulo_documento + '.tex' ), 'w+' )
        self.documento.write('%Creado de manera automática en ' + time.strftime("%x")
        + " a las " + time.strftime("%X") + '\n')
        self.documento.write('\\input{Carta3.tex} \n')
        self.documento.write('\\renewcommand{\partes}{} \n')
        self.documento.write('\\renewcommand{\\titulodoc}{ ' +
        self.titulo_documento + '}\n')
        self.documento.write( '\\newcommand{\\ra}[1]{\\renewcommand{\\arraystretch}{#1}} \n' )
        self.documento.write( '\\definecolor{color1}{rgb}{0,0,0.8} \n' +
        '\\definecolor{color2}{rgb}{0.3,0.5,1} \n' )
        self.documento.write('\\begin{document} \n' )
        self.documento.write('\\tableofcontents')

    def crear_presentacion(self):
        self.presentacion = open( os.path.join( self.ruta_salida,
        self.titulo_documento + '-Presentacion.tex' ), 'w+' )
        self.presentacion.write('%Creado de manera automática en ' + time.strftime("%x")
        + " a las " + time.strftime("%X") + '\n')
        self.presentacion.write('\\input{Presentacion.tex} \n')
        self.presentacion.write('\\begin{document} \n' )


    def crear_cajita(self, titulo,descripcion, titulo_grafica,
        des_grafica, grafica, fuente):
        cajita = '\\cajita{% \n' \
        + titulo + ' % \n' \
        + '}% \n' \
        + '{% \n' \
        + descripcion +  ' % \n' \
        + '}% \n' \
        + '{% \n'\
        + titulo_grafica + ' % \n' \
        + '}% \n' \
        + '{% \n ' \
        + des_grafica + ' % \n' \
        + '}% \n' \
        + '{% \n ' \
        + grafica +' % \n' \
        + '}% \n' \
        + '{% \n' \
        + fuente + ' % \n' \
        + '} \n'
        return cajita

    def crear_capitulo(self,nombre_cap, descripcion_cap):
        capitulo = "\\INEchaptercarta{" + nombre_cap \
        +"}{" + descripcion_cap + "} "
        return capitulo

    def escribir_en_doc(self, texto):
        self.documento.write( '\n \n ' + texto + '\n \n' )

    def escribir_en_presentacion(self, texto):
        self.presentacion.write( '\n \n ' + texto + '\n \n' )

    def terminar_documento(self):
        self.escribir_en_doc('\\end{document}'.encode('utf-8'))
        self.documento.close()


    def terminar_presentacion(self):
        self.escribir_en_presentacion('\\end{document}'.encode('utf-8'))
        self.presentacion.close()


    def compilar_documento(self):
        cadena_compilacion = "cd "+ self.ruta_compilacion + " && xelatex " + self.titulo_documento.strip().replace(" ", "\\ ") + ".tex"
        print cadena_compilacion
        print subprocess.Popen(cadena_compilacion, shell=True, stdout=subprocess.PIPE).stdout.read()

    def compilar_presentacion(self):
        cadena_compilacion = "cd "+ self.ruta_compilacion + " && xelatex " + self.titulo_documento.strip().replace(" ", "\\ ") + "-Presentacion.tex"
        print cadena_compilacion
        print subprocess.Popen(cadena_compilacion, shell=True, stdout=subprocess.PIPE).stdout.read()

    def crear_cadena_descriptor(self,formato,tipo):
        archivo = open(os.path.join(self.ruta_salida, 'descripciones',formato + '.tex'), 'w')
        archivo.write('%Dummy file')
        archivo.close()
        if tipo.strip().upper() == "CUADRO":
                tex = os.path.isfile( os.path.join(self.ruta_salida, 'graficas',formato + '.tex') )
                pdf = False
        else:
            tex = os.path.isfile( os.path.join(self.ruta_salida, 'graficas',formato + '.tex') )
            pdf = os.path.isfile( os.path.join(self.ruta_salida,'graficas', formato + '.pdf') )
        retorno = ''
        if not tex or pdf:
            try:
                os.makedirs( os.path.join(self.ruta_salida,'graficas') )
            except OSError:
                print "El directorio de graficas ya existe"
            try:
                os.makedirs( os.path.join(self.ruta_salida,'cuadros') )
            except OSError:
                print "El directorio de cuadros ya existe"
            try:
                if tipo.strip().upper() == "CUADRO":
                    archivo = open(os.path.join(self.ruta_salida, 'cuadros',formato + '.tex'), 'w')
                    archivo.write('%Dummy file')
                else:
                    archivo = open(os.path.join(self.ruta_salida, 'graficas',formato + '.tex'), 'w')
                    archivo.write('%Dummy file')
            except ValueError:
                print 'Una excepcion', ValueError
                pass
        if tipo.strip().upper() == "CUADRO":
            retorno = '\\input{cuadros/' + formato + '.tex}'
        else:
            if pdf:
                retorno = '\\includepdf{' + formato + '.pdf' + '}'
            else:
                retorno = '\\begin{tikzpicture}[x=1pt,y=1pt]\\input{graficas/' + formato + '.tex}' + '\\end{tikzpicture}'
        return retorno

    def leer_csv(self, ruta):
        archivo = open(ruta, 'rb')
        lector =  csv.reader(archivo,  delimiter=';')
        salida = []
        for row in lector:
            salida.append(row)
        return salida

    def crear_carpeta_descripciones(self):
        try:
            os.makedirs( os.path.join(self.ruta_salida, 'descripciones') )
        except OSError:
            print "El directorio ya existe"

    def des_102(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','1_02.csv'))
        des = 'Saber cuál es la población de un departamento' \
        +' es fundamental para el diseño de políticas públicas, ya que este dato representa el ' \
        +'universo de los potenciales usuarios de los distintos programas y' \
        +' proyectos implementados por el Gobierno a nivel departamental. \n\n ' \
        +' Se estima que en 2014 el departamento de ' + self.lugar_geografico + ' tenía ' + self.formato_bonito(datos[3][1]) \
        +' habitantes; este dato representa un ' + self.cambio(datos[3][1], datos[2][1]) \
        +' del ' + self.porcentaje(datos[3][1], datos[2][1]) + '\\% respecto de la población estimada para 2011.' \
        + ' Para el 2006, la Encovi estimó que la población de este departamento ascendía a '+  self.formato_bonito(datos[1][1])
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','1_02.tex'), 'w')
        archivo.write(des)

    def des_104(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','1_04.csv'))
        des = 'La densidad poblacional relaciona el número de habitantes con el tamaño del territorio donde esta población habita. Normalmente este indicador se expresa en personas por kilómetro cuadrado. \n \n'\
        +' En 2014 la densidad poblacional de ' + self.lugar_geografico +  ' era de ' \
        +self.formato_bonito(datos[3][1]) + ' habitantes por kilómetro cuadrado; este dato es ' \
        +self.mayor_menor(datos[3][1],datos[1][1]) + ' que el estimado para 2006, el cual ascendía a  ' \
        + self.formato_bonito(datos[1][1]) + ' habitantes por kilómetro cuadrado.'

        archivo = open( os.path.join(self.ruta_salida, 'descripciones','1_04.tex'), 'w')
        archivo.write(des)

    def des_106(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','1_06.csv'))
        des = 'Para el 2014, la Encovi estima que el ' + self.formato_bonito(datos[2][2]) \
        +'\\% de la población del departamento de ' + self.lugar_geografico \
        + ' era mujer y el restante ' + self.formato_bonito(datos[2][1]) + '\\% hombre. \n \n' \
        + 'El departamento muestra una proporción un poco '+  self.mayor_menor(datos[2][2],datos[1][2])\
        +'de población femenina que el indicador nacional.'
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','1_06.tex'), 'w')
        archivo.write(des)

    def des_107(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','1_07.csv'))
        des = 'Debido a que las personas de distintas edades tienen diferentes necesidades, es importante conocer la estructura de la población por grupos de edad. Por ejemplo, es de mucho interés saber cuántos niños hay en un departamento porque ellos necesitan educarse para su adecuado desarrollo; el número de adultos mayores también es relevante, porque este grupo necesita de mayores cuidados médicos. \n\n'\
        +'La Encovi estima que en 2014 el ' + self.formato_bonito(datos[1][1]) +  '\\% de la población del departamento de '\
        + self.lugar_geografico + ' es menor de quince años, mientras que el '\
        + self.formato_bonito(datos[4][1]) + '\\% tiene 65 años o más.'
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','1_07.tex'), 'w')
        archivo.write(des)

    def des_201(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','2_01.csv'))
        des = 'El tipo de material del piso de una vivienda incide en la calidad de vida de sus habitantes. Por ejemplo, el piso de tierra es de difícil limpieza, por lo que las personas que habitan viviendas con este tipo de material tienen mayor riesgo de contraer enfermedades gastrointestinales. \n\n' \
        +'En este sentido, la Encovi 2014 muestra que el ' + self.formato_bonito(datos[7][1]) \
        +'\\% de hogares en el departamento de ' + self.lugar_geografico \
        +' habitan viviendas con piso de tierra, mientras que el ' \
        + self.formato_bonito(datos[4][1]) +'\\% habita en viviendas con piso de torta de cemento.'
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','2_01.tex'), 'w')
        archivo.write(des)


    def des_203(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','2_03.csv'))
        des = 'El material del techo también es un aspecto relevante para determinar las condiciones de vida de un hogar. Un techo de mala calidad no brinda el suficiente resguardo para las inclemencias del tiempo, lo cual puede incidir en una mayor prevalencia de enfermedades respiratorias. \n\n' \
        +'En el departamento de ' + self.lugar_geografico \
        +' el ' + self.formato_bonito(datos[2][1]) + '\\% de hogares habitan viviendas con techo de lámina, ' + self.especial(datos[5][1])
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','2_03.tex'), 'w')
        archivo.write(des)

    def des_205(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','2_05.csv'))
        des = 'Se sabe que hay algunas enfermedades cuyos vectores se reproducen más fácilmente en cierto tipo de paredes, como el mal de Chagas; por ello es relevante investigar acerca del tipo de material de las paredes en el que habitan los hogares. \n\n'\
        +'En el 2014, el ' + self.formato_bonito(datos[2][1])+ '\\% de hogares del departamento de '\
        +self.lugar_geografico + ' habitaban una casa con paredes de block, '\
        +self.especial1(datos[4][1])
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','2_05.tex'), 'w')
        archivo.write(des)

    def des_218(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','2_18.csv'))
        des = 'Según área de residencia, la Encovi 2014  muestra que los hogares del área rural del departamento de '\
        +self.lugar_geografico + ' son un poco ' + self.plural_mayor_menor(datos[1][1],datos[2][1]) \
        +' que los del área urbana. \n\n '\
        +'Concretamente, esta encuesta estima que en este departamento el hogar promedio rural tiene '\
        +self.formato_bonito(datos[2][1]) + ' miembros y el urbano ' + self.formato_bonito(datos[1][1])
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','2_18.tex'), 'w')
        archivo.write(des)

    def des_219(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','2_19.csv'))
        des = 'La Encovi revela que a nivel nacional los hogares pobres tienen, en promedio, más habitantes que los no pobres. \n \n'\
        +'Esta tendencia también se encuentra en el departamento de ' + self.lugar_geografico \
        + ', donde en el 2014 los hogares pobres extremos tenían en promedio '\
        +self.formato_bonito(datos[1][1]) + ' habitantes, dato mayor a los '\
        +self.formato_bonito(datos[3][1]) + ' miembros de los hogares no pobres. '
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','2_19.tex'), 'w')
        archivo.write(des)

    def des_601(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','6_01.csv'))
        des = 'Para el año 2006, el valor de la línea de pobreza total era de Q 6,574. Es importante recordar que la línea de pobreza total incluye, además del costo de una canasta básica de alimentos, un monto adicional que corresponde al porcentaje de consumo no alimenticio de las personas, cuyo consumo de alimentos se encuentra alrededor de la línea de pobreza extrema. \n \n'\
        +'Se puede observar que para 2014, el valor de la línea de pobreza total aumentó a Q 10,218, que equivale a un incremento del 137\\%'
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','6_01.tex'), 'w')
        archivo.write(des)

    def des_602(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','6_02.csv'))
        des ='Al comparar el consumo de las familias con la línea de pobreza total, resulta que en 2014 el '\
        +self.formato_bonito(datos[2][1]) + ' \\% de personas en el departamento de '\
        +self.lugar_geografico + ' se encontraba en condición de pobreza. \n \n'\
        +' Este porcentaje es más ' + self.alto_bajo(datos[2][1], datos[1][1]) + '  que el observado en 2006, el cual ascendía a '\
        +self.formato_bonito(datos[1][1])  +'\\%'
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','6_02.tex'), 'w')
        archivo.write(des)

    def des_603(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','6_03.csv'))
        des = 'La Encovi 2014 revela que el 59.3\\% de la población guatemalteca total se encontraba en condición de pobreza. Sin embargo, es importante analizar este dato territorialmente para determinar diferencias a lo interno del país. \n\n'\
        +'Al comparar la incidencia de pobreza del departamento de ' + self.lugar_geografico\
        +' con el dato nacional, se observa que éste tiene un porcentaje de pobreza total '\
        +self.mayor_menor(datos[2][1],datos[1][1]) + ' que el promedio de todo el país. '
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','6_03.tex'), 'w')
        archivo.write(des)

    def des_604(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','6_04.csv'))
        des = ' Por área de residencia, la Encovi 2014  muestra que los hogares del área rural del departamento de '\
        +self.lugar_geografico + ' tienen una  ' + self.mayor_menor(datos[2][1], datos[1][1])\
        +' incidencia de pobreza que los del área urbana. \n\n '\
        + ' Concretamente, esta encuesta estima que en este departamento la incidencia de la pobreza total en el área rural es del  '\
        +self.formato_bonito(datos[2][1]) + '\\%,  mientras que el área urbana es de  ' + self.formato_bonito(datos[1][1]) + '\\%'
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','6_04.tex'), 'w')
        archivo.write(des)

    def des_607(self):
        datos = self.leer_csv(os.path.join(self.ruta_salida, 'csv','6_07.csv'))
        des = ' Para el año 2006, el valor de la línea de pobreza extrema era de Q 3,206. Es importante recordar que la línea de pobreza extrema representa el costo de adquirir la cantidad de calorías mínimas recomendadas para un humano. \n\n'\
        +'Se puede observar que para 2014, el valor de la línea de pobreza extrema aumentó a Q 5,750 que equivale a un incremento del 79.4% respecto al valor de 2006.'
        archivo = open( os.path.join(self.ruta_salida, 'descripciones','6_07.tex'), 'w')
        archivo.write(des)


    def alto_bajo(self,dato1, dato2):
        if float(dato1) > float(dato2):
            return 'alto'
        else:
            return 'bajo'


    def plural_mayor_menor(self, dato1, dato2):
        if dato2 > dato1:
            return 'mayores'
        else:
            return 'menores'

    def especial(self, dato):
        if float(dato) > 1:
            return 'mientras que el '+self.formato_bonito(dato) + '\\% poseen casas con techo de paja, palma o de un material similar. '
        else:
           return 'mientras que casi ningún hogar posee vivienda con techo de paja, palma o de un material similar.'

    def especial1(self, dato):
        if float(dato) > 1:
            return 'mientras que el '+self.formato_bonito(dato) + '\\% de hogares ocupaba una vivienda con paredes de adobe. '
        else:
           return 'mientras que casi ningún hogar habitaba una  vivienda con  paredes de adobe.'

    def formato_bonito(self, numero):
        return "{:,}".format(round(float(numero),2)).strip('0').strip('.')

    def cambio(self, dato1, dato2):
        dato1 = float(dato1)
        dato2 = float(dato2)
        if dato1 > dato2:
            return 'incremento'
        else:
            return 'descenso'

    def porcentaje(self, dato1, dato2):
        dato1 = float(dato1)
        dato2 = float(dato2)
        salida = ''
        if dato1 > dato2:
            salida = str( round((dato1 / dato2 - 1)*100,2) )
        else:
            salida = str( round((1- dato2 / dato1) * 100,2 )  )
        return salida

    def mayor_menor(self,dato1,dato2):
        if dato1 > dato2:
            return ' mayor '
        elif(dato1 < dato2):
            return ' menor '
        else:
            return ' igual '

    def escribir_descripciones(self):
        self.des_102()
        self.des_104()
        self.des_106()
        self.des_107()
        self.des_201()
        self.des_203()
        self.des_205()
        self.des_218()
        self.des_219()
        self.des_601()
        self.des_602()
        self.des_603()
        self.des_604()