# Hardware And Power Plan

## Core Hardware

- Raspberry Pi 4
- 4WD 小車底盤
- 4 個 DC 馬達與輪子
- 馬達驅動板
- Raspberry Pi Camera
- USB 麥克風或 I2S 麥克風
- 小型喇叭或 USB / 3.5mm 音源輸出裝置
- 18650 鋰電池組
- 5V 降壓模組或 UPS 模組

## Recommended Module Roles

### Motor Driver

選擇原則：

- 要能獨立控制左右輪組方向
- 要能接受 Raspberry Pi 的 GPIO / PWM 訊號
- 要能承受馬達啟動電流

軟體層請封裝成：

- `set_speed(left, right)`
- `move_forward(speed)`
- `move_backward(speed)`
- `turn_left(speed)`
- `turn_right(speed)`
- `stop()`

### Power

供電建議分開：

- `RPi` 走穩定的 5V 輸出
- `Motor driver + motors` 使用獨立較高電流輸出
- 兩邊共地

原因：

- 馬達啟動瞬間電流波動大
- 若和 RPi 共用不穩定電源，容易導致 Raspberry Pi 重啟

### Camera

建議一開始固定使用：

- `640x480`
- `JPEG`
- 降低幀率

因為第一階段目標是穩定搜尋迴圈，不是高畫質串流。

## Suggested Future Sensors

第二階段之後可加入：

- 超音波測距，用於近距離避障
- IMU，用於估計轉向與姿態
- 編碼器，用於輪速估計與更穩定移動

## Hardware Bring-Up Order

建議不要一次全部接上，請按順序整合：

1. 先測 Raspberry Pi 開機、Wi-Fi、相機。
2. 再單獨測馬達驅動與四輪控制。
3. 再測麥克風錄音與喇叭播放。
4. 最後才整合整體任務流程。
