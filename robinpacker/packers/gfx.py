import array

def writeDiscreteRun(output, discrete_values):
    length = len(discrete_values)
    slice_start = 0
    while length:
        min_length = min(length, 0x7F)
        output.append(min_length)
        output.extend(discrete_values[slice_start:slice_start + min_length])
        length -= min_length
        slice_start += min_length

def writeRepeatingRun(output, repeating_value, repeating_length):
    while repeating_length:
        min_length = min(repeating_length, 0x7F)
        output.append(min_length | 0x80)
        output.append(repeating_value)
        repeating_length -= min_length

def encodeGfx(gfx_data):
    output = array.array('B')
    last_val = None
    repeating_run = False
    repeating_value = None
    repeating_length = 0
    discrete_run = False
    tmp_values = array.array('B')
    for val in gfx_data.data:
        if last_val is None:
            last_val = val
            continue
        if last_val == val:
            if discrete_run:
#                if len(tmp_values):
#                    del tmp_values[-1]
                writeDiscreteRun(output, tmp_values)
#                tmp_values = array.array('B')
            if not repeating_run:
                repeating_length = 1
            discrete_run = False
            repeating_run = True
            repeating_value = val
            repeating_length += 1
        else:
            if repeating_run:
                writeRepeatingRun(output, repeating_value, repeating_length)
                discrete_run = True
                repeating_run = False
                repeating_value = None
                repeating_length = 0
            else:
                if not discrete_run:
#                    tmp_values = array.array('B')
                    tmp_values.append(last_val)
                discrete_run = True
                tmp_values.append(val)

        last_val = val

    if repeating_run:
        writeRepeatingRun(output, repeating_value, repeating_length)
    elif discrete_run:
        writeDiscreteRun(output, tmp_values)

    output.append(0xFF)
    return output
