import os
import shutil as sh

class Document:

    def __init__(self, tituloDoc, lugar_geografico, ruta_salida, anio = 2014):
        self.titulo_documento = tituloDoc
        self.lugar_geografico = lugar_geografico
        self.ruta_salida = ruta_salida
        self.anio_evento = anio
        self.titulo_seccion = {}
        self.descripcion = {}
        self.titulo_grafica = {}
        self.desagregacion_grafica = {}
        self.grafica = {}
        self.fuente = {}

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
        self.documento = open( os.path.join( self.ruta_salida,
        self.titulo_documento ), 'w+' )
        self.documento.write('\\input{Carta3.tex} \n')
        self.documento.write('\\renewcommand{\partes}{} \n')
        self.documento.write('\\renewcommand{\\titulodoc}{ ' +
        self.titulo_documento + '}\n')
        self.documento.write( '\\newcommand{\\ra}[1]{\\renewcommand{\\arraystretch}{#1}} \n' )
        self.documento.write( '\\definecolor{color1}{rgb}{0,0,0.8} \n' +
        '\\definecolor{color2}{rgb}{0.3,0.5,1} \n' )
        self.documento.write('\\begin{document} \n' )


    def crear_cajita(self, titulo,descripcion, titulo_grafica,
        des_grafica, grafica, fuente):
        cajita = '\\cajita{% \n'
        + titulo + ' % \n'
        + '}% \n'
        + '{%'
        descripcion +  ' % \n'
        + '}% \n'
        + '{%'
        + titulo_grafica + ' % \n'
        + '}%'
        + '{% \n '
        + des_grafica + ' % \n'
        + '}%'
        + '{% \n '
        + grafica +' % \n'
        + '}%'
        + '{% \n'
        + fuente + ' % \n'
        + '} \n'
        return cajita

    def escribir_en_doc(self, texto):
        self.documento.write('\n \n ' + texto + '\n \n')

    def terminar_documento(self):
        escribir_en_doc('\\end{document}')
        self.documento.close()







