import os
import numpy as np
import trimesh
import math
import datetime

STENCIL_DATA_MAP = {
    'input_pin_number':     (0,  int),
    'input_pin_length':     (1,  float),
    'input_pin_width':      (2,  float),
    'input_distance_x':     (3,  float),
    'input_pin_pitch':      (4,  float),
    'input_pin_number_0':   (5,  int),
    'input_pin_number_1':   (6,  int),
    'input_pin_number_2':   (7,  int),
    'input_pin_number_3':   (8,  int),
    'input_distance_y':     (9,  float),
    'input_tolerance':      (10, float),
    'input_stencil_height': (11, float),
    'input_margin_x':       (12, float),
    'input_margin_y':       (13, float)
}

MIN_MAX_VALUE_MAP = {
    'input_min_n_pin':      (0, int),
    'input_min_length':     (1, float),
    'input_min_width':      (2, float),
    'input_min_dist_x':     (3, float),
    'input_min_pitch':      (4, float),
    'input_min_h':          (5, float),
    'input_min_margin_x':   (6, float),
    'input_min_margin_y':   (7, float),
    'input_max_n_pin':      (8, int),
    'input_max_length':     (9, float),
    'input_max_width':      (10, float),
    'input_max_dist_x':     (11, float),
    'input_max_pitch':      (12, float),
    'input_max_h':          (13, float),
    'input_max_margin_x':   (14, float),
    'input_max_margin_y':   (15, float)
}

def get_available_packages(type_package):                                       #Populates the package option menu with the name found in the selected folder (grouped by package type)
    path = os.getcwd() + '/data/' + type_package
    try:
        package_titles = os.listdir(path)
        for i in range(len(package_titles)):
            index = package_titles[i].find('.')
            package_titles[i] = package_titles[i][:index]
        package_titles.append('Custom')
    except:
        package_titles = ['Custom']
    return package_titles

def get_data(type_package, package, package_data):                              #Returns a list with the package data read from the data file
        path = os.getcwd() + '/data/' + type_package + '/'
        pack_path = path + package + '.txt'
        file = open(pack_path)
        if type_package == 'DIP':
            list_interval = range(0,5)
        else:
            list_interval = range(1,10)
        for i in list_interval:
            buffer = file.readline()
            index_0 = buffer.find('=')
            index_1 = buffer.find('\n')
            if index_1 == -1:
                index_1 = len(buffer)
            package_data[i] = float(buffer[index_0+1:index_1])
            package_data[i] = math.trunc(((package_data[i]))*10000)/10000
        file.close()
        return package_data

def check_field_filled(stencil_data, type_package):                             #Checks if all input boxes are filled
    if type_package == 'QFP':
        for_length = range(1, len(stencil_data))
    elif type_package == 'DIP':
        for_length = [0, 1, 2, 3, 4, 10, 11, 12, 13]
    for i in for_length:
        if stencil_data[i] == '':
            return False
    return True

def all_fields_empty(stencil_data):                                              #Checks if the list is empty
    for data in stencil_data:
        if data != '':
            return False
    return True

def get_input_data(event, value, stencil_data, type_package, unit_constant):    #Reads the event and its associate value, converts it to the correct type, scalrd if needed, checks if all fields are filled and then, returns the updated stencil_data
    if event in STENCIL_DATA_MAP:
        index, target_type = STENCIL_DATA_MAP[event]
        if value != '':
            if target_type == int:
                value = int(value)
            else:
                value = math.trunc((float(value) / unit_constant) * 1000) / 1000
        else:
            value = ''
        stencil_data[index] = value
    return check_field_filled(stencil_data, type_package), stencil_data

def generate_DIP(stencil_data):                                                 #Generates the stl model for the DIP type package
    pin_number, pin_length, pin_width, distance_x, pin_pitch = stencil_data[:5]
    tolerance, stencil_height, margin_x, margin_y = stencil_data[10:]
    #Creation of one pin
    pin_measure = [pin_length + tolerance*2, pin_width + tolerance*2, stencil_height + 0.02]
    pin_model = trimesh.creation.box(pin_measure)
    pin_model.rezero()
    #Start with "the base"
    base_length = 2*margin_x + 2*pin_measure[0] + distance_x
    base_width = 2*margin_y + int(pin_number/2)*pin_measure[1] + int(pin_number/2 - 1)*pin_pitch
    base_measure = [base_length, base_width, stencil_height]
    base = trimesh.creation.box(base_measure)
    base.rezero()
    #Creation of all pin
    pin = [None] * pin_number
    for i in range(pin_number):
        pin[i] = pin_model.copy()
    #Pin positioning (first column)
    for i in range(int(pin_number/2)):
        pin_translation = [margin_x, margin_y + i*pin_measure[1] + i*pin_pitch, -0.01]
        pin[i].apply_translation(pin_translation)
    #Pin positioning (second column)
    for i in range(int(pin_number/2)):
        pin_translation = [margin_x + pin_measure[0] + distance_x, margin_y + i*pin_measure[1] + i*pin_pitch, -0.01]
        pin[i + int(pin_number/2)].apply_translation(pin_translation)
    #Difference and export
    all_pins_combined = trimesh.util.concatenate(pin)
    total = trimesh.boolean.difference([base, all_pins_combined])
    
    return total

def generate_QFP(stencil_data):                                                 #Generates the stl model for the QFP type package 
    pin_length, pin_width, distance_x, pin_pitch, n_pin_0, n_pin_1, n_pin_2, n_pin_3, distance_y, tolerance, stencil_height, margin_x, margin_y = stencil_data[1:]
    M_90 = [(0, -1, 0, 0), 
            (1, 0 ,0, 0), 
            (0, 0, 1, 0), 
            (0, 0, 0, 1)]
    n_pin_h = n_pin_0 + n_pin_2 
    n_pin_v = n_pin_1 + n_pin_3
    #Creation of one pin
    pin_length = [pin_length + tolerance*2, pin_width + tolerance*2, stencil_height + 0.02]
    pin_model_o = trimesh.creation.box(pin_length)
    pin_model_v = trimesh.creation.box(pin_length).apply_transform(M_90)
    pin_model_v.rezero()
    pin_model_o.rezero()
    #Start with "the base"
    base_x = 2*margin_x + 2*pin_length[0] + distance_x
    base_y = 2*margin_y + 2*pin_length[0] + distance_y
    base_length = [base_x, base_y, stencil_height]
    base = trimesh.creation.box(base_length)
    base.rezero()
    #Offset definitions
    offset_0 = (base_length[1] - n_pin_0*pin_length[1] - (n_pin_0 - 1)*pin_pitch)/2
    offset_1 = (base_length[0] - n_pin_1*pin_length[1] - (n_pin_1 - 1)*pin_pitch)/2
    offset_2 = (base_length[1] - n_pin_2*pin_length[1] - (n_pin_2 - 1)*pin_pitch)/2
    offset_3 = (base_length[0] - n_pin_3*pin_length[1] - (n_pin_3 - 1)*pin_pitch)/2
    #Creation of horizontal pin
    pin_h = [None] * int(n_pin_h)
    for i in range(int(n_pin_h)):
        pin_h[i] = pin_model_o.copy()
    #Creation of vertical pin
    pin_v = [None] * int(n_pin_v)
    for i in range(int(n_pin_v)):
        pin_v[i] = pin_model_v.copy()
    #Pin positioning (Left column/ Zone 0)
    for i in range(int(n_pin_0)):
        pin_translation = [margin_x, 
                        i*pin_length[1] + i*pin_pitch + offset_0, 
                        -0.01]
        pin_h[i].apply_translation(pin_translation)
    #Pin positioning (Up row/ Zone 1)
    for i in range(int(n_pin_1)):
        pin_translation = [i*pin_length[1] + i*pin_pitch + offset_1, 
                        margin_y + distance_y + pin_length[0], 
                        -0.01]
        pin_v[i + int(n_pin_3)].apply_translation(pin_translation)
    #Pin positioning (Right column/ Zone 2)
    for i in range(int(n_pin_2)):
        pin_translation = [margin_x + distance_x + pin_length[0], 
                        i*pin_length[1] + i*pin_pitch + offset_2,
                        -0.01]
        pin_h[i + int(n_pin_0)].apply_translation(pin_translation)
    #Pin positioning (Down row/ Zone 3)
    for i in range(int(n_pin_3)):
        pin_translation = [i*pin_length[1] + i*pin_pitch + offset_3, 
                        margin_y, 
                        -0.01]
        pin_v[i].apply_translation(pin_translation)
    #Difference and export
    all_pins_combined = trimesh.util.concatenate(pin_h + pin_v)
    total = trimesh.boolean.difference([base, all_pins_combined])
    
    return total

def generate_stl(type_package, stencil_data):                                   #Selects the correct generation method for the stencil after applying the tolerance
    #pin_number, distance_x, pin_pitch = int(pin_number), distance_x - 2*tolerance, pin_pitch - 2*tolerance
    if type_package == 'DIP':
        stencil_data[0] = int(stencil_data[0])
    if type_package == 'QFP':
        stencil_data[9] -= 2*stencil_data[10]
    stencil_data[3] -= 2*stencil_data[10]
    stencil_data[4] -= 2*stencil_data[10]
    match type_package:
        case 'DIP':
            model = generate_DIP(stencil_data)
            return model
        case 'QFP':
            model = generate_QFP(stencil_data)
            return model            

def get_min_max_value():                                                        #Loads the stencil min-max dimensions into a list from a .txt file in the workspace folder
    min_max_array = [0]*16
    file_path = os.getcwd() + '/data/min_max_values.txt' 
    file = open(file_path)
    j = 0
    for i in range(18):
        buffer = file.readline()
        if buffer not in ('MINIMUM VALUES (cm)\n', 'MAXIMUM VALUES (cm)\n'):
            index_0 = buffer.find('=')
            index_1 = buffer.find('\n')
            if index_1 == -1:
                index_1 = len(buffer)
            min_max_array[j] = float(buffer[index_0+1:index_1])
            j += 1
    file.close()
    min_max_array[0], min_max_array[8] = int(min_max_array[0]), int(min_max_array[8])
    return min_max_array

def integrity_control(stencil_data, min_max_value, package_type, window):       #Validates the data and block the stencil generation if errors exist (moreover, highlights red the incorrect one)
    pin_number, pin_length, pin_width, distance_x, pin_pitch = stencil_data[:5]
    n_pin_0, n_pin_1, n_pin_2, n_pin_3, distance_y, tolerance, stencil_height, margin_x, margin_y = stencil_data[5:]
    min_pin_number, min_pin_length, min_pin_width, min_dist_x, min_pin_pitch, min_height, min_margin_x, min_margin_y = min_max_value[:8]
    max_pin_number, max_pin_length, max_pin_width, max_dist_x, max_pin_pitch, max_height, max_margin_x, max_margin_y = min_max_value[8:]
    stencil_data_no_tolerance = stencil_data[:5] + stencil_data[11:]
    error_presence = False
    input_elements = [window['input_pin_number'], window['input_pin_length'], window['input_pin_width'], window['input_distance_x'], 
                      window['input_pin_pitch'], window['input_stencil_height'], window['input_margin_x'], window['input_margin_y']]
    match package_type:
        case 'DIP':
            #Checks for even pin number
            if (pin_number % 2) != 0:
                window['input_pin_number'].update(background_color = "#C93F3F")
                error_presence = True
                error_string = 'pin_number must be even in DIP packages.'
                window['log_window'].write('>>> ' + error_string + '\n')
            #Checks minimum and max pin number
            elif pin_number < min_pin_number:
                input_elements[0].update(background_color = "#C93F3F")
                error_presence = True
                error_string = 'pin_number below the minimum ' + '(' + str(min_max_value[0]) + ')'
                window['log_window'].write('>>> ' + error_string + '\n')
            elif pin_number > max_pin_number:
                input_elements[0].update(background_color = "#C93F3F")
                error_presence = True
                error_string = 'pin_number above the maximum ' + '(' + str(min_max_value[8]) + ')'
                window['log_window'].write('>>> ' + error_string + '\n')
            else:
                input_elements[0].update(background_color = "#FFFFFF")                  
            #Checks for values below or above the min/max value
            for i in range(1,8):
                if stencil_data_no_tolerance[i] < min_max_value[i]:
                    if not(pin_number == 2 and i == 4): 
                        input_elements[i].update(background_color = "#C93F3F")
                        error_presence = True
                        error_string = input_elements[i].key.replace('input_', '', 1) + ' below the minimum ' + '(' + str(min_max_value[i]*10) + ' mm)'
                        window['log_window'].write('>>> ' + error_string + '\n')
                elif stencil_data_no_tolerance[i] > min_max_value[i + 8]:
                    input_elements[i].update(background_color = "#C93F3F")
                    error_presence = True  
                    error_string = input_elements[i].key.replace('input_', '', 1) + ' above the maximum ' + '(' + str(min_max_value[i + 8]*10) + ' mm)'
                    window['log_window'].write('>>> ' + error_string + '\n')   
                else:
                    input_elements[i].update(background_color = "#FFFFFF")
            #Checks for tolerance issue
            if ((pin_pitch - 2*tolerance < min_pin_pitch) and pin_number != 2) or (distance_x - 2*tolerance < min_dist_x):
                    window['input_tolerance'].update(background_color = "#C93F3F")
                    error_presence = True  
                    error_string = 'Tolerance value too high'
                    window['log_window'].write('>>> ' + error_string + '\n')                
            else:
                    window['input_tolerance'].update(background_color = "#FFFFFF")
        case 'QFP':
            #Checks minimum distance x (calculated)
            if n_pin_0 >= n_pin_2:
                more_n_pin_vertical = n_pin_0
            else:
                more_n_pin_vertical = n_pin_2
            gap_vertical = distance_y - more_n_pin_vertical*pin_width - (more_n_pin_vertical - 1)*pin_pitch
            gap_vertical = math.trunc(gap_vertical * 100)/100
            if gap_vertical < 0:
                    window['input_distance_y'].update(background_color = "#C93F3F")
                    error_presence = True  
                    minimum_distance = math.trunc((more_n_pin_vertical*pin_width + (more_n_pin_vertical - 1)*pin_pitch)*10000)/1000
                    error_string = 'distance_y below the minimum ' + '(' + str(minimum_distance) + ' mm)'
                    window['log_window'].write('>>> ' + error_string + '\n')                
            else:
                    window['input_distance_y'].update(background_color = "#FFFFFF")
            #Checks minimum distance y (calculated)
            if n_pin_1 >= n_pin_3:
                more_n_pin_horizontal = n_pin_1
            else:
                more_n_pin_horizontal = n_pin_3
            gap_vertical = distance_x - more_n_pin_horizontal*pin_width - (more_n_pin_horizontal - 1)*pin_pitch
            gap_vertical = math.trunc(gap_vertical*100)/100
            if gap_vertical < 0:
                    window['input_distance_x'].update(background_color = "#C93F3F")
                    error_presence = True  
                    minimum_distance = math.trunc((more_n_pin_horizontal*pin_width + (more_n_pin_horizontal - 1)*pin_pitch)*10000)/1000
                    error_string = 'distance_x below the minimum ' + '(' + str(minimum_distance) + ' mm)'
                    window['log_window'].write('>>> ' + error_string + '\n')                
            else:
                    window['input_distance_x'].update(background_color = "#FFFFFF")
            #Checks for values below or above the min/max value
            stencil_data_no_tolerance[0] = n_pin_0 + n_pin_1 + n_pin_2 + n_pin_3
            for i in [0,1,2,4,5,6,7]:
                if stencil_data_no_tolerance[i] < min_max_value[i]:
                    error_presence = True
                    if i == 0:
                        window['input_pin_number_0'].update(background_color = "#C93F3F")
                        window['input_pin_number_1'].update(background_color = "#C93F3F")
                        window['input_pin_number_2'].update(background_color = "#C93F3F")
                        window['input_pin_number_3'].update(background_color = "#C93F3F")
                        window['log_window'].write('>>> Total pin number below the minimum ' + '(' + str(min_max_value[0]) + ')\n')
                    else:
                        input_elements[i].update(background_color = "#C93F3F")
                        error_string = input_elements[i].key.replace('input_', '', 1) + ' below the minimum ' + '(' + str(min_max_value[i]*10) + ' mm)'
                        window['log_window'].write('>>> ' + error_string + '\n')
                elif stencil_data_no_tolerance[i] > min_max_value[i + 8]:
                    error_presence = True
                    if i == 0:
                        window['input_pin_number_0'].update(background_color = "#C93F3F")
                        window['input_pin_number_1'].update(background_color = "#C93F3F")
                        window['input_pin_number_2'].update(background_color = "#C93F3F")
                        window['input_pin_number_3'].update(background_color = "#C93F3F")
                        window['log_window'].write('>>> Total pin number above the maximum ' + '(' + str(min_max_value[8]) + ')\n') 
                    else: 
                        input_elements[i].update(background_color = "#C93F3F")
                        error_string = input_elements[i].key.replace('input_', '', 1) + ' above the maximum ' + '(' + str(min_max_value[i + 8]*10) + ' mm)'
                        window['log_window'].write('>>> ' + error_string + '\n')   
                elif i == 0:
                    window['input_pin_number_0'].update(background_color = "#FFFFFF")
                    window['input_pin_number_1'].update(background_color = "#FFFFFF")
                    window['input_pin_number_2'].update(background_color = "#FFFFFF")
                    window['input_pin_number_3'].update(background_color = "#FFFFFF")
                else:
                    input_elements[i].update(background_color = "#FFFFFF")
            #Checks for tolerance issues
            if ((pin_pitch - 2*tolerance < min_pin_pitch) and (n_pin_0 > 1 or n_pin_1 > 1 or n_pin_2 > 1 or n_pin_3 > 1)) or (distance_x - 2*tolerance < min_dist_x) or (distance_y - 2*tolerance < min_dist_x):
                window['input_tolerance'].update(background_color = "#C93F3F")
                error_presence = True  
                error_string = 'Tolerance value too high'
                window['log_window'].write('>>> ' + error_string + '\n')                
            else:
                window['input_tolerance'].update(background_color = "#FFFFFF")
                
    return error_presence

def get_personalized_data(stencil_data, package_name, type_package):            #Saves the custom package data to the workspace folder
    #pin_number, pin_length, pin_width, distance_x, pin_pitch, n_pin_0, n_pin_1, n_pin_2, n_pin_3, distance_y, tolerance, stencil_height, margin_x, margin_y 
    stencil_data_local = [str(x) for x in stencil_data ] 
    match type_package:
        case 'DIP':
            path = os.getcwd() + '/data/' + type_package + '/'
            file = open(path + package_name + '.txt', 'w')
            file_content =  'pin_number='+stencil_data_local[0]+'\n'+'pin_length='+stencil_data_local[1]+'\n'+'pin_width='+stencil_data_local[2]+'\n'+'distance_x='+stencil_data_local[3]+'\n'+'pin_pitch='+stencil_data_local[4]
            file.write(file_content)
            file.close()
        case 'QFP':
            path = os.getcwd() + '/data/' + type_package + '/' 
            file = open(path + package_name + '.txt', 'w')
            file_content =  'pin_length=' + stencil_data_local[1] + '\n' + 'pin_width=' + stencil_data_local[2] + '\n' + 'distance_x=' + stencil_data_local[3] + '\n' + 'pin_pitch=' + stencil_data_local[4] + '\n' + 'pin_number_0=' + stencil_data_local[5] + '\n' + 'pin_number_1=' + stencil_data_local[6] + '\n' + 'pin_number_2=' + stencil_data_local[7] + '\n' + 'pin_number_3=' + stencil_data_local[8] + '\n' + 'distance_y=' + stencil_data_local[9]
            file.write(file_content)
            file.close()

def same_file_name(file_name, folder):                                          #Checks if there is a file with the same name in the same directory

    files = [f for f in os.listdir(folder) if f.endswith('.stl')]
    for file in files:
        path1 = folder + '/' + file
        path2 = folder + '/' + file_name + '.stl'
        try:
            if os.path.samefile(path1, path2):
                return True
        except FileNotFoundError:
            return False
    return False

def check_file_name(file_name):                                                 #Checks if the file name contains characters forbidden by Windows                                              
    if len(file_name) > 255:
        return False, '>>> File name too long.\n'
    if len(file_name) == 0:
        return False, '>>> File name cannot be empty.\n'
    if any((c in ['.', ',', '<', '>',':','"','/','\\','|','?','*']) for c in file_name):
        return False, '>>> File name cannot contain forbidden character.\n'
    else:
        return True, ''

def is_float(value):                                                            #Tries to convert a value in float, returns True if successful
    try:
        float(value)
        return True
    except ValueError:
        return False

def update_min_max_value_box(window, min_max_value, unit_constant):             #Updates the min-max input boxes with the elements from the provided list
    for event in MIN_MAX_VALUE_MAP:
        index, target_type = MIN_MAX_VALUE_MAP[event]
        if target_type == int:
            updated_value = min_max_value[index]
        else:
            updated_value = math.trunc(min_max_value[index] * unit_constant * 10000000) / 10000000
        window[event].update(value = updated_value)

def get_input_data_extreme(event, value, min_max_value_updated, unit_constant): #Retrieves the min-max list values entered by the user
    if event in MIN_MAX_VALUE_MAP:
        index, target_type = MIN_MAX_VALUE_MAP[event]
        if target_type == int:
            value = int(value)
        else:
            value = math.trunc((float(value) / unit_constant) * 10000000) / 10000000
        min_max_value_updated[index] = value
    return min_max_value_updated

def update_min_max_value_file(values):                                          #Updates the min-max file with the provided elements
    file_path = os.getcwd() + '/data/min_max_values.txt' 
    file = open(file_path, 'w')
    file_content = 'MINIMUM VALUES (cm)\n'+'min_n_pin='+str(values[0])+'\nmin_pin_length='+str(values[1])+'\nmin_pin_width='+str(values[2])+'\nmin_dist_x='+str(values[3])+'\nmin_pitch='+str(values[4])+'\nmin_h='+str(values[5])+'\nmin_margin_x='+str(values[6])+'\nmin_margin_y='+str(values[7])+'\nMAXIMUM VALUES (cm)\n'+'max_n_pin='+str(values[8])+'\nmax_pin_length='+str(values[9])+'\nmax_pin_width='+str(values[10])+'\nmax_dist_x='+str(values[11])+'\nmax_pitch='+str(values[12])+'\nmax_h='+str(values[13])+'\nmax_margin_x='+str(values[14])+'\nmax_margin_y='+str(values[15])
    file.write(file_content)
    file.close()

def get_date_time():                                                            #Gets current date and time and returns an ISO 8601 string format
    date = datetime.datetime.now()
    string = str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '_' + str(date.hour) + '-' + str(date.minute) + '-' + str(date.second)
    return string

def log_file_write(event, value, date_time, log_string = '', error = ''):       #First, create a log file for the current session, then write every event-pair to it, or eventually the error string
    file_path = os.getcwd() + '/log_files/' + date_time + '.txt'
    file = open(file_path, 'a')
    if event != '':
        try:
            file_content = 'event: ' + event.ljust(20) + ' value: ' + str(value) + '\n'
        except AttributeError:
            file_content = '\n\n\n"e quindi uscimmo a riveder le stelle"'
    else:
        file_content = f"log string: {log_string}"
    file.write(file_content)
    if error != '':
        file_content = f"error: {error}."
        file.write(file_content)
    file.close()

def log_write(log_window, date_time, log_string, error = ''):                   #Writes to both the log window and the log file
    log_window.write(log_string)
    log_file_write('','',date_time,log_string,error)