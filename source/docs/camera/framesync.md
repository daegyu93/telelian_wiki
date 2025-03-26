
# frame sync pwm 설정

## avs200
- avs200의 fsync는 pwmchip3을 사용합니다.
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

