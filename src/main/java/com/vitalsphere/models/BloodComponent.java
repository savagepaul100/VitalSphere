package com.vitalsphere.models;

/**
 * Standard blood component classifications.
 */
public enum BloodComponent {
    WHOLE_BLOOD("Whole Blood", 35),
    PACKED_RED_CELLS("Packed Red Blood Cells (PRBC)", 42),
    FRESH_FROZEN_PLASMA("Fresh Frozen Plasma (FFP)", 365),
    PLATELET_CONCENTRATE("Random Donor Platelets (RDP)", 5),
    SINGLE_DONOR_PLATELET("Single Donor Platelets (SDP/Apheresis)", 5),
    CRYOPRECIPITATE("Cryoprecipitate", 365);

    private final String displayName;
    private final int shelfLifeDays;

    BloodComponent(String displayName, int shelfLifeDays) {
        this.displayName = displayName;
        this.shelfLifeDays = shelfLifeDays;
    }

    public String getDisplayName() {
        return displayName;
    }

    public int getShelfLifeDays() {
        return shelfLifeDays;
    }
}
