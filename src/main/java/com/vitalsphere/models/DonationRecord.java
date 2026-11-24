package com.vitalsphere.models;

import java.time.LocalDate;

/**
 * Historical donation record mapped to Firestore collection 'donations'.
 */
public class DonationRecord {
    private String id;
    private String donorId;
    private String donorName;
    private BloodGroup bloodGroup;
    private BloodComponent component;
    private String bloodBankOrCamp;
    private LocalDate donationDate;
    private int unitsDonated;
    private String certificateUrl;
    private String status; // COMPLETED, REJECTED
    private boolean demoData = true;

    public DonationRecord() {}

    public DonationRecord(String id, String donorId, String donorName, BloodGroup bloodGroup,
                          BloodComponent component, String bloodBankOrCamp, LocalDate donationDate, int unitsDonated) {
        this.id = id;
        this.donorId = donorId;
        this.donorName = donorName;
        this.bloodGroup = bloodGroup;
        this.component = component;
        this.bloodBankOrCamp = bloodBankOrCamp;
        this.donationDate = donationDate;
        this.unitsDonated = unitsDonated;
        this.status = "COMPLETED";
        this.demoData = true;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getDonorId() { return donorId; }
    public void setDonorId(String donorId) { this.donorId = donorId; }

    public String getDonorName() { return donorName; }
    public void setDonorName(String donorName) { this.donorName = donorName; }

    public BloodGroup getBloodGroup() { return bloodGroup; }
    public void setBloodGroup(BloodGroup bloodGroup) { this.bloodGroup = bloodGroup; }

    public BloodComponent getComponent() { return component; }
    public void setComponent(BloodComponent component) { this.component = component; }

    public String getBloodBankOrCamp() { return bloodBankOrCamp; }
    public void setBloodBankOrCamp(String bloodBankOrCamp) { this.bloodBankOrCamp = bloodBankOrCamp; }

    public LocalDate getDonationDate() { return donationDate; }
    public void setDonationDate(LocalDate donationDate) { this.donationDate = donationDate; }

    public int getUnitsDonated() { return unitsDonated; }
    public void setUnitsDonated(int unitsDonated) { this.unitsDonated = unitsDonated; }

    public String getCertificateUrl() { return certificateUrl; }
    public void setCertificateUrl(String certificateUrl) { this.certificateUrl = certificateUrl; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public boolean isDemoData() { return demoData; }
    public void setDemoData(boolean demoData) { this.demoData = demoData; }
}
