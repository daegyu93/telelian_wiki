# frame sync pwm 설정


## avs100
- avs100의 framesync는 pwmchip2을 사용합니다.
- HZ에 원하는 주파수를 입력하면 됩니다.
```bash
BASE_PATH=/sys/class/pwm/pwmchip2
HZ=30

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

## avs101
- avs101의 framesync는 i2c 7 bus에 연결된 Micom pwm generator를 이용합니다.
```bash
HZ=30

i2cset -y 7 0x44 1 $HZ
```


## avs200
- avs200의 framesync는 pwmchip3을 사용합니다.
- HZ에 원하는 주파수를 입력하면 됩니다.
```bash
BASE_PATH=/sys/class/pwm/pwmchip3
HZ=30

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

