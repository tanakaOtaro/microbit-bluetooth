/**
 * w：前進
 * 
 * s：後退
 * 
 * a：左回転
 * 
 * d：右回転
 * 
 * b：ブレーキ
 */
function RC () {
    let RunTime: number;
let RadioData: number;
// 受信データを999にリセットする
    // Resets received data to 999.
    RadioData = 1023
    // 受信データ　：　0(指令無し)
    // ギア状態　　：　0(前後進無し)　なら
    // If received data is 0 (no command) ,
    // and gear is 0 (no forward/reverse movement)...
    // 
    // 受信データ　：　555(前進指令)　なら
    // If received data is 555 (forward command)...
    // 
    // 受信データ　：　666(後進指令)　なら
    // If received data is 666 (reverse command)...
    // 
    // 受信データ　：　-180~180(旋回指令)　なら
    // If received data is between -180 and 180...
    // 
    // 受信データ　：　999(受信無し)
    // ギア状態　　：　0(前後進無し)　なら
    // If received data is 999 (no signal) and gear is 0 (no forward/reverse movement)...
    if (webvalue == "b" || webvalue == "N") {
        // モーターをブレーキする
        // Brakes the motors.
        STOP()
    } else if (webvalue == "w") {
        // ブレーキを解除する
        // Releases brakes.
        MOVE()
        // 旋回しない
        // No turning.
        turn = 0
        // 低速で前進する
        // Moves robot slowly forward.
        speed = 895
    } else if (webvalue == "s") {
        // 旋回しない
        // No turning.
        turn = 0
        // 低速で後進する
        // Moves robot slowly in reverse.
        speed = 127
    } else if (webvalue == "a" || webvalue == "d") {
        // ブレーキを解除する
        // Releases brakes.
        MOVE()
        // ギア状態　　：　0(前後進無し)
        // 1または2(前進中)　なら
        // If gear is 0 (no forward/reverse movement), or 1/2 (moving forward)...
        if (webvalue == "d") {
            // そのまま旋回する
            // Turns the robot.
            turn = RadioData * 1
        } else {
            // 反対方向に旋回する
            // Turns the robot in the other direction.
            turn = RadioData * -1
        }
    }
}
bluetooth.onBluetoothConnected(function () {
    basic.showIcon(IconNames.Happy)
})
bluetooth.onBluetoothDisconnected(function () {
    basic.showIcon(IconNames.Asleep)
})
function STOP () {
    // 右モーターをブレーキする
    // Applies brake to right motor.
    pins.digitalWritePin(DigitalPin.P15, 1)
    // 左モーターをブレーキする
    // Applies brake to left motor.
    pins.digitalWritePin(DigitalPin.P16, 1)
    // 前後進しない
    // No forward or reverse movement.
    speed = 511
    // 旋回しない
    // No turning.
    turn = 0
}
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    webvalue = bluetooth.uartReadUntil(serial.delimiters(Delimiters.NewLine))
    basic.showString(webvalue)
})
function MOVE () {
    // 右モーターのブレーキを解除する
    // Unbrakes right motor.
    pins.digitalWritePin(DigitalPin.P15, 0)
    // 左モーターのブレーキを解除する
    // Unbrakes left motor.
    pins.digitalWritePin(DigitalPin.P16, 0)
}
let speed = 0
let turn = 0
let webvalue = ""
basic.showString("DEMO")
webvalue = "neutral"
STOP()
// モーターを停止する
// Stops the motors.
pins.analogWritePin(AnalogPin.P13, 511)
// モーターを停止する
// Stops the motors.
pins.analogWritePin(AnalogPin.P14, 511)
// モーターに送る信号の初期設定
// Resets signal sent to motor.
pins.analogSetPeriod(AnalogPin.P13, 1000)
// モーターに送る信号の初期設定
// Resets signal sent to motor.
pins.analogSetPeriod(AnalogPin.P14, 1000)
basic.showString("N")
basic.forever(function () {
    let wait = 0
    RC()
    pins.analogWritePin(AnalogPin.P13, Math.constrain(speed - turn, 0, 1023))
    pins.analogWritePin(AnalogPin.P14, Math.constrain(speed + turn, 0, 1023))
    basic.pause(wait)
})
