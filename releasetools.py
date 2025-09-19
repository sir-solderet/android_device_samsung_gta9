#
# Copyright (C) 2009 The Android Open Source Project
# Copyright (C) 2019 The LineageOS Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import common

SUPPORTED_MODELS = ["SM-X115"]
SUPPORTED_DEVICE = "gta9"

def FullOTA_InstallBegin(info):
    # Force file-based OTA (avoid block-based AssertionError)
    common.OPTIONS.block_based = False
    info.script.Print("⚡ Using file-based OTA for gta9 (SM-X115)")

def FullOTA_Assertions(info):
    OTA_Assertions(info)
    return

def IncrementalOTA_Assertions(info):
    OTA_Assertions(info)
    return

def FullOTA_InstallEnd(info):
    OTA_InstallEnd(info)
    info.script.Print("✅ Installation complete for SM-X115 (gta9)")
    return

def IncrementalOTA_InstallEnd(info):
    OTA_InstallEnd(info)
    info.script.Print("✅ Incremental OTA install complete for SM-X115 (gta9)")
    return

def AddImage(info, basename, dest):
    """Add an image from IMAGES/ into the OTA package and extract it to target block."""
    name = basename
    data = info.input_zip.read("IMAGES/" + basename)
    common.ZipWriteStr(info.output_zip, name, data)
    info.script.AppendExtra('package_extract_file("%s", "%s");' % (name, dest))

def OTA_InstallEnd(info):
    info.script.Print("📦 Patching firmware images...")
    # Flash dtbo.img
    AddImage(info, "dtbo.img", "/dev/block/bootdevice/by-name/dtbo")
    return

def OTA_Assertions(info):
    # Assert model and device
    info.script.AssertOemProperty("ro.boot.em.model", SUPPORTED_MODELS, True)
    info.script.AppendExtra(
        'assert(getprop("ro.product.device") == "{0}" || '
        'getprop("ro.build.product") == "{0}");'.format(SUPPORTED_DEVICE)
    )
    info.script.Print("✅ Target device verified: gta9 (SM-X115)")
    return
