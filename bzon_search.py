from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from phonenumbers import parse, is_valid_number, carrier, geocoder,format_number, PhoneNumberFormat
from kivy.core.clipboard import Clipboard
from itertools import product
import random

# Tu interfaz aquí...
interfaz = """
BoxLayout:
    orientation: 'vertical'
    Screen:
        MDLabel:
            text: "BZON-SEARCH"
            font_size: 50
            halign: "center"
            pos_hint: {"center_x": 0.5, "center_y": 0.9}

    Screen:
        MDLabel:
            text: "BY: STE4LPH"
            font_size: 20
            halign: "center"
            pos_hint: {"center_x": 0.5, "center_y": 1.70}

    Screen:
        MDLabel:
            text: "+"
            font_size: 25
            halign: "center"
            pos_hint: {"center_x": 0.19, "center_y": 2.19}

    Screen:
        MDTextField:
            hint_text:"   XX"
            id: country
            font_size: 25
            width: 100
            input_filter: "int"
            on_text: if len(self.text) > 3: self.text = self.text[:3]
            halign: "center"
            size_hint_x: None
            pos_hint: {"center_x": 0.25, "center_y": 3.2}

    Screen:
        MDTextField:
            id: number_phone
            hint_text: "número de tel."
            font_size: 25
            width: 330
            size_hint_x: None
            pos_hint: {"center_x": 0.59, "center_y": 4.2}

    Screen:
        MDTextField:
            hint_text:"  count"
            halign:"center"
            id: generator
            font_size: 25
            width: 100
            input_filter: "int"
            size_hint_x: None
            halign: "center"
            on_text: if len(self.text) > 2: self.text = self.text[:2]
            pos_hint: {"center_x": 0.3, "center_y": 4.5}

    Screen:
        MDTextField:
            id: transport
            hint_text:"TRANSPORTADOR "
            font_size: 25
            width: 250
            size_hint_x: None
            halign: "center"
            pos_hint: {"center_x": 0.58, "center_y": 5.5}

    Screen:
        MDFillRoundFlatButton:
            text: "Sig."
            pos_hint: {"center_x": 0.5, "center_y": 3.0}
            on_release: app.LOGICA()
"""

class MIAPP(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Blue"
        return Builder.load_string(interfaz)

    def variar(self, numero):
        for i in range(len(numero)):
            if numero[i] == "X":
                numero = numero[:i] + str(random.randint(0, 9)) + numero[i + 1:]
        return numero

    def generate_combinations(self, pattern):
        combinations = []
        count_x = pattern.count("X")
        digits = "0123456789"
        for combination in product(digits, repeat=count_x):
            new_pattern = pattern.replace("X", "{}").format(*combination)
            combinations.append(new_pattern)
        return combinations

    def LOGICA(self):
        country_digit = {
            "+51": 9,  # Peru
            "+33": 9,  # Francia
            "+49": 11,  # Alemania
            "+55": 11,  # Brasil
            "+972": 9,  # Israel
            "+590": 9,  # Guadalupe
            "+598": 8,  # Uruguay
            "+41": 9,  # Suiza
            "+56": 9,  # Chile
            "+506": 8,  # Costa Rica
            "+54": 11,  # Argentina
            "+27": 9,  # Africa
            "+1": 10  # United States
        }

        country_code = self.root.ids.country.text
        codigo_pais = "+" + country_code

        if codigo_pais in country_digit:
            numero_telefono = self.root.ids.number_phone.text
            digitos_numero = country_digit[codigo_pais]

            if len(numero_telefono) != 0 and len(numero_telefono) == digitos_numero and "X" in numero_telefono:
                generar = self.root.ids.generator.text
                operador = self.root.ids.transport.text

                if len(operador) != 0:
                    generar_digit = int(generar)
                    valid_numbers = set()
                    result_text = ""
                    number_generation = codigo_pais + numero_telefono
                    combinations = self.generate_combinations(number_generation)
                    intentos = 0
                    MAX_INTENTOS = 30  

                    while len(valid_numbers) < generar_digit and intentos < MAX_INTENTOS:
                        intentos += 1
                        random_number = random.choice(combinations)
                        
                        
                        
                        if random_number not in valid_numbers:
      
                            try:
                                
                                numero_parsed = parse(random_number, None)
                                numero_international = format_number(numero_parsed, PhoneNumberFormat.INTERNATIONAL)
                                if numero_parsed:
                                    carrier_info = carrier.name_for_number(numero_parsed, "es")
                                    if not operador or carrier_info == operador:
                                        valid_numbers.add(random_number)
                         
                                        result_text += f"-------------------------------------------------\nNúmero : {numero_international}\nOperador : {carrier_info}\n-------------------------------------------------\n"
                            except:
                                pass

                    if intentos >= MAX_INTENTOS:
                        self.ERROR_DIALOGO("Error", "Se alcanzó el límite de intentos sin encontrar números válidos.")
                
                    if len(valid_numbers) > 0:
                        self.TRUE_DIALOGO("Resultados", result_text)
                elif "X" not in numero_telefono and len(numero_telefono) != 0:
                    self.ERROR_DIALOGO("ERROR #7(5)", f"No se permiten ingresar letras")
                elif len(generar) != 0:
                    generar_digit = int(generar)
                    number_generation = codigo_pais + numero_telefono
                    combinations = self.generate_combinations(number_generation)

                    if generar_digit > len(combinations):
                        self.ERROR_DIALOGO("PREMIUM ERROR", f"No es posible generar {generar_digit} números ya que solo existen {len(combinations)} combinaciones posibles.")
                        return

                    valid_numbers = set()
                    result_text = ""

                    if any(char.isalpha() for char in numero_telefono if char != "X"):
                        self.ERROR_DIALOGO("ERROR #7(4)", f"No se permiten ingresar letras")
                    elif "X" in numero_telefono or (numero_telefono.isdigit() and len(numero_telefono) == 1):
                        while len(valid_numbers) < generar_digit:
                            random_number = random.choice(combinations)
                            if random_number not in valid_numbers:
                                
                                try:
                                    numero_parsed = parse(random_number, None)
                                    internation_number = format_number(numero_parsed, PhoneNumberFormat.INTERNATIONAL)
                                    if numero_parsed:
                                        carrier_info = carrier.name_for_number(numero_parsed, "es")
                                        if carrier_info:
                                            valid_numbers.add(random_number)
                                            result_text += f"-------------------------------------------------\nNumber : {internation_number}\nOperador : {carrier_info}\n-------------------------------------------------\n"
                                except:
                                    pass

                        if len(valid_numbers) > 0:
                            self.TRUE_DIALOGO("Resultados", result_text)
                    else:
                        self.ERROR_DIALOGO("ERROR 8", "Introduce la cantidad a generar")
                else:
                    if any(char.isalpha() for char in numero_telefono if char != "X"):
                        self.ERROR_DIALOGO("ERROR #7(3)", f"No se permiten ingresar letras")
                    elif "X" in numero_telefono or (numero_telefono.isdigit() and len(numero_telefono) == 1):
                        self.ERROR_DIALOGO("ERROR 8", f"Introduce la cantidad a generar")
            elif len(numero_telefono) == 0:
                self.ERROR_DIALOGO("ERROR #2", "Ingresa un número de teléfono o la base")
            elif len(numero_telefono) == digitos_numero:
                if any(char.isalpha() for char in numero_telefono if char != "X"):
                    self.ERROR_DIALOGO("ERROR #7(2)", "No se permiten ingresar letras")
                elif numero_telefono.isdigit():
                    try:
                        numero_completo = f"{codigo_pais}{numero_telefono}"
                        parsed_numero = parse(numero_completo, None)
                        pais = geocoder.country_name_for_number(parsed_numero, "es")
                       
                        if is_valid_number(parsed_numero):
                            carrier_info = carrier.name_for_number(parsed_numero, "es")

                            if carrier_info:
                                self.TRUE_DIALOGO("VALIDO #0",f"País :> {pais}\nCodigo de pais :> {codigo_pais}\nNúmero :> {numero_telefono}\nOperadora :> {carrier_info}")
                            else:
                                self.ERROR_DIALOGO("ERROR #6","El número de teléfono existe, pero no tiene transportador")
                        else:
                            self.ERROR_DIALOGO("ERROR #5","El número no es valido")
                    except Exception as e:
                        self.ERROR_DIALOGO("ERROR #4","El número ingresado no existe")
            elif any(char.isalpha() for char in numero_telefono if char != "X"):
                self.ERROR_DIALOGO("ERROR #7(1)", "No se permiten ingresar letras")
            else:
                self.ERROR_DIALOGO("ERROR #3",f"Tienes que ingresar {digitos_numero} digitos")
        elif len(codigo_pais) == 1:
            self.ERROR_DIALOGO("ERROR #0", "Ingresa código de país")
        else:
            self.ERROR_DIALOGO("ERROR #1", f"El código {codigo_pais} no se encuentra disponible")
    
    
    def TRUE_DIALOGO(self, titulo, texto):
        dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[
               MDFlatButton(
                    text="Copiar",
                    on_release=lambda x: self.copiar_respuesta(texto),
                ),      
                          
                MDFlatButton(
                    
                
                    text="Close",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
        
    def ERROR_DIALOGO(self, titulo, texto):
        dialog = MDDialog(
            title=titulo,
            text=texto,
            buttons=[                
                MDFlatButton(
                
                    text="Cerrar",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    def copiar_respuesta(self, texto):
        Clipboard.copy(texto)
        self.ERROR_DIALOGO("Texto Copiado", "Se copio existosamente estúpida.")


if __name__ == "__main__":
    MIAPP().run()
    