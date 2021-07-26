import PySimpleGUI as sg

#sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
"""layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text('Enter something on Row 2'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]
"""


tab1_layout = [
                [sg.Text ('DESCARGAR INVENTARIO', size=(12,1))],
                [sg.Text ('Presione el botón para iniciar la descarga')],
                [sg.Button('Descargar', key='btn_item')],
                [sg.one_line_progress_meter('test',
                    1,
                    20,
                    key = "OK for 1 meter",
                    orientation = "h",
                    bar_color = (None, None),
                    button_color = None,
                    size = (20, 20),
                    border_width = None,
                    grab_anywhere = False,
                    no_titlebar = True)],
              ]

tab2_layout = [[sg.T('This is inside tab 2')]]    

layout = [[
            sg.TabGroup([[sg.Tab('Items', tab1_layout), 
            sg.Tab('Ordenes', tab2_layout)]])],    
            [sg.Button('Salir')]]    

# Create the Window
window = sg.Window('Momi - Integración Netsuite/POS', layout, default_element_size=(12,1))    

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Salir': # if user closes window or clicks cancel
        break

    if event == 'Descargar': #'btn_items': 
        print ('Iniciando proceso')
    
    print('You entered ', values[0])

window.close()