# Interface

## UART

보드 우측에는 두 개의 4핀 헤더가 있습니다.

### UART1

- **디바이스 경로**: `/dev/ttyTHS0`

### UART2

- **디바이스 경로**: `/dev/ttyAMA0`

현재 기본 설정으로 `/dev/ttyAMA0`가 디버그 UART로 지정되어 있어, 설정을 변경하지 않으면 디버그 메시지가 출력됩니다. 일반 UART로 사용하려면 `extlinux.conf` 파일을 수정해야 합니다.

```bash
sudo vim /boot/extlinux/extlinux.conf
# APPEND 라인에서 "console=ttyAMA0,115200" 구문 제거
```

## LAN

LAN LED가 비정상적으로 동작하며, LAN2의 MAC 주소가 재부팅 시마다 변경되는 문제가 있습니다. 이를 해결하려면 아래 링크의 스크립트를 다운로드하여 설치해야 합니다.

[avs200_eth_conf](https://gitlab.com/telelian-jetpack/util/avs200_eth_conf)

```bash
git clone https://gitlab.com/telelian-jetpack/util/avs200_eth_conf.git
cd avs200_eth_conf
./install.sh
```

(can-interface-section)=
CAN

CAN 포트의 하드웨어 설정은 제조사의 공식 문서를 참고하시기 바랍니다.

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

H/W configuration은 [CANFD 섹션](canfd.md#canfd-section)