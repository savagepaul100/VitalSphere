package com.vitalsphere.security;

/**
 * 10 Strict Role-Based Access Control (RBAC) definitions matching Section 10 of specification.
 */
public enum UserRole {
    SUPER_ADMIN("Super Administrator", "Full platform access across all modules, configurations, and audits"),
    NATIONAL_AUTHORITY("National Authority", "National analytics, regulatory oversight and policy dashboards"),
    STATE_AUTHORITY("State Authority", "Oversight and reporting for assigned state"),
    DISTRICT_AUTHORITY("District Authority", "Oversight and coordination for assigned district"),
    BLOOD_BANK_ADMIN("Blood Bank Administrator", "Manage authorized blood center, inventory, and staff"),
    MEDICAL_OFFICER("Medical Officer", "Review confidential clinical screening records, deferrals, and donor fitness"),
    CAMP_ORGANIZER("Camp Organizer", "Coordinate blood donation camps, slots, and verify attendee attendance"),
    SUPPORT_STAFF("Support Staff", "Handle citizen queries, request routing, and platform support"),
    DONOR("Voluntary Donor", "Public features, donor profile, donation cooldown, and appointments"),
    RECIPIENT("Recipient / Citizen", "Public search, submit emergency requests, and view compatibility");

    private final String displayName;
    private final String description;

    UserRole(String displayName, String description) {
        this.displayName = displayName;
        this.description = description;
    }

    public String getDisplayName() {
        return displayName;
    }

    public String getDescription() {
        return description;
    }

    public String getAuthority() {
        return "ROLE_" + this.name();
    }
}
