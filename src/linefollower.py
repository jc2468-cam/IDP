#1 left, 1 right, 1 middle sensor. 
#1 left, 1 right, 1 middle sensor. 

def linefollower():
    
    # black = 0, white = 1

    while True:
        sll = sensor.ll
        sl = sensor.l
        sr = sensor.r
        srr = sensor.rr

        while True:
            if srr == 0 and sll == 0:
                if sl == 0 and sr == 0:
                    motor.r = 1
                    motor.l = 1
                    break
            if sr == 1:
                motor.r = 0.5
                motor.l = 1
                break
            if sl == 1:
                motor.l = 0.5
                motor.r = 1

            if sll == 1 or srr == 1:
                
                while True:
                    sll = sensor.ll
                    sl = sensor.l
                    sr = sensor.r
                    srr = sensor.rr

                    if sll == 0 and srr == 0:
                        break

                    while True:
                        if sll == 1 and sl == 1:
                            #90 degree left turn
                            while srr != 0 and sll != 0:
                                motor.l = -1
                                motor.r = 1
                            break

                        if sll == 1 and sl == 1:
                            #90 degree right turn
                            while srr != 0 and sll != 0:
                                motor.r = -1
                                motor.l = 1
                            break

    
