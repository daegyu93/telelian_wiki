# Jetpack 5

## Setup

1. **호스트 시스템 준비**:
   - Ubuntu 20.04를 사용하십시오.

```{warning}
**주의사항**:
- `setup.sh`를 실행하기 전에 필요한 패키지를 설치해야 합니다.
- 권한 문제로 인해 `./setup.sh`를 `sudo`로 실행하면 안 됩니다. 실행 중간에 한 번 루트 비밀번호를 입력해야 합니다.
```
2. **필요한 패키지 설치 및 스크립트 실행**:

   ```bash
   sudo apt install git-core build-essential \
   libncurses5-dev bc bison flex libssl-dev fakeroot \
   device-tree-compiler
   ./setup.sh
   ```

3. **`setup.sh` 실행 완료 후 준비되는 패키지**:
   - **Jetson Linux_for_Tegra**:
     - L4T 커널 및 DTB 소스
     - AVS200에 필요한 플래싱 관련 도구
   - **L4T Root Filesystem**:
     - DTB 오버레이를 위한 도구
   - **Telelian AVS200 관련 소스**:
     - GMSL 드라이버
     - 카메라 드라이버
     - AVS200 디바이스 트리
     - 카메라 디바이스 트리

## Build

1. **소스 디렉토리 위치**:
   - 기본 경로: `$HOME/l4t_ws/Linux_for_Tegra/sources`

2. **빌드 및 설치 명령어**:

   ```bash
   cd $HOME/l4t_ws/Linux_for_Tegra/sources
    
   # 전체 빌드
   ./maketegra

   # DTB만 빌드
   ./maketegra dtbs

   # DTB를 플래싱 위치로 복사
   sudo ./cpdtb

   # 커널만 빌드
   ./maketegra Image

   # 커널 이미지를 플래싱 위치로 복사
   sudo ./cpkernel

   # 모듈만 빌드
   ./maketegra modules

   # 모듈을 루트 파일 시스템으로 복사
   sudo ./maketegra modules_install
   ```

## Flashing

1. **플래싱 디렉토리 위치**:
   - 기본 경로: `$HOME/l4t_ws/Linux_for_Tegra/`

2. **플래싱 전 준비사항**:
   - 호스트와 타겟을 연결하고, 타겟을 리커버리 모드로 진입시켜야 합니다.

3. **플래싱 명령어**:

   ```bash
   cd $HOME/l4t_ws/Linux_for_Tegra/
   sudo ./flash_agx_orin_nvme.sh
   ```

## Target device setup

### 최초 부팅 후 설정

1. **카메라 오버레이 설정**:

   ```bash
   cd /boot
   sudo ./makeoverlay_rootfs
   sudo reboot
   ```

2. **NVPModel 설정**:
   - Orin의 성능을 최대로 설정합니다.
   - 설정 후 `yes`를 입력하면 재부팅됩니다.

   ```bash
   sudo nvpmodel -m 0
   ```

### JetPack 설치

```bash
sudo apt install nvidia-jetpack
```

### JTop 설치

```bash
sudo apt install python3-pip
sudo -H pip3 install -U jetson-stats
sudo systemctl restart jtop
```

### 카메라 확인

- 카메라 오버레이가 설정되어 있어야 합니다.

1. **프리뷰**:
   - `device=/dev/video` 뒤의 숫자는 카메라 번호입니다.

   ```bash
   export DISPLAY=:0

   gst-launch-1.0 \
   nvv4l2camerasrc device=/dev/video0 \
   ! "video/x-raw(memory:NVMM),format=(string)UYVY,width=(int)3840,height=(int)2160,framerate=(fraction)30/1" \
   ! nvvidconv \
   ! "video/x-raw(memory:NVMM),format=(string)NV12" \
   ! nv3dsink sync=false -e
   ```

2. **JPEG 캡처**:
   - `filesink location=test.jpg`에서 `test.jpg`를 원하는 파일명으로 변경하여 저장할 수 있습니다.

   ```bash
   export DISPLAY=:0

   gst-launch-1.0 \
   nvv4l2camerasrc device=/dev/video0 num-buffers=1 \
   ! "video/x-raw(memory:NVMM),format=(string)UYVY,width=(int)3840,height=(int)2160,framerate=(fraction)30/1" \
   ! nvvidconv \
   ! "video/x-raw(memory:NVMM),format=(string)NV12" \
   ! nvjpegenc \
   ! filesink location=test.jpg
   ```
