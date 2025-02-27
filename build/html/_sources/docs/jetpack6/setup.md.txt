# setup telelian l4t

## setup
- host는 ubuntu 20.04 또는 22.04를 사용하세요.
- telelian-l4t-jp6.tar.gz를 Linux_for_Tegra 폴더에서 압축해제 하세요.
- **주의사항**
    - build-setup.sh를 실행하기 전에 설치해야 할 패키지가 있습니다.
    - Jetpack6 (L4T 36.3)와 rootfs, toolchain 11.03이 준비되어 있어야 합니다. 
        - 이 링크를 참조하세요. https://developer.nvidia.com/embedded/jetson-linux-r363
    - Linux_for_Tegra, Toolchain 경로를 환경변수에 설정합니다.
    - 권한문제로 인해 ./build-setup.sh를 sudo로 실행하면 안됩니다.
    - 꼭 nvbuild.sh를 실행한 후 build-setup.sh를 실행하세요.

- Linux_for_Tegra와 rootfs, toolchain이 준비되었다면 아래의 명령어를 실행하세요.


```bash
sudo apt install -y git-core build-essential libncurses5-dev bc bison flex libssl-dev fakeroot device-tree-compiler qemu-user-static debootstrap sshpass abootimg libxml2-utils nfs-kernel-server xmlstarlet

export CROSS_COMPILER_PATH=/path/to/aarch64--glibc--stable-2022.08-1
export CROSS_COMPILE=$CROSS_COMPILER_PATH/bin/aarch64-buildroot-linux-gnu-
export ARCH=arm64
export L4T_PATH=/path/to/Linux_for_Tegra

cd $L4T_PATH/source
./source_sync.sh -t jetson_36.3
./nvbuild.sh

cd telelian-l4t-jp6
./build-setup.sh
```

- setup.sh의 실행이 완료되면 아래의 패키지가 준비됩니다.
    1. jetson Linux_for_Tegra
        - l4t kernel/dtb sources
        - avs200에 필요한 flashing 관련 tools       
    2. L4T rootfs
        - dtb overlay를 위한 tool
    3. telelian avs200 관련 source
        - gmsl driver
        - camera driver
        - avs200 device tree
        - camera device tree
    
## build
- build와 install을 위한 명령어는 아래와 같습니다.
```bash
cd $L4T_PATH/source

# defconfig
./maketegra kernel defconfig

# 전체 build
./maketegra

# dtb만 build
./maketegra dtbs

# dtb를 flash하기 위한 위치와 rootfs로 복사
sudo ./cpdtb

# kernel만 build
./maketegra kernel

# image를 flash하기 위한 위치와 rootfs로 복사
./cpkernel

# kernel module을 rootfs로 복사
sudo ./maketegra kernel_install

# nvidia oot module만 build
./maketegra modules

# nvidia oot module을 rootfs로 복사
sudo ./maketegra modules_install

# telelian cam만 build  
./maketegra telelian-cam modules

# telelian cam을 rootfs로 복사
sudo ./maketegra telelian-cam modules_install

```
## make rootfs
- build한 뒤에 cpdtb, cpkernel, kernel_install, modules_install, telelian-cam modules_install를 실행하면 rootfs에 필요한 파일들이 복사됩니다.
- nvidia l4t 기본 패키지를 설치하고 기본 user, passwd, hostname을 설정합니다.
```bash
cd $L4T_PATH
sudo ./apply_binaries.sh
sudo ./tools/l4t_create_default_user.sh -u <username> -p <password> -n <hostname> -a --accept-license
```

## flash
- flash를 위한 기본 폴더는 아래와 같습니다.
    - Linux_for_Tegra/
- flash를 위한 명령어는 아래와 같습니다.
- flash를 위해서는 host와 target을 연결하고 target을 recovery mode로 진입시켜야 합니다.
```bash
cd /path/to/Linux_for_Tegra/

# emmc에 flash
sudo ./flash_agx_orin_emmc.sh

# nvme에 flash
sudo ./flash_agx_orin_nvme.sh
```

## target device (avs200) 설정

### 최초 부팅 후 설정 
- avs200을 booting한 후 터미널에서 설정합니다.
- group설정
    ```bash
    sudo usermod -aG gpio <username>
    sudo usermod -aG i2c <username>
- camera overlay 설정
    ```bash
    cd /boot
    sudo ./makeoverlay_rootfs
    sudo reboot
    ```
- nvpmodel 설정
    - orin의 성능 설정을 최대로 설정합니다.
    - 설정 후 yes를 입력하면 재부팅됩니다.
    ```bash
    sudo nvpmodel -m 0
    ```
### l4t gstreamer 설치
```bash
sudo apt install nvidia-l4t-gstreamer
```

### jetpack 설치
```bash
sudo apt install nvidia-jetpack
```

### jtop 설치
```bash
sudo apt install python3-pip
sudo -H pip3 install -U jetson-stats
sudo systemctl restart jtop
```

### pwm 설정
- avs200의 pwm은 pwmchip3을 사용합니다.
- HZ에 원하는 주파수를 입력하면 됩니다.
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


### camera 확인
- camera overlay가 설정되어 있어야 합니다.

- preview
    - device=/dev/video 뒤의 숫자는 camera의 번호입니다.
    ```bash
    export DISPLAY=:0

    gst-launch-1.0 \
    nvv4l2camerasrc device=/dev/video0 \
    ! "video/x-raw(memory:NVMM),format=(string)UYVY,width=(int)3840,height=(int)2160,framerate=(fraction)30/1" \
    ! nvvidconv \
    ! "video/x-raw(memory:NVMM),format=(string)NV12" \
    ! nv3dsink sync=false -e
    ```

- jpeg capture
    - filesink location=test.jpg 뒤의 test.jpg외의 파일명을 입력하면 해당 파일명으로 저장됩니다.
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

