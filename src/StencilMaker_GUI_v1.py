import PySimpleGUI as sg
from StencilMaker_functions_v1 import *

def create_main_window(type_package, package):
    #Parameters
    w = 7
    h = 1
    menu_w = 16
    menu_h = h
    log_w = 75
    log_h = 6
    button_w = 7
    button_h = h
    disabled_color = '#9BA8B6'

    #Text boxes
    #---TAB 0---#
    #---COL 0---#
    text_pin_number = sg.Text(key = 'text_pin_number', text = 'Pin number')
    text_pin_number_0 = sg.Text(key = 'text_number_0', text = 'Pin number [0]')
    text_pin_number_1 = sg.Text(key = 'text_number_1', text = 'Pin number [1]')
    text_pin_number_2 = sg.Text(key = 'text_number_2', text = 'Pin number [2]')
    text_pin_number_3 = sg.Text(key = 'text_number_3', text = 'Pin number [3]')
    #---COL 2---#
    text_pin_length = sg.Text(text = 'Pin length')
    text_pin_width = sg.Text(text = 'Pin width')
    text_pin_pitch = sg.Text(text = 'Pin pitch')
    text_pin_distance_x = sg.Text(key = 'text_distance_x', text = 'Pin distance x')
    text_pin_distance_y = sg.Text(key = 'text_distance_y', text = 'Pin distance y')
    #---COL 4---#
    text_tolerance = sg.Text(text = 'Tolerance')
    text_stencil_height = sg.Text(text = 'Stencil height')
    text_margin_x= sg.Text(text = 'Horizontal margin')
    text_margin_y = sg.Text(text = 'Vertical margin')
    text_menu_unit = sg.Text(text = 'Unit')
    #---TAB 1---#
    #---COL 7---#
    text_void_0 = sg.Text(text = '')
    text_min_max_n_pin = sg.Text(text = 'Pin number')
    text_min_max_length = sg.Text(text = 'Pin length')
    text_min_max_width = sg.Text(text = 'Pin width')
    text_min_max_dist_x = sg.Text(text = 'Pin distance')
    text_min_max_pitch = sg.Text(text = 'Pin pitch')
    text_min_max_h = sg.Text(text = 'Stencil height')
    text_min_max_margin_x = sg.Text(text = 'Horizontal margin')
    text_min_max_margin_y =sg.Text(text = 'Vertical margin')
    #---COL 8---#
    text_min = sg.Text(text = 'Min (mm)', key = 'text_min')
    #---COL 9---#
    text_max = sg.Text(text = 'Max (mm)', key = 'text_max')
    #---COL 10---#
    text_void_1 = sg.Text(text = '')
    #---COL 11---#
    text_file_name = sg.Text(text = 'File name')
    text_actual_folder = sg.Text(text = 'Actual folder')

    #Input boxes
    #---TAB 0---#
    #---COL 1---#
    input_pin_number = sg.Input(key = 'input_pin_number', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_pin_number_0 = sg.Input(key = 'input_pin_number_0', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_pin_number_1 = sg.Input(key = 'input_pin_number_1', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_pin_number_2 = sg.Input(key = 'input_pin_number_2', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_pin_number_3 = sg.Input(key = 'input_pin_number_3', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    #---COL 3---#
    input_pin_length = sg.Input(key = 'input_pin_length', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_pin_width = sg.Input(key = 'input_pin_width', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_pin_pitch = sg.Input(key = 'input_pin_pitch', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_distance_x = sg.Input(key = 'input_distance_x', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_distance_y = sg.Input(key = 'input_distance_y', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    #---COL 5---#
    input_tolerance = sg.Input(key = 'input_tolerance', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_margin_x = sg.Input(key = 'input_margin_x', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_margin_y = sg.Input(key = 'input_margin_y', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    input_stencil_height = sg.Input(key = 'input_stencil_height', size = (w,h), enable_events = True, readonly = True, disabled_readonly_background_color = disabled_color)
    #---TAB 1---#
    #---COL 8---#
    input_min_n_pin = sg.Input(key = 'input_min_n_pin', size = (w,h), enable_events = True, readonly = False)
    input_min_length = sg.Input(key = 'input_min_length', size = (w,h), enable_events = True, readonly = False)
    input_min_width = sg.Input(key = 'input_min_width', size = (w,h), enable_events = True, readonly = False)
    input_min_dist_x = sg.Input(key = 'input_min_dist_x', size = (w,h), enable_events = True, readonly = False)
    input_min_pitch = sg.Input(key = 'input_min_pitch', size = (w,h), enable_events = True, readonly = False)
    input_min_h = sg.Input(key = 'input_min_h', size = (w,h), enable_events = True, readonly = False)
    input_min_margin_x = sg.Input(key = 'input_min_margin_x', size = (w,h), enable_events = True, readonly = False)
    input_min_margin_y = sg.Input(key = 'input_min_margin_y', size = (w,h), enable_events = True, readonly = False)
    #---COL 9---#
    input_max_n_pin = sg.Input(key = 'input_max_n_pin', size = (w,h), enable_events = True, readonly = False)
    input_max_length = sg.Input(key = 'input_max_length', size = (w,h), enable_events = True, readonly = False)
    input_max_width = sg.Input(key = 'input_max_width', size = (w,h), enable_events = True, readonly = False)
    input_max_dist_x = sg.Input(key = 'input_max_dist_x', size = (w,h), enable_events = True, readonly = False)
    input_max_pitch = sg.Input(key = 'input_max_pitch', size = (w,h), enable_events = True, readonly = False)
    input_max_h = sg.Input(key = 'input_max_h', size = (w,h), enable_events = True, readonly = False)
    input_max_margin_x = sg.Input(key = 'input_max_margin_x', size = (w,h), enable_events = True, readonly = False)
    input_max_margin_y = sg.Input(key = 'input_max_margin_y', size = (w,h), enable_events = True, readonly = False)
    #---COL 12---#
    input_file_name = sg.Input(key = 'input_file_name', size = (w*4,h), enable_events = True, default_text = '3d_stencil')
    input_folder = sg.Input(key = 'input_folder', size = (w*4,h), disabled = True)

    #Multiline
    log_window = sg.Multiline(key = 'log_window', autoscroll = True, size = (log_w, log_h), reroute_cprint = True, disabled=True)

    #Option menu
    menu_type = sg.OptionMenu(['DIP', 'QFP'], default_value = 'Select type', key = 'menu_type', enable_events = 'True', size = (menu_w, menu_h))
    menu_package = sg.OptionMenu(get_available_packages(type_package), default_value = package, key = 'menu_package', enable_events = 'True', size = (menu_w, menu_h), disabled = True)
    menu_unit = sg.OptionMenu(['mm', 'cm', 'in'], default_value = 'mm', key = 'menu_unit', enable_events = 'True', size = (w - 5, h))

    #Buttons
    #---TAB 0---#
    button_folder = sg.FolderBrowse('Folder', key = 'button_folder', size = (button_w, button_h), enable_events = True, target='button_folder')
    button_save = sg.Button('Save', key = 'button_save', size = (button_w, button_h), enable_events = True, disabled = True)
    button_run = sg.Button('Run', key = 'button_run', size = (button_w, button_h), enable_events = True, disabled = True)
    button_create = sg.Button('Create', key = 'button_create', size = (button_w, button_h), enable_events = True, disabled = True)
    button_clear = sg.Button('Clear', key = 'button_clear', size=(button_w, button_h), enable_events = True)
    button_cancel = sg.Button('Cancel', key = 'button_cancel', size=(button_w, button_h), enable_events = True)
    #---TAB 1---#
    button_update = sg.Button('Update', key = 'button_update', size=(button_w, button_h), enable_events = True, disabled = True)
    button_back = sg.Button('Back', key = 'button_back', size=(button_w, button_h), enable_events = True, disabled = True)
    #button_test = sg.Button('Test', key = 'button_test', size=(button_w, button_h), enable_events = True)

    #Checkbox
    log_check = sg.Checkbox('Activate log file writing', key = 'log_check', default = True, enable_events = True)

    #Columns
    Col0 = sg.Column([[text_pin_number], [text_pin_number_0], [text_pin_number_1], [text_pin_number_2], [text_pin_number_3]])
    Col1 = sg.Column([[input_pin_number], [input_pin_number_0], [input_pin_number_1], [input_pin_number_2], [input_pin_number_3]])
    Col2 = sg.Column([[text_pin_length], [text_pin_width], [text_pin_pitch], [text_pin_distance_x], [text_pin_distance_y]])
    Col3 = sg.Column([[input_pin_length], [input_pin_width], [input_pin_pitch], [input_distance_x], [input_distance_y]]) 
    Col4 = sg.Column([[text_tolerance], [text_margin_x], [text_margin_y], [text_stencil_height], [text_menu_unit]])
    Col5 = sg.Column([[input_tolerance], [input_margin_x], [input_margin_y], [input_stencil_height], [menu_unit]])
    Col6 = sg.Column([[log_window]])
    Col7 = sg.Column([[text_void_0], [text_min_max_n_pin], [text_min_max_length], [text_min_max_width], [text_min_max_dist_x], [text_min_max_pitch], [text_min_max_h], [text_min_max_margin_x], [text_min_max_margin_y]])
    Col8 = sg.Column([[text_min], [input_min_n_pin], [input_min_length], [input_min_width], [input_min_dist_x], [input_min_pitch], [input_min_h], [input_min_margin_x], [input_min_margin_y]], element_justification = 'center')
    Col9 = sg.Column([[text_max], [input_max_n_pin], [input_max_length], [input_max_width], [input_max_dist_x], [input_max_pitch], [input_max_h], [input_max_margin_x], [input_max_margin_y]], element_justification = 'center')
    Col10 = sg.Column([[text_void_1], [button_update], [button_back]])
    Col11 = sg.Column([[text_file_name], [text_actual_folder]])
    Col12 = sg.Column([[input_file_name], [input_folder]])

    #Frames
    #---TAB 0---#
    frame0 = sg.Frame('', [[button_folder, button_create], [button_run, button_save]])
    frame1 = sg.Frame('', [[button_clear, button_cancel]], pad=((0, 0), (66, 0)))
    #---TAB 1---#
    frame2 = sg.Frame('Limit values', [[Col7, Col8, Col9, sg.vtop(Col10)]])
    frame3 = sg.Frame('Saving info', [[Col11, Col12]])

    left_column = sg.Column([[sg.vtop(Col0), sg.vtop(Col1), sg.vtop(Col2), sg.vtop(Col3), sg.vtop(Col4), sg.vtop(Col5)], [sg.vtop(Col6)]])
    right_column = sg.Column([[menu_type], [menu_package], [frame0], [log_check], [frame1]], expand_y = True)

    #Tabs
    tab1_layout = [
        [sg.vtop(left_column), sg.VerticalSeparator(color = 'grey'), sg.vtop(right_column)]
    ]
    tab2_layout = [
        [frame2, sg.vtop(frame3)]
    ]

    main_layout = [
        [sg.TabGroup([
            [sg.Tab('Design', tab1_layout), 
            sg.Tab('Options', tab2_layout)]
        ])]
    ]
    
    return sg.Window('StencilMaker_v1', main_layout, finalize = True)