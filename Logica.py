# -*- coding: utf-8 -*-
from Documento import *
import os
from openpyxl import load_workbook


class Manejador:

    def __init__(self):
        self.departamentos = ['Guatemala',
        'El Progreso',
        'Sacatepéquez',
        'Chimaltenango',
        'Escuintla',
        'Santa Rosa',
        'Sololá',
        'Totonicapán',
        'Quetzaltenango',
        'Suchitepéquez',
        'Retalhuleu',
        'San Marcos',
        'Huehuetenango',
        'Quiché',
        'Baja Verapaz',
        'Alta Verapaz',
        'Petén',
        'Izabal',
        'Zacapa',
        'Chiquimula',
        'Jalapa',
        'Jutiapa'
        ]
        self.documentos = []
        self.crear_documentos()
        self.crear_carpetas()
        self.empezar_documentos()
        self.leer_libro()

    def crear_documentos(self):
        for depto in self.departamentos:
            self.documentos.append( Document( 'Encovi-2014-' + depto,
            depto,
            os.path.join('/home/hugo/Documents/Departamentos', depto)
             ) )

    def crear_carpetas(self):
        for x in range(0,22):
            self.documentos[x].crear_directorio()
            self.documentos[x].copiar_utilidades()


    def empezar_documentos(self):
        for x in range(0,22):
            self.documentos[x].crear_documento()

    def leer_libro(self):
        wb = load_workbook(filename = 'Contenido_Encovi_Departamentales.xlsx')
        sheet_ranges = wb['Hoja1']
        for row in sheet_ranges:
            for cell in row:
                for x in range(0,22):
                    if cell.col_idx