package com.vitalsphere.models;

import com.vitalsphere.security.UserRole;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Core User entity mapped to Firestore collection 'users'.
 */
public class User {
    private String id;
    private String fullName;
    private String email;
    private String mobileNumber;
    private LocalDate dateOfBirth;
    private String gender; // MALE, FEMALE, OTHER
    private String address;
    private String state;
    private String district;
    private String city;
    private String pincode;
    private BloodGroup bloodGroup;
    private UserRole role;
    private boolean identityVerified;
    private String verificationStatus; // PENDING, VERIFIED, REJECTED
    private boolean demoData = true;
    private LocalDateTime createdAt = LocalDateTime.now();

    public User() {}

    public User(String id, String fullName, String email, String mobileNumber, LocalDate dateOfBirth,
                String gender, String state, String district, String city, BloodGroup bloodGroup, UserRole role) {
        this.id = id;
        this.fullName = fullName;
        this.email = email;
        this.mobileNumber = mobileNumber;
        this.dateOfBirth = dateOfBirth;
        this.gender = gender;
        this.state = state;
        this.district = district;
        this.city = city;
        this.bloodGroup = bloodGroup;
        this.role = role;
        this.identityVerified = true;
        this.verificationStatus = "VERIFIED";
        this.demoData = true;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getMobileNumber() { return mobileNumber; }
    public void setMobileNumber(String mobileNumber) { this.mobileNumber = mobileNumber; }

    public LocalDate getDateOfBirth() { return dateOfBirth; }
    public void setDateOfBirth(LocalDate dateOfBirth) { this.dateOfBirth = dateOfBirth; }

    public String getGender() { return gender; }
    public void setGender(String gender) { this.gender = gender; }

    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }

    public String getState() { return state; }
    public void setState(String state) { this.state = state; }

    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }

    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    public String getPincode() { return pincode; }
    public void setPincode(String pincode) { this.pincode = pincode; }

    public BloodGroup getBloodGroup() { return bloodGroup; }
    public void setBloodGroup(BloodGroup bloodGroup) { this.bloodGroup = bloodGroup; }

    public UserRole getRole() { return role; }
    public void setRole(UserRole role) { this.role = role; }

    public boolean isIdentityVerified() { return identityVerified; }
    public void setIdentityVerified(boolean identityVerified) { this.identityVerified = identityVerified; }

    public String getVerificationStatus() { return verificationStatus; }
    public void setVerificationStatus(String verificationStatus) { this.verificationStatus = verificationStatus; }

    public boolean isDemoData() { return demoData; }
    public void setDemoData(boolean demoData) { this.demoData = demoData; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
