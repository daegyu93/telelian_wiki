# Jetpack 6

## Setup

1. **호스트 시스템 준비**:
   - Ubuntu 20.04 또는 22.04를 사용하십시오.

2. **필수 파일 준비**:
   - `telelian-l4t-jp6.tar.gz` 파일을 `Linux_for_Tegra` 폴더 내에서 압축 해제하십시오.

```{warning}
**주의사항**:
   - `build-setup.sh`를 실행하기 전에 다음 패키지를 설치해야 합니다:
     ```bash
     sudo apt install -y git-core build-essential \
     libncurses5-dev bc bison flex libssl-dev fakeroot \
     device-tree-compiler qemu-user-static debootstrap \
     sshpass abootimg libxml2-utils nfs-kernel-server \
     xmlstarlet
     ```
   - JetPack 6 (L4T 36.3), rootfs, 그리고 toolchain 11.03이 필요합니다. 자세한 내용은 [NVIDIA Jetson Linux 36.3](https://developer.nvidia.com/embedded/jetson-linux-r363)을 참조하십시오.
   - `Linux_for_Tegra` 및 Toolchain 경로를 환경 변수로 설정해야 합니다:
     ```bash
     export CROSS_COMPILER_PATH=/path/to/aarch64--glibc--stable-2022.08-1
     export CROSS_COMPILE=$CROSS_COMPILER_PATH/bin/aarch64-buildroot-linux-gnu-
     export ARCH=arm64
     export L4T_PATH=/path/to/Linux_for_Tegra
     ```
   - 권한 문제로 인해 `./build-setup.sh`를 `sudo`로 실행하지 마십시오.
   - 반드시 `nvbuild.sh`를 실행한 후 `build-setup.sh`를 실행해야 합니다.
```

4. **소스 코드 동기화 및 빌드 설정**:
   ```bash
   cd $L4T_PATH/source
   ./source_sync.sh -t jetson_36.3
   ./nvbuild.sh

   cd telelian-l4t-jp6
   ./build-setup.sh
   ```

## Build

1. **빌드 및 설치 명령어**:
   ```bash
   cd $L4T_PATH/source

   # 기본 설정 적용
   ./maketegra kernel defconfig

   # 전체 빌드
   ./maketegra

   # DTB만 빌드
   ./maketegra dtbs

   # DTB를 플래시 위치와 rootfs로 복사
   sudo ./cpdtb

   # 커널만 빌드
   ./maketegra kernel

   # 커널 이미지를 플래시 위치와 rootfs로 복사
   sudo ./cpkernel

   # 커널 모듈을 rootfs로 복사
   sudo ./maketegra kernel_install

   # NVIDIA 외부 모듈만 빌드
   ./maketegra modules

   # NVIDIA 외부 모듈을 rootfs로 복사
   sudo ./maketegra modules_install

   # Telelian 카메라 모듈만 빌드
   ./maketegra telelian-cam modules

   # Telelian 카메라 모듈을 rootfs로 복사
   sudo ./maketegra telelian-cam modules_install
   ```

## Create root filesystem

1. **루트 파일 시스템에 필요한 파일 복사**:
   - 빌드 후 `cpdtb`, `cpkernel`, `kernel_install`, `modules_install`, `telelian-cam modules_install`을 실행하여 필요한 파일들을 rootfs에 복사합니다.

2. **NVIDIA L4T 기본 패키지 설치 및 사용자 설정**:
   ```bash
   cd $L4T_PATH
   sudo ./apply_binaries.sh
   sudo ./tools/l4t_create_default_user.sh -u <username> -p <password> -n <hostname> -a --accept-license
   ```

## Flashing

1. **플래시를 위한 기본 폴더**:
   - `Linux_for_Tegra/`

2. **플래시 명령어**:
   - 호스트와 타겟을 연결하고 타겟을 복구 모드로 진입시킨 후 실행합니다.
   ```bash
   cd /path/to/Linux_for_Tegra/

   # eMMC에 플래시
   sudo ./flash_agx_orin_emmc.sh

   # NVMe에 플래시
   sudo ./flash_agx_orin_nvme.sh
   ```

## Target device setup

### 최초 부팅 후 설정

1. **그룹 설정**:
   ```bash
   sudo usermod -aG gpio <username>
   sudo usermod -aG i2c <username>
   ```

2. **카메라 오버레이 설정**:
   ```bash
   cd /boot
   sudo ./makeoverlay_rootfs
   sudo reboot
   ```

3. **NVPModel 설정**:
   - Orin의 성능을 최대로 설정합니다.
   - 설정 후 `yes`를 입력하면 재부팅됩니다.
   ```bash
   sudo nvpmodel -m 0
   ```

### L4T GStreamer 설치

```bash
sudo apt install nvidia-l4t-gstreamer
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

### PWM 설정

- AVS200의 PWM은 `pwmchip3`을 사용합니다.
- 원하는 주파수를 `HZ` 변수에 설정합니다.
  ```bash
  BASE_PATH=/sys/class/pwm/pwmchip3
  # HZ=30
  HZ=20

  PERIOD=$((1000000000/$HZ))
  DUTY=$(($PERIOD/2))

  if [[ ! -d $BASE_PATH/pwm0 ]]; then
      echo 0 > $BASE_PATH/export
      sleep 1
  fi

  echo 0 > $BASE_PATH/pwm0/enable
  echo $PERIOD > $BASE_PATH/pwm0/period
  echo $DUTY > $BASE_PATH/pwm0/duty_cycle
  echo 1 > $BASE_PATH/pwm0/enable
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
   ! "video
::contentReference[oaicite:0]{index=0}
 
