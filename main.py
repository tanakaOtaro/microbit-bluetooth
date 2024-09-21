def RC():
    global speed, gear, turn, wait
    # 受信データ　：　0(指令無し)
    # ギア状態　　：　0(前後進無し)　なら
    # If received data is 0 (no command) ,
    # and gear is 0 (no forward/reverse movement)...
    # 
    # 受信データ　：　555(前進指令)　なら
    # If received data is 555 (forward command)...
    # 
    # 受信データ　：　666(後進指令)　なら
    # If received data is 666 (reverse command)...
    # 
    # 受信データ　：　-180~180(旋回指令)　なら
    # If received data is between -180 and 180...
    # 
    # 受信データ　：　999(受信無し)
    # ギア状態　　：　0(前後進無し)　なら
    # If received data is 999 (no signal) and gear is 0 (no forward/reverse movement)...
    if webvalue == "b" and gear == 0:
        # モーターをブレーキする
        # Brakes the motors.
        STOP()
    elif webvalue == "w":
        # ギア状態　　：　0(前後進無し)　なら
        # If gear is 0 (no forward/reverse movement)...
        # 
        # ギア状態　　：　1(低速前進中) なら
        # If gear is 1 (moving slowly forward)...
        # 
        # ギア状態　　：　-1または-2(後進中) なら
        # If gear is -1 or -2 (moving in reverse)...
        if gear == 0:
            # ブレーキを解除する
            # Releases brakes.
            MOVE()
            # 低速で前進する
            # Moves robot slowly forward.
            speed = 895
            # ギアを1に設定する
            # Changes gear to 1.
            gear = 1
        elif gear == 1:
            # ブレーキを解除する
            # Releases brakes.
            MOVE()
            # 最大速度で前進する
            # Moves robot forward at maximum speed.
            speed = 1023
            # ギアを2に設定する
            # Changes gear to 2.
            gear = 2
        elif gear < 0:
            # モーターをブレーキする
            # Brakes the motors.
            STOP()
            # ギアを0にリセットする
            # Resets gear to 0.
            gear = 0
    elif webvalue == "s":
        # ギア状態　　：　0(前後進無し)　なら
        # If gear is 0 (no forward/reverse movement)...
        # 
        # ギア状態　　：　-1(低速後進中)　なら
        # If gear is -1 (moving slowly in reverse)...
        # 
        # ギア状態　　：　1または2(前進中)　なら
        # If gear is 1 or 2 (moving forward)...
        if gear == 0:
            # ブレーキを解除する
            # Releases brakes.
            MOVE()
            # 低速で後進する
            # Moves robot slowly in reverse.
            speed = 127
            # ギアを-1に設定する
            # Changes gear to -1.
            gear = -1
        elif gear == -1:
            # ブレーキを解除する
            # Releases brakes.
            MOVE()
            # 最大速度で後進する
            # Moves robot in reverse at maximum speed.
            speed = 0
            # ギアを-2に設定する
            # Changes gear to -2.
            gear = -2
        elif gear > 0:
            # モーターをブレーキする
            # Brakes the motors.
            STOP()
            # ギアを0にリセットする
            # Resets gear to 0.
            gear = 0
    elif webvalue == "a" or "d":
        # ブレーキを解除する
        # Releases brakes.
        MOVE()
        # ギア状態　　：　0(前後進無し)
        # 1または2(前進中)　なら
        # If gear is 0 (no forward/reverse movement), or 1/2 (moving forward)...
        if webvalue == "d":
            # そのまま旋回する
            # Turns the robot.
            turn = RadioData * 10
        else:
            # 反対方向に旋回する
            # Turns the robot in the other direction.
            turn = RadioData * -10
    elif gear == 0:
        RunTime = 0
        # 1秒以上受信できていないなら
        # If no signal is received for 1 second...
        if 1000 < input.running_time() - RunTime:
            # モーターをブレーキする
            # Brakes the motors.
            STOP()
    # 待機時間を指定する
    # (単位はミリ秒)
    # Defines waiting time (unit = milliseconds)
    wait = 0
    # 受信データを999にリセットする
    # Resets received data to 999.
    RadioData = 999

def on_bluetooth_connected():
    basic.show_icon(IconNames.HAPPY)
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_icon(IconNames.ASLEEP)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def STOP():
    global speed, turn
    # 右モーターをブレーキする
    # Applies brake to right motor.
    pins.digital_write_pin(DigitalPin.P15, 1)
    # 左モーターをブレーキする
    # Applies brake to left motor.
    pins.digital_write_pin(DigitalPin.P16, 1)
    # 前後進しない
    # No forward or reverse movement.
    speed = 511
    # 旋回しない
    # No turning.
    turn = 0

def on_uart_data_received():
    global webvalue
    webvalue = bluetooth.uart_read_until(serial.delimiters(Delimiters.NEW_LINE))
    basic.show_string(webvalue)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.NEW_LINE),
    on_uart_data_received)

def MOVE():
    # 右モーターのブレーキを解除する
    # Unbrakes right motor.
    pins.digital_write_pin(DigitalPin.P15, 0)
    # 左モーターのブレーキを解除する
    # Unbrakes left motor.
    pins.digital_write_pin(DigitalPin.P16, 0)
wait = 0
turn = 0
speed = 0
gear = 0
webvalue = ""
bluetooth.start_led_service()
basic.show_string("DEMO")
webvalue = "neutral"
STOP()
# モーターを停止する
# Stops the motors.
pins.analog_write_pin(AnalogPin.P13, 511)
# モーターを停止する
# Stops the motors.
pins.analog_write_pin(AnalogPin.P14, 511)
# モーターに送る信号の初期設定
# Resets signal sent to motor.
pins.analog_set_period(AnalogPin.P13, 1000)
# モーターに送る信号の初期設定
# Resets signal sent to motor.
pins.analog_set_period(AnalogPin.P14, 1000)
basic.show_string("N")

def on_forever():
    RC()
    pins.analog_write_pin(AnalogPin.P13, Math.constrain(speed - turn, 0, 1023))
    pins.analog_write_pin(AnalogPin.P14, Math.constrain(speed + turn, 0, 1023))
    basic.pause(wait)
basic.forever(on_forever)
