#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.."; pwd)
PREBUILT="$ROOT/prebuilt"
OUTDIR="$ROOT/out"
mkdir -p "$OUTDIR"

# Prefer recovery.img, fall back to boot.img
RECOVERYIMG="$PREBUILT/recovery.img"
BOOTIMG="$PREBUILT/boot.img"
VENDORBOOT="$PREBUILT/vendor_boot.img"
ARGS_MK="$OUTDIR/bootimg-args.mk"

IMG=""
if [[ -f "$RECOVERYIMG" ]]; then
  IMG="$RECOVERYIMG"
  echo "Using recovery.img for kernel + args"
elif [[ -f "$BOOTIMG" ]]; then
  IMG="$BOOTIMG"
  echo "Using boot.img for kernel + args"
else
  echo "Missing prebuilt/recovery.img or prebuilt/boot.img" >&2
  exit 1
fi

rm -f "$ARGS_MK"

write_arg() {
  local key="$1"
  local val="$2"
  if [[ "$key" == BOARD_MKBOOTIMG_ARGS* ]]; then
    echo "$key += $val" >>"$ARGS_MK"
  else
    echo "$key := $val" >>"$ARGS_MK"
  fi
}

if command -v unpack_bootimg >/dev/null 2>&1; then
  unpack_bootimg --boot_img "$IMG" --out "$OUTDIR" >/dev/null || true
  [[ -f "$OUTDIR/kernel" ]] && cp -f "$OUTDIR/kernel" "$PREBUILT/kernel"
  [[ -f "$OUTDIR/dtb" ]] && cp -f "$OUTDIR/dtb" "$PREBUILT/dtb"

  MKARGS=$(unpack_bootimg --boot_img "$IMG" --format=mkbootimg || true)
  set -- $MKARGS
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --header_version) shift; write_arg BOARD_BOOTIMG_HEADER_VERSION "$1" ;;
      --base) shift; write_arg BOARD_KERNEL_BASE "$1" ;;
      --pagesize) shift; write_arg BOARD_KERNEL_PAGESIZE "$1" ;;
      --cmdline) shift; write_arg BOARD_MKBOOTIMG_ARGS "--cmdline \"$1\"" ;;
      --board) shift; write_arg BOARD_MKBOOTIMG_ARGS "--board \"$1\"" ;;
      --kernel_offset) shift; write_arg BOARD_MKBOOTIMG_ARGS "--kernel_offset $1" ;;
      --ramdisk_offset) shift; write_arg BOARD_MKBOOTIMG_ARGS "--ramdisk_offset $1" ;;
      --tags_offset) shift; write_arg BOARD_MKBOOTIMG_ARGS "--tags_offset $1" ;;
      --dtb_offset) shift; write_arg BOARD_MKBOOTIMG_ARGS "--dtb_offset $1" ;;
    esac
    shift || true
  done
else
  # Fallback: magiskboot
  command -v magiskboot >/dev/null 2>&1 || { echo "Need unpack_bootimg or magiskboot"; exit 1; }
  magiskboot unpack -h "$IMG" >"$OUTDIR/boot.hdr"
  magiskboot unpack "$IMG" >/dev/null
  [[ -f kernel ]] && mv -f kernel "$PREBUILT/kernel"
  [[ -f dtb ]] && mv -f dtb "$PREBUILT/dtb"

  BASE=$(grep -oE 'base=0x[0-9a-f]+' "$OUTDIR/boot.hdr" | head -1 | cut -d= -f2)
  PAGESIZE=$(grep -oE 'pagesize=[0-9]+' "$OUTDIR/boot.hdr" | head -1 | cut -d= -f2)
  HV=$(grep -oE 'header=[0-9]+' "$OUTDIR/boot.hdr" | sed 's/header=//')
  CMDLINE=$(grep -oE 'cmdline=.*' "$OUTDIR/boot.hdr" | sed 's/cmdline=//' | sed 's/\"/\\\"/g')
  BOARD=$(grep -oE 'board=.*' "$OUTDIR/boot.hdr" | sed 's/board=//')

  [[ -n "$HV" ]] && write_arg BOARD_BOOTIMG_HEADER_VERSION "$HV"
  [[ -n "$BASE" ]] && write_arg BOARD_KERNEL_BASE "$BASE"
  [[ -n "$PAGESIZE" ]] && write_arg BOARD_KERNEL_PAGESIZE "$PAGESIZE"
  [[ -n "$CMDLINE" ]] && write_arg BOARD_MKBOOTIMG_ARGS "--cmdline \"$CMDLINE\""
  [[ -n "$BOARD" ]] && write_arg BOARD_MKBOOTIMG_ARGS "--board \"$BOARD\""
fi

# If vendor_boot exists, force header version 4
if [[ -f "$VENDORBOOT" ]]; then
  sed -i '/BOARD_BOOTIMG_HEADER_VERSION/d' "$ARGS_MK" || true
  echo "BOARD_BOOTIMG_HEADER_VERSION := 4" >>"$ARGS_MK"
fi

echo "Generated $ARGS_MK"

