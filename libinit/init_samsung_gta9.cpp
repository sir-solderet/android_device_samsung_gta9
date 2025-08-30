/*
 * Copyright (C) 2021 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <libinit_variant.h>
#include <libinit_utils.h>
#include <unistd.h>

//#include "vendor_init.h"

static std::vector<variant_info_t> variants = {
    {
        .hwc_value = "",
        .sku_value = "",
        .brand = "samsung",
        .device = "gta9",
        .marketname = "Galaxy Tab A9",
        .model = "SM-X115",
        .build_fingerprint = "samsung/gta9xx/gta9:15/AP3A.240905.015.A2/X115XXU4CYE5:user/release-keys"
    }
};

void vendor_load_properties() {
    if (access("/system/bin/recovery", F_OK) != 0) {
        search_variant(variants);
    }
}
