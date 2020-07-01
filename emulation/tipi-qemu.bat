"\Program Files\qemu\qemu-system-arm" ^
  -M versatilepb ^
  -cpu arm1176 ^
  -m 256M ^
  -drive file=sdimage.img,format=raw ^
  -net nic ^
  -net user,hostfwd=tcp::9900-:9900,hostfwd=tcp::9901-:9901,hostfwd=tcp::9922-:22 ^
  -dtb versatile-pb-buster.dtb ^
  -kernel kernel-qemu-4.19.50-buster ^
  -append "root=/dev/sda2 rootfstype=ext4 rw"
