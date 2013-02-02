def writeToArray(values, output, repeating_run):
    length = len(values)
    while length > 0:
        rle_byte = min(length, 0x7F)
        if repeating_run:
            rle_byte &= 0x80
        output.extend(values) # TODO: check if this method exists
        length -= min(length, 0x7F)

def encodeGfx(gfx_data):
    output = array.array('B')
    last_val = None
    repeating_run = False
    discrete_run = False
    tmp_values = array.array('B')
    for val in gfx_data.data:
        # If last val is different
            # Are we already in a repeating run?
                # end it
                # start a new discrete run
                # (special case for the first value?)
            # Are we already in a discrete run?
                # continue it
            # Else
                # start a new discrete run? (special case for first value?)
        # If last val is the same
            # Are we already in a repeating run?
                # continue it
            # Are we already in a discrete run?
                # end it
                # start a new repeating run
            # Else
                # start a new repeating run

        if val != last_val:
            if repeating_run:
                writeToArray(tmp_values, output, repeating_run)
                repeating_run = False
                discrete_run = True
                tmp_values = array.array('B')


        # Use RLE flag is 0x80
        # run length is masked with 0x7F

        # End with 0xFF


        runLength = ord(input_file.read(1))
        if runLength == 0xFF:
            break
        useRLE = runLength & 0x80
        runLength &= 0x7F
        endpos = len(output) + runLength
        if endpos >= max_size:
            runLength -= endpos
            if not runLength:
                break
        if useRLE:
            val = ord(input_file.read(1))
            for i in xrange(runLength):
                output.append(val)
        else:
            for i in xrange(runLength):
                val = ord(input_file.read(1))
                output.append(val)
    # Fill in pixels until we get to the maximum position.
    while len(output) < max_size:
        output.append(0x00)
    return output
