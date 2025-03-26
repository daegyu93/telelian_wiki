# Camera overlay

```{important}
- avs 시리즈는 다양한 add-on board를 지원합니다.
- 다양한 보드와 카메라를 유연하게 설정하기 위한 안내입니다.
```
## Jetson Orin System

### AVS100, AVS200
- avs100과 avs200의 add-on board는 호환됩니다.
- avs100의 경우 Orin NX, nano의 csi port가 부족하여 4ch까지만 지원합니다.

| 보드  |  설명 |
|------|------|
| GCAM-R3   | GMSL 6ch rev3 |
| GCAM-R4   | GMSL 6ch rev4 |
| RGBIR-R1  | GMSL 6ch + RGB 1ch + IR 1ch |

### AVS101

| 보드  |  설명 |
|------|------|
| GCAM-R1  | GMSL 6ch |

## Camera
| 제조사 | 모델명 | 해상도 | 이미지 포맷 | 센서 | ISP |
|------|------|------|------|------|------|
| atech solution | acc02ong | 1920x1080 | YUV | onsemi ar0233  | geosemi gw5300 |
| sensing-world | sg2-imx390c | 1920x1080 | YUV | sony imx390  | geosemi gw5300 |
| sensing-world | sg3s-isx031c | 1920x1536 | YUV | sony isx031  | 센서 내장 |
| sensing-world | sg8-ox08bc | 3840x2160 | YUV | omnivision ox08b40 | geosemi gw5300 |


## Setup Camera Overlay
```{important}
- device tree를 avs, add-on board, camera에 맞게 overlay 설정을 해줘야 카메라가 동작합니다.
- /boot/makeoverlay_rootfs의 상단의 주석을 조합에 맞게 해제하세요
    - 예를 들어 GCAM-R4를 사용하고 sensing-world의 sg3s-isx031c 카메라를 사용하는 경우 아래와 같이 주석을 해제합니다.
        ```bash
        GCAM_BOARD=gcam-r4
        CAMERA=sg3s-isx031c
        ```
```

- /boot/makeoverlay_rootfs
```bash
#!/bin/bash

# select cam board
# GCAM_BOARD=gcam-r3
# GCAM_BOARD=gcam-r4
# GCAM_BOARD=gcam-rgbir-r1
# GCAM_BOARD=gcam-r1

# select camera
# CAMERA=acc02ong
# CAMERA=rgbir
# CAMERA=sg8-ox08bc-gw5300
# CAMERA=sg3s-isx031c
# CAMERA=sg2-imx390c-gw5200

COMPATIBLE=$(cat /proc/device-tree/compatible)

if [[ "$COMPATIBLE" == *"avs101"* ]]; then
    TARGET_PREFIX=avs101
elif [[ "$COMPATIBLE" == *"avs100"* ]]; then
    TARGET_PREFIX=avs100
elif [[ "$COMPATIBLE" == *"avs200"* ]]; then
    TARGET_PREFIX=avs200
else
    echo "Error: No target prefix found"
    exit 1
fi

IFS=' ' read -ra DATA <<< $(i2ctransfer -f -y 0 w1@0x50 0 r256)

if [ -z $DATA ];then
    echo "can't access"
    exit 1
fi

get_hex_to_dec()
{
    array=$@
    result=0
    ITER=0
    for i in ${array[@]}
    do
        val=$( printf "%d" ${i} )
        result=$(( result + (val<<(ITER*8)) ))
        ITER=$( expr $ITER + 1 )
    done
    DIGIT=$(( ITER * 2))
    case $DIGIT in
        2)
        result=$( printf "0x%02x" $result  )
        ;;
        4)
        result=$( printf "0x%04x" $result  )
        ;;
        6|8)
        result=$( printf "0x%08x" $result  )
        ;;
        *)
        echo digit error
        ;;
    esac
}

get_hex_to_dec ${DATA[0]} ${DATA[1]}

SOC_VERSION=$result

PARTNUM=$( echo ${DATA[@]:0x14:22} | xxd -r -p )
echo PARTNUM = $PARTNUM

SERIAL=$( echo ${DATA[@]:0x4a:13} | xxd -r -p )
echo SERIAL $SERIAL

PART_ARRAY=$( echo $PARTNUM | tr "-" "\n" )
IFS='- ' read -ra PART_ARRAY <<< $PARTNUM

MODULE_ID=${PART_ARRAY[1]:1}
SKU=${PART_ARRAY[2]}
FAB=${PART_ARRAY[3]}
REV=${PART_ARRAY[4]}

case $MODULE_ID in
    3701)
    case $SKU in
        0000)
        MODULE="AGX Orin"
        TARGET=avs200-agx-orin-64g
        ;;
        0004)
        MODULE="AGX Orin 32GB"
        TARGET=avs200-agx-orin-32g
        ;;
        0005)
        MODULE="AGX Orin 64GB"
        TARGET=avs200-agx-orin-64g
        ;;
        0008)
        MODULE="AGX Orin Industrial"
        TARGET=avs200-agx-orin-industrial
        ;;
    esac
    ;;
    3767)
    case $SKU in
        0000)
        MODULE="Orin NX 16GB"
        TARGET=$TARGET_PREFIX-orinnx-16g
        ;;
        0001)
        MODULE="Orin NX 8GB"
        TARGET=$TARGET_PREFIX-orinnx-8g
        ;;
        0003|0005)
        MODULE="Orin Nano 8GB"
        TARGET=$TARGET_PREFIX-orinnano-8g
        ;;
        0004)
        MODULE="Orin Nano 4GB"
        TARGET=$TARGET_PREFIX-orinnano-4g
        ;;
    esac
    ;;
esac

# echo module : $MODULE
# echo sku : $SKU
# echo fab : $FAB
# echo rev : $REV

FS_DEV=$(df -h / | grep "^/dev" | awk '{print $1}')

if [[ $FS_DEV = *"nvme"* ]];then
    FS_DEV=nvme
elif [[ $FS_DEV = *"mmcblk"* ]];then
    FS_DEV=emmc
else
    FS_DEV=unknown
fi

echo filesystem: $FS_DEV

if [[ $TARGET = "avs200-agx-orin"* ]]; then
    PREFIX=avs200
    EXT_LINUX_SRC="extlinux.conf.$PREFIX""_$FS_DEV.overlay"
elif [[ $TARGET = "avs100-orin"* ]]; then
    PREFIX=avs100
    EXT_LINUX_SRC="extlinux.conf.$PREFIX.overlay"
elif [[ $TARGET = "avs101-orin"* ]]; then
    PREFIX=avs101
    EXT_LINUX_SRC="extlinux.conf.$PREFIX.overlay"
fi
echo "target : $TARGET"

DTB_PATH=/boot
BOARD_DTB=$DTB_PATH/$TARGET.dtb
OUTPUT_DTB=$DTB_PATH/dtb/$TARGET-overlay.dtb

GCAM_DTB=$DTB_PATH/$PREFIX-$GCAM_BOARD-overlay.dtbo
CAMERA_DTB=$DTB_PATH/$PREFIX-$CAMERA-overlay.dtbo

OVERLAY_DTB_FILES=(
    tegra234-carveouts.dtbo
    tegra-optee.dtbo
)

OVERLAY_DTB_PATH=""

for OVERLAY_DTB_FILE in ${OVERLAY_DTB_FILES[@]}; do
    OVERLAY_DTB_PATH+="$DTB_PATH/$OVERLAY_DTB_FILE "
done
echo "additional overlay : $OVERLAY_DTB_PATH"

echo "board : $BOARD_DTB"
echo "gcam : $GCAM_DTB"
echo "camera : $CAMERA_DTB"
echo "overlay : $OUTPUT_DTB"
fdtoverlay -i $BOARD_DTB -o $OUTPUT_DTB $GCAM_DTB $CAMERA_DTB $OVERLAY_DTB_PATH 

if [[ ! -f $OUTPUT_DTB ]]; then
    echo "$OUTPUT_DTB is not exists."
    exit
fi

EXT_LINUX_SRC="/boot/$EXT_LINUX_SRC"

if [[ ! -f $EXT_LINUX_SRC ]]; then
    echo "$EXT_LINUX_SRC is not exists."
    exit
fi

# FDT 경로를 overlay dtb로 변경
sudo sed -i "s|FDT .*|FDT $OUTPUT_DTB|" $EXT_LINUX_SRC


DIFF_RESULT=$(diff $EXT_LINUX_SRC /boot/extlinux/extlinux.conf -q)

if [[ $DIFF_RESULT = *"differ"* ]]; then
    echo "extlinux.conf is updated."
    sudo mv /boot/extlinux/extlinux.conf /boot/extlinux/extlinux.conf.overlay_backup
    sudo cp $EXT_LINUX_SRC /boot/extlinux/extlinux.conf
else
    echo "extlinux.conf is already updated."
fi

echo "Done. reboot"
```

### run
- 아래 명령을 수행하고 재부팅 후 /dev/video* 장치들이 보이면 성공입니다.
```bash
cd /boot
sudo ./makeoverlay_rootfs
sudo reboot now
```
