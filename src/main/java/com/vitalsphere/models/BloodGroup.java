package com.vitalsphere.models;

import java.util.Arrays;
import java.util.List;

/**
 * Standard ABO and RhD blood group enumeration.
 */
public enum BloodGroup {
    O_NEGATIVE("O-", "O Negative"),
    O_POSITIVE("O+", "O Positive"),
    A_NEGATIVE("A-", "A Negative"),
    A_POSITIVE("A+", "A Positive"),
    B_NEGATIVE("B-", "B Negative"),
    B_POSITIVE("B+", "B Positive"),
    AB_NEGATIVE("AB-", "AB Negative"),
    AB_POSITIVE("AB+", "AB Positive");

    private final String code;
    private final String label;

    BloodGroup(String code, String label) {
        this.code = code;
        this.label = label;
    }

    public String getCode() {
        return code;
    }

    public String getLabel() {
        return label;
    }

    public static BloodGroup fromCode(String code) {
        if (code == null) return null;
        for (BloodGroup bg : values()) {
            if (bg.code.equalsIgnoreCase(code.trim()) || bg.name().equalsIgnoreCase(code.trim())) {
                return bg;
            }
        }
        return null;
    }
}
