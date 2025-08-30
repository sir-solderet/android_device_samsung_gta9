
# Samsung Galaxy Tab A9 (gta9) Device Tree

This repository contains the device tree for building custom ROMs, such as LineageOS, for the Samsung Galaxy Tab A9 (gta9).

## Device Specifications

| Feature              | Specification                      |
|----------------------|-------------------------------------|
| **Chipset**          | MediaTek Helio G99 (6nm)            |
| **CPU**              | Octa-core                         |
| **GPU**              | Mali-G57 MC2                       |
| **Display**          | 8.7-inch TFT                      |
| **RAM**              | 4GB / 6GB / 8GB                   |
| **Storage**          | 64GB / 128GB / 128GB              |
| **Battery**          | 5100mAh                           |
| **Launch Android Version** | Android 13                  |
| **Treble Support**   | Yes (GSI Compatible)              |

## Repository Contents

This repository includes:
- **Device-specific configurations**: Required to build a custom ROM for the Samsung Galaxy Tab A9.
- **Vendor blobs**: Proprietary files necessary for hardware functionality (if linked separately).
- **Build scripts and configuration files**: For compiling the kernel and ROM.

## Kernel Information

The source kernel for this device is not included in this repository. Refer to the appropriate kernel source from Samsung's Open Source Release Center or other kernel repositories.

## How to Build

### Prerequisites

1. A Linux-based build environment with the necessary tools installed.
2. LineageOS source synced for the target Android version (e.g., `lineage-22.2`).

### Steps

1. **Initialize LineageOS Repository**
   ```bash
   repo init -u https://github.com/LineageOS/android.git -b lineage-22.2
   repo sync --force-sync -j$(nproc)
   ```

2. **Clone Device Tree**
   ```bash
   git clone https://github.com/sir-solderet/android_device_samsung_gta9.git -b main device/samsung/gta9
   ```

3. **Clone Kernel and Vendor Trees**
   (If needed, replace `<kernel-repo>` and `<vendor-repo>` with actual URLs.)
   ```bash
   git clone <kernel-repo> kernel/samsung/gta9
   git clone https://github.com/sir-solderet/vendor_samsung_gta9.git -b main vendor/samsung/gta9
   ```

4. **Set Up Build Environment**
   ```bash
   source build/envsetup.sh
   lunch lineage_gta9-bp1a-userdebug
   ```

5. **Build the ROM**
   ```bash
   make bacon -j$(nproc)
   ```

6. **Locate the Built ROM**
   After a successful build, the output will be located in:
   ```
   out/target/product/gta9/
   ```
