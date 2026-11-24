package com.vitalsphere.models;

import java.time.LocalDateTime;

/**
 * Blood Bank entity mapped to Firestore collection 'blood_banks'.
 */
public class BloodBank {
    private String id;
    private String name;
    private String licenseNumber;
    private String category; // Government, Red Cross, Charitable, Private
    private String state;
    private String district;
    private String city;
    private String address;
    private String contactNumber;
    private String email;
    private double latitude;
    private double longitude;
    private boolean componentSeparationAvailable;
    private boolean active = true;
    private boolean demoData = true;
    private LocalDateTime updatedAt = LocalDateTime.now();

    public BloodBank() {}

    public BloodBank(String id, String name, String licenseNumber, String category, String state,
                     String district, String city, String address, String contactNumber, String email) {
        this.id = id;
        this.name = name;
        this.licenseNumber = licenseNumber;
        this.category = category;
        this.state = state;
        this.district = district;
        this.city = city;
        this.address = address;
        this.contactNumber = contactNumber;
        this.email = email;
        this.componentSeparationAvailable = true;
        this.demoData = true;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getLicenseNumber() { return licenseNumber; }
    public void setLicenseNumber(String licenseNumber) { this.licenseNumber = licenseNumber; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public String getState() { return state; }
    public void setState(String state) { this.state = state; }

    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }

    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }

    public String getContactNumber() { return contactNumber; }
    public void setContactNumber(String contactNumber) { this.contactNumber = contactNumber; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public double getLatitude() { return latitude; }
    public void setLatitude(double latitude) { this.latitude = latitude; }

    public double getLongitude() { return longitude; }
    public void setLongitude(double longitude) { this.longitude = longitude; }

    public boolean isComponentSeparationAvailable() { return componentSeparationAvailable; }
    public void setComponentSeparationAvailable(boolean componentSeparationAvailable) { this.componentSeparationAvailable = componentSeparationAvailable; }

    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }

    public boolean isDemoData() { return demoData; }
    public void setDemoData(boolean demoData) { this.demoData = demoData; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
