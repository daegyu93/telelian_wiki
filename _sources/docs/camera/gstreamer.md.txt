# gstreamer
```{important}
- [Camera Overlay](overlay.md)가 설정되어 있어야 합니다.
```

## preview
- device=/dev/video 뒤의 숫자는 camera의 번호입니다.
```bash
export DISPLAY=:0
WIDTH=3840
HEIGHT=2160

gst-launch-1.0 \
nvv4l2camerasrc device=/dev/video0 \
! "video/x-raw(memory:NVMM),format=(string)UYVY,width=(int)$WIDTH,height=(int)$HEIGHT,framerate=(fraction)30/1" \
! nvvidconv \
! "video/x-raw(memory:NVMM),format=(string)NV12" \
! nv3dsink sync=false -e
```

## jpeg capture
- filesink location=test.jpg 뒤의 test.jpg외의 파일명을 입력하면 해당 파일명으로 저장됩니다.
```bash 
export DISPLAY=:0
WIDTH=3840
HEIGHT=2160

gst-launch-1.0 \
nvv4l2camerasrc device=/dev/video0 num-buffers=1 \
! "video/x-raw(memory:NVMM),format=(string)UYVY,width=(int)$WIDTH,height=(int)$HEIGHT,framerate=(fraction)30/1" \
! nvvidconv \
! "video/x-raw(memory:NVMM),format=(string)NV12" \
! nvjpegenc \
! filesink location=test.jpg
```