#
# Copyright (C) 2024 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import common

def FullOTA_Assertions(info):
  """Asserts that the device is the correct model. This is a crucial safety check."""

  info.Print("Checking for target device...")

  # This is the standard and most reliable way to check the device model.
  # It prevents the ROM from being installed on any device that isn't a 'gta9'.
  info.script.AppendExtra('assert(getprop("ro.product.device") == "gta9" || getprop("ro.build.product") == "gta9");')
  return


def FullOTA_InstallEnd(info):
  """Post-install actions. Not needed for this build as there's no special firmware."""

  info.Print("Device patching complete.")
  return


def IncrementalOTA_Assertions(info):
  """Assertions for incremental OTAs. Not used for initial bringup."""
  pass


def IncrementalOTA_InstallEnd(info):
  """Post-install actions for incremental OTAs. Not used for initial bringup."""
  pass
