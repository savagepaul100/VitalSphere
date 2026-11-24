package com.vitalsphere.eligibility;

/**
 * Official Indian Blood Center reference statuses as specified in Section 7.
 */
public enum EligibilityStatus {
    PENDING("Pending Initial Review", "Awaiting donor submission or medical intake verification"),
    UNDER_REVIEW("Under Review", "Clinical screening in progress by authorized medical officer"),
    CLEARED_FOR_ASSESSMENT("Cleared for Assessment", "Meets initial health benchmarks, pending on-site physical check"),
    REQUIRES_ADDITIONAL_REVIEW("Requires Additional Review", "Minor anomaly detected, further clinical history needed"),
    TEMPORARILY_DEFERRED("Temporarily Deferred", "Donor temporarily in cooldown, recent medication, or transient condition"),
    PERMANENTLY_DEFERRED("Permanently Deferred", "Permanent disqualifying medical history for voluntary transfusion safety");

    private final String label;
    private final String description;

    EligibilityStatus(String label, String description) {
        this.label = label;
        this.description = description;
    }

    public String getLabel() {
        return label;
    }

    public String getDescription() {
        return description;
    }
}
