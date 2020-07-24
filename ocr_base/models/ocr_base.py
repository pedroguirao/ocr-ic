
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_bank import sanitize_account_number
import base64
import cv2
import pytesseract
import numpy as np
from PIL import Image
import time

import logging
_logger = logging.getLogger(__name__)

TYPE = [
    #('emitida', 'Facturas emitidas'),
    ('identity', 'DNI'),
    #('emitida_batch', 'Lote de facturas emitidas'),
    ('image', 'Imagen'),
]
STATE = [
    ('draft', 'Draft'),
    ('sending', 'Sending'),
    ('processing', 'Processing'),
    ('error', 'Error'),
    ('done', 'Done'),
]

class OcrBaseClass(models.Model):
    _name = 'ocr.base'
    _description = 'IA interpreter for images'

    name = fields.Char(
        string='Name'
    )
    attachment_ids = fields.Many2many(comodel_name="ir.attachment",
                                relation="m2m_ocr_attachments_rel",
                                column1="m2m_id",
                                column2="attachment_id",
                                string="Attachments")
    type = fields.Selection(
        selection=TYPE, string="Type", default='recibida',
    )
    state = fields.Selection(
        selection=STATE, string="State", default='draft', track_visibility='onchange'
    )
    values = fields.Text(string='values')


    @api.multi
    def procesar_ocr(self, imagen, tipo):

        print("Procesar_OCR")

        img = cv2.imread(imagen)
        if img.all() == None:
            raise Exception("no puedo localizar el fichero !")
        #img = base64.decodebytes(imagen)
        # esto se aplica para lo que viene en color, que es casi todo, intentamos pasar a la funcion de switcher
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #print("Imagen Leida")
        # primero convertimos la imagen a escala de grises, esto se hace para permiso de circulacion
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #print("Escala Grises")
        # convertir a blanco y negro, solo para itv
        # (thresh, img) = cv2.threshold(img, 56, 127, cv2.THRESH_BINARY)

        # este preprocesamiento suele dar muy buen resultado en todo tipo de iamgenes, por lo que de momento se aplica a todas
        img = cv2.medianBlur(img, 3)
        #print("Blur")
        # print(pytesseract.image_to_string(img, lang='spa'))
        self.values = result = pytesseract.image_to_data(imagen, lang='spa', output_type='dict')

        print(self.values)

    @api.multi
    def send2tesseract(self):
        for record in self.attachment_ids:
            img = base64.b64decode(record.datas)
            #img = record.datas

            with open('/tmp/imageToSave.png', "wb") as imgFile:
                imgFile.write(img)

            #https://stackoverflow.com/questions/49747190/store-odoo-images-into-filesystem

            #cv2.imwrite('Test_gray.jpg', image)
            self.procesar_ocr('/tmp/imageToSave.png', self.type)



