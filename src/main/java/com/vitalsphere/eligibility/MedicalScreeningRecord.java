package com.vitalsphere.eligibility;

import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Confidential medical screening record mapped to Firestore collection 'medical_records'.
 * Strictly masked and visible only to MEDICAL_OFFICER and SUPER_ADMIN.
 */
public class MedicalScreeningRecord {
    private String id;
    private String donorId;
    private String donorName;
    private int age;
    private double weightKg;
    private double hemoglobinGdl;
    private String bloodPressure;
    private int pulseBpm;
    private double temperatureCelsius;
    private boolean recentInfection;
    private boolean recentTattooOrPiercing;
    private boolean majorSurgeryPastSixMonths;
    private boolean underPrescriptionMedication;
    private LocalDate lastDonationDate;
    private EligibilityStatus status;
    private String medicalOfficerNotes;
    private String reviewingOfficerName;
    private boolean demoData = true;
    private LocalDateTime reviewedAt;

    public MedicalScreeningRecord() {}

    public MedicalScreeningRecord(String id, String donorId, String donorName, int age, double weightKg,
                                  double hemoglobinGdl, String bloodPressure, int pulseBpm,
                                  double temperatureCelsius, LocalDate lastDonationDate) {
        this.id = id;
        this.donorId = donorId;
        this.donorName = donorName;
        this.age = age;
        this.weightKg = weightKg;
        this.hemoglobinGdl = hemoglobinGdl;
        this.bloodPressure = bloodPressure;
        this.pulseBpm = pulseBpm;
        this.temperatureCelsius = temperatureCelsius;
        this.lastDonationDate = lastDonationDate;
        this.status = EligibilityStatus.CLEARED_FOR_ASSESSMENT;
        this.demoData = true;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getDonorId() { return donorId; }
    public void setDonorId(String donorId) { this.donorId = donorId; }

    public String getDonorName() { return donorName; }
    public void setDonorName(String donorName) { this.donorName = donorName; }

    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }

    public double getWeightKg() { return weightKg; }
    public void setWeightKg(double weightKg) { this.weightKg = weightKg; }

    public double getHemoglobinGdl() { return hemoglobinGdl; }
    public void setHemoglobinGdl(double hemoglobinGdl) { this.hemoglobinGdl = hemoglobinGdl; }

    public String getBloodPressure() { return bloodPressure; }
    public void setBloodPressure(String bloodPressure) { this.bloodPressure = bloodPressure; }

    public int getPulseBpm() { return pulseBpm; }
    public void setPulseBpm(int pulseBpm) { this.pulseBpm = pulseBpm; }

    public double getTemperatureCelsius() { return temperatureCelsius; }
    public void setTemperatureCelsius(double temperatureCelsius) { this.temperatureCelsius = temperatureCelsius; }

    public boolean isRecentInfection() { return recentInfection; }
    public void setRecentInfection(boolean recentInfection) { this.recentInfection = recentInfection; }

    public boolean isRecentTattooOrPiercing() { return recentTattooOrPiercing; }
    public void setRecentTattooOrPiercing(boolean recentTattooOrPiercing) { this.recentTattooOrPiercing = recentTattooOrPiercing; }

    public boolean isMajorSurgeryPastSixMonths() { return majorSurgeryPastSixMonths; }
    public void setMajorSurgeryPastSixMonths(boolean majorSurgeryPastSixMonths) { this.majorSurgeryPastSixMonths = majorSurgeryPastSixMonths; }

    public boolean isUnderPrescriptionMedication() { return underPrescriptionMedication; }
    public void setUnderPrescriptionMedication(boolean underPrescriptionMedication) { this.underPrescriptionMedication = underPrescriptionMedication; }

    public LocalDate getLastDonationDate() { return lastDonationDate; }
    public void setLastDonationDate(LocalDate lastDonationDate) { this.lastDonationDate = lastDonationDate; }

    public EligibilityStatus getStatus() { return status; }
    public void setStatus(EligibilityStatus status) { this.status = status; }

    public String getMedicalOfficerNotes() { return medicalOfficerNotes; }
    public void setMedicalOfficerNotes(String medicalOfficerNotes) { this.medicalOfficerNotes = medicalOfficerNotes; }

    public String getReviewingOfficerName() { return reviewingOfficerName; }
    public void setReviewingOfficerName(String reviewingOfficerName) { this.reviewingOfficerName = reviewingOfficerName; }

    public boolean isDemoData() { return demoData; }
    public void setDemoData(boolean demoData) { this.demoData = demoData; }

    public LocalDateTime getReviewedAt() { return reviewedAt; }
    public void setReviewedAt(LocalDateTime reviewedAt) { this.reviewedAt = reviewedAt; }
}
