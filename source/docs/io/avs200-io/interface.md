# Interface

## UART

보드 우측에는 두 개의 4핀 헤더가 있습니다.

### UART1

- **디바이스 경로**: `/dev/ttyTHS0`

### UART2

- **디바이스 경로**: `/dev/ttyAMA0`


(can-interface-section)=
## CAN

CAN 포트의 하드웨어 설정은 [CANFD 섹션](canfd.md#canfd-section) 를 참조하세요

부팅 시 `mttcan` 모듈이 로드되지 않으므로 수동으로 로드해야 합니다.

### 모듈 로드

```bash
sudo modprobe mttcan
ifconfig -a
```

위 명령을 실행하면 `can0`과 `can1` 인터페이스가 표시됩니다.

### 테스트 (FD 모드: 예시로 baudrate 500k, dbitrate 2M 설정)

```bash
sudo ip link set can0 up type can bitrate 500000 dbitrate 2000000 fd on
sudo ip link set can1 up type can bitrate 500000 dbitrate 2000000 fd on
```

- **CAN 데이터 수신**:

  ```bash
  candump -c -c -ta can0
  ```

- **CAN 데이터 송신**:

  ```bash
  cansend can0 123##512345678
  ```

  - `123`: CAN ID
  - `5`: 플래그 (1자리 16진수)
  - `12345678`: 데이터 (짝수 개의 16진수)

FD 모드를 사용하지 않을 경우, `dbitrate` 설정은 필요하지 않습니다. 예를 들어, baudrate를 500k로 설정하려면 다음과 같이 입력합니다.

```bash
sudo ip link set can0 up type can bitrate 500000
```