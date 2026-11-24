package com.vitalsphere.models;

import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Citizen blood emergency request mapped to Firestore collection 'blood_requests'.
 */
public class BloodRequest {
    private String id;
    private String patientName;
    private BloodGroup bloodGroup;
    private BloodComponent component;
    private int unitsRequired;
    private String hospitalName;
    private String hospitalAddress;
    private String state;
    private String district;
    private String city;
    private LocalDate requiredDate;
    private String contactPerson;
    private String contactNumber;
    private String urgency; // CRITICAL, URGENT, ROUTINE
    private String requestDescription;
    private String status; // SUBMITTED, APPROVED, ALLOCATED, FULFILLED, CLOSED
    private boolean demoData = true;
    private LocalDateTime createdAt = LocalDateTime.now();

    public BloodRequest() {}

    public BloodRequest(String id, String patientName, BloodGroup bloodGroup, BloodComponent component,
                        int unitsRequired, String hospitalName, String district, String city,
                        LocalDate requiredDate, String contactPerson, String contactNumber, String urgency) {
        this.id = id;
        this.patientName = patientName;
        this.bloodGroup = bloodGroup;
        this.component = component;
        this.unitsRequired = unitsRequired;
        this.hospitalName = hospitalName;
        this.state = "Andhra Pradesh";
        this.district = district;
        this.city = city;
        this.requiredDate = requiredDate;
        this.contactPerson = contactPerson;
        this.contactNumber = contactNumber;
        this.urgency = urgency;
        this.status = "APPROVED";
        this.demoData = true;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getPatientName() { return patientName; }
    public void setPatientName(String patientName) { this.patientName = patientName; }

    public BloodGroup getBloodGroup() { return bloodGroup; }
    public void setBloodGroup(BloodGroup bloodGroup) { this.bloodGroup = bloodGroup; }

    public BloodComponent getComponent() { return component; }
    public void setComponent(BloodComponent component) { this.component = component; }

    public int getUnitsRequired() { return unitsRequired; }
    public void setUnitsRequired(int unitsRequired) { this.unitsRequired = unitsRequired; }

    public String getHospitalName() { return hospitalName; }
    public void setHospitalName(String hospitalName) { this.hospitalName = hospitalName; }

    public String getHospitalAddress() { return hospitalAddress; }
    public void setHospitalAddress(String hospitalAddress) { this.hospitalAddress = hospitalAddress; }

    public String getState() { return state; }
    public void setState(String state) { this.state = state; }

    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }

    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    public LocalDate getRequiredDate() { return requiredDate; }
    public void setRequiredDate(LocalDate requiredDate) { this.requiredDate = requiredDate; }

    public String getContactPerson() { return contactPerson; }
    public void setContactPerson(String contactPerson) { this.contactPerson = contactPerson; }

    public String getContactNumber() { return contactNumber; }
    public void setContactNumber(String contactNumber) { this.contactNumber = contactNumber; }

    public String getUrgency() { return urgency; }
    public void setUrgency(String urgency) { this.urgency = urgency; }

    public String getRequestDescription() { return requestDescription; }
    public void setRequestDescription(String requestDescription) { this.requestDescription = requestDescription; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public boolean isDemoData() { return demoData; }
    public void setDemoData(boolean demoData) { this.demoData = demoData; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
