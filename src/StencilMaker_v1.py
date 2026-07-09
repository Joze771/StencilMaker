import PySimpleGUI as sg

from StencilMaker_functions_v1 import *
from StencilMaker_GUI_v1 import *

#-----VARIABLES & DEFAULT VALUES-----#
package_type = 'Select type'
package = 'Select package'
stencil_data = [''] * 14
folder = ''
file_name = '3d_stencil'
all_fields_filled = False
run_button_pushed = False
menu_w = 16
menu_h = 1
unit_constant = 10
log_writing_activated = True
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(root_directory, "assets", "icon.ico")

#-----STARTUP FUNCTIONS-----#
min_max_value = get_min_max_value()
min_max_value_updated = min_max_value.copy()
window = create_main_window(package_type, package)
window.set_icon(icon_path)
update_min_max_value_box(window, min_max_value, unit_constant)
date_time = get_date_time()

#-----USEFUL LISTS-----#
input_elements = [
    window['input_pin_length'], window['input_pin_width'], window['input_pin_number'], window['input_distance_x'], window['input_pin_pitch'], 
    window['input_tolerance'], window['input_stencil_height'], window['input_margin_x'], window['input_margin_y'], window['input_distance_y'], 
    window['input_pin_number_0'], window['input_pin_number_1'], window['input_pin_number_2'], window['input_pin_number_3']
]
input_elements_key = [
    'input_pin_number', 'input_pin_length', 'input_pin_width',  'input_distance_x', 'input_pin_pitch', 
    'input_tolerance', 'input_stencil_height', 'input_margin_x', 'input_margin_y', 'input_pin_number_0', 
    'input_pin_number_1', 'input_pin_number_2', 'input_pin_number_3', 'input_distance_y'
    ]
custom_elements = [window['input_distance_y'], window['input_pin_number_0'], window['input_pin_number_1'], window['input_pin_number_2'], window['input_pin_number_3']]

input_min_max_element_key = [
    'input_min_n_pin', 'input_min_length', 'input_min_width', 'input_min_dist_x', 'input_min_pitch', 
    'input_min_h', 'input_min_margin_x', 'input_min_margin_y', 'input_max_n_pin', 'input_max_length', 
    'input_max_width', 'input_max_dist_x', 'input_max_pitch', 'input_max_h', 'input_max_margin_x', 
    'input_max_margin_y'
]

#-----SUPERLOOP-----#
while True:
    event, values = window.Read()
    if log_writing_activated:
        try:
            log_file_write(event, values[event], date_time)
        except:
            log_file_write(event, 'None', date_time)
    match event:
        case sg.WIN_CLOSED:
            break
        case 'button_clear':
            window['log_window'].update(value = '')
        case 'menu_type':
            window['menu_package'].update(disabled = False)
            if values['menu_type'] != package_type:
                window['button_create'].update(disabled = True)
                for input_box in input_elements:
                    input_box.update(readonly = True, value = '')
            package_type = values['menu_type']
            window['menu_package'].update(values = get_available_packages(package_type), value = 'Select package', size = (menu_w, menu_h))
            match values['menu_type']:
                case 'DIP':
                    for element in custom_elements:
                        element.update(readonly = True)
                case 'QFP':
                    window['input_pin_number'].update(readonly = True)
        case 'menu_package' if values['menu_package'] != 'Select package':
            try:            
                window['menu_unit'].update(disabled = True)
                window['button_create'].update(disabled = True)
                package = values['menu_package']
                if package not in ('Select package', 'Custom'):
                    stencil_data[:10] =  get_data(package_type, package, stencil_data[:10])
                    n_pin, pin_length, pin_width, distance_x, pin_pitch = stencil_data[:5]
                    pin_length *= unit_constant
                    pin_width *= unit_constant
                    distance_x *= unit_constant
                    pin_pitch *= unit_constant
                    window['input_pin_length'].update(value = f"{pin_length:.3f}".rstrip('0').rstrip('.'))
                    window['input_pin_width'].update(value = f"{pin_width:.3f}".rstrip('0').rstrip('.'))
                    window['input_distance_x'].update(value = f"{distance_x:.3f}".rstrip('0').rstrip('.'))
                    window['input_pin_pitch'].update(value = f"{pin_pitch:.3f}".rstrip('0').rstrip('.'))
                    match values['menu_type']:
                        case 'DIP':
                            n_pin = int(n_pin)
                            window['input_pin_number'].update(value = n_pin)
                        case 'QFP':
                            stencil_data[9] = math.trunc(stencil_data[9]*1000)/1000 
                            n_pin_0, n_pin_1, n_pin_2, n_pin_3, distance_y = stencil_data[5:10]
                            n_pin_0, n_pin_1, n_pin_2, n_pin_3 = int(n_pin_0), int(n_pin_1), int(n_pin_2), int(n_pin_3)
                            distance_y *= unit_constant 
                            window['input_pin_number_0'].update(value = n_pin_0)
                            window['input_pin_number_1'].update(value = n_pin_1)
                            window['input_pin_number_2'].update(value = n_pin_2)
                            window['input_pin_number_3'].update(value = n_pin_3)
                            window['input_distance_y'].update(value = f"{distance_y:.3f}".rstrip('0').rstrip('.'))
                    for input_box in input_elements:
                        input_box.update(readonly = False)
                    match values['menu_type']:
                        case 'DIP':
                            for element in custom_elements:
                                element.update(readonly = True)
                        case 'QFP':
                            window['input_pin_number'].update(readonly = True)
                    log_write(window['log_window'], date_time, '>>> Data loaded successfully.\n')
                elif package == 'Custom':
                    log_write(window['log_window'], date_time, '>>> Enter custom stencil data.\n')
                    if all_fields_empty(stencil_data):
                        window['menu_unit'].update(disabled = False)
                    else:
                        window['menu_unit'].update(disabled = True)
                    for input_box in input_elements:
                        input_box.update(readonly = False)
                    match values['menu_type']:
                        case 'DIP':
                            for element in custom_elements:
                                element.update(readonly = True)
                        case 'QFP':
                            window['input_pin_number'].update(readonly = True)
                    if all_fields_filled:
                        window['button_create'].update(disabled = False)
                else:
                    window['button_create'].update(disabled = True)
            except Exception as error:
                log_write(window['log_window'], date_time, '>>> Error loading data.\n', error)
                for input_box in input_elements:
                    input_box.update(readonly = True)
        case 'button_create':
            personalized_package_name = sg.popup_get_text('Enter custom package name:', icon = icon_path)
            try:
                get_personalized_data(stencil_data, personalized_package_name, package_type)
                log_write(window['log_window'], date_time, f">>> Custom stencil data saved as {personalized_package_name}.txt.\n")
                window['button_create'].update(disabled = True)
            except Exception as error:
                log_write(window['log_window'], date_time, '>>> An error occurred while creating the file.\n', error)
        case event if event in input_elements_key and package != 'Select package':
            window['menu_unit'].update(disabled = True)
            if is_float(values[event]) or values[event] == '':
                all_fields_filled, stencil_data = get_input_data(event, values[event], stencil_data, package_type, unit_constant)
                window[event].update(background_color = "#FFFFFF")
            else:
                log_write(window['log_window'], date_time, '>>> Invalid value.\n')
                window[event].update(background_color = "#C93F3F")
            if all_fields_filled:
                error_presence = integrity_control(stencil_data, min_max_value, package_type, window)
                if error_presence == False:
                    window['button_run'].update(disabled = False)
                    if values['menu_package'] == 'Custom':
                        window['button_create'].update(disabled = False)
                else:
                    window['button_save'].update(disabled = True)
                    window['button_run'].update(disabled = True)
                    window['button_create'].update(disabled = True)
            else:
                window['button_save'].update(disabled = True)
                window['button_run'].update(disabled = True)
                window['button_create'].update(disabled = True)
            if all_fields_empty(stencil_data):
                window['menu_unit'].update(disabled = False)   
        case 'button_run':
            stencil_stl = generate_stl(package_type, stencil_data)
            log_write(window['log_window'], date_time, '>>> Model generated!\n')
            run_button_pushed = True
            if folder != '':
                window['button_save'].update(disabled = False)
        case 'button_folder':
            folder = values['button_folder']
            log_write(window['log_window'], date_time, '>>> Folder selected: ' + folder +'\n')
            window['input_folder'].update(value = folder)
            if run_button_pushed:
                window['button_save'].update(disabled = False)
                run_button_pushed = False
        case 'button_save':
            if same_file_name(file_name, folder):
                user_choice = sg.popup_ok_cancel('File with this name already exists, overwrite?', title = 'Warning', icon = icon_path)
                if user_choice == 'OK':
                    save_path = folder + '/' + file_name + '.stl'
                    stencil_stl.export(save_path)
                    window['button_save'].update(disabled = True)
            else:
                save_path = folder + '/' + file_name + '.stl'
                try:
                    stencil_stl.export(save_path)
                    log_write(window['log_window'], date_time, '>>> Model saved!\n')
                except Exception as error:
                    log_write(window['log_window'], date_time, '>>> Problems occurred while saving the model.\n', error)
                window['button_save'].update(disabled = True)
        case 'button_cancel':
            for element in input_elements:
                element.update(value = '', background_color = "#FFFFFF", readonly = True)
            window['menu_unit'].update(disabled = False)
            window['button_run'].update(disabled = True)
            window['button_save'].update(disabled = True)
            window['button_create'].update(disabled = True)
            window['menu_package'].update(value = 'Select package', size = (menu_w, menu_h))
            stencil_data = [''] * 14
        case 'input_file_name':
            file_name_is_correct, error_string = check_file_name(values['input_file_name'])
            if not file_name_is_correct:
                log_write(window['log_window'], date_time, error_string)
                window['button_save'].update(disabled = True)
            else:
                file_name = values['input_file_name']
                if folder != '':
                    window['button_save'].update(disabled = False)
        case event if event in input_min_max_element_key:
            if is_float(values[event]):
                min_max_value_updated = get_input_data_extreme(event, values[event], min_max_value_updated, unit_constant)
                window['button_update'].update(disabled = False)
        case 'button_update':
            min_max_value_back = min_max_value.copy()
            min_max_value = min_max_value_updated.copy()
            if all_fields_filled:
                error_presence = integrity_control(stencil_data, min_max_value, package_type, window)
                if error_presence == False:
                    window['button_run'].update(disabled = False)
                    if values['menu_package'] == 'Custom':
                        window['button_create'].update(disabled = False)
                else:
                    window['button_save'].update(disabled = True)
                    window['button_run'].update(disabled = True)
                    window['button_create'].update(disabled = True)
            else:
                window['button_save'].update(disabled = True)
                window['button_run'].update(disabled = True)
                window['button_create'].update(disabled = True)
            update_min_max_value_file(min_max_value_updated)
            window['button_update'].update(disabled = True)
            window['button_back'].update(disabled = False)
        case 'button_back':
            min_max_value = min_max_value_back.copy()
            min_max_value_updated = min_max_value_back.copy()
            if all_fields_filled:
                error_presence = integrity_control(stencil_data, min_max_value, package_type, window)
                if error_presence == False:
                    window['button_run'].update(disabled = False)
                    if values['menu_package'] == 'Custom':
                        window['button_create'].update(disabled = False)
                else:
                    window['button_save'].update(disabled = True)
                    window['button_run'].update(disabled = True)
                    window['button_create'].update(disabled = True)
            else:
                window['button_save'].update(disabled = True)
                window['button_run'].update(disabled = True)
                window['button_create'].update(disabled = True)
            update_min_max_value_file(min_max_value_back)
            update_min_max_value_box(window, min_max_value_back, unit_constant)
            window['button_back'].update(disabled = True)    
        case 'menu_unit':
            match values['menu_unit']:
                case 'mm':
                    unit_constant = 10
                    window['text_min'].update(value = 'Min (mm)')
                    window['text_max'].update(value = 'Max (mm)')
                    update_min_max_value_box(window, min_max_value, unit_constant)
                case 'cm':
                    unit_constant = 1
                    window['text_min'].update(value = 'Min (cm)')
                    window['text_max'].update(value = 'Max (cm)')
                    update_min_max_value_box(window, min_max_value, unit_constant)
                case 'in':
                    unit_constant = 0.3937
                    window['text_min'].update(value = 'Min (in)')
                    window['text_max'].update(value = 'Max (in)')
                    update_min_max_value_box(window, min_max_value, unit_constant)
        case 'log_check':
            log_writing_activated = values['log_check']
    #print(stencil_data)

#-----SHUTDOWN FUNCTIONS-----#
window.close()