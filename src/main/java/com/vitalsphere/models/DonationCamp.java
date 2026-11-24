package com.vitalsphere.models;

import java.time.LocalDate;
import java.time.LocalTime;

/**
 * Blood donation camp entity mapped to Firestore collection 'camps'.
 */
public class DonationCamp {
    private String id;
    private String campTitle;
    private String organizerName;
    private String participatingBloodBank;
    private String state;
    private String district;
    private String city;
    private String venueAddress;
    private LocalDate campDate;
    private LocalTime startTime;
    private LocalTime endTime;
    private int targetUnits;
    private int registeredSlots;
    private int maxSlots;
    private String contactNumber;
    private String status; // UPCOMING, ACTIVE, COMPLETED, CANCELLED
    private boolean demoData = true;

    public DonationCamp() {}

    public DonationCamp(String id, String campTitle, String organizerName, String participatingBloodBank,
                        String state, String district, String city, String venueAddress,
                        LocalDate campDate, LocalTime startTime, LocalTime endTime, int maxSlots, String contactNumber) {
        this.id = id;
        this.campTitle = campTitle;
        this.organizerName = organizerName;
        this.participatingBloodBank = participatingBloodBank;
        this.state = state;
        this.district = district;
        this.city = city;
        this.venueAddress = venueAddress;
        this.campDate = campDate;
        this.startTime = startTime;
        this.endTime = endTime;
        this.maxSlots = maxSlots;
        this.registeredSlots = 0;
        this.contactNumber = contactNumber;
        this.status = "UPCOMING";
        this.demoData = true;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getCampTitle() { return campTitle; }
    public void setCampTitle(String campTitle) { this.campTitle = campTitle; }

    public String getOrganizerName() { return organizerName; }
    public void setOrganizerName(String organizerName) { this.organizerName = organizerName; }

    public String getParticipatingBloodBank() { return participatingBloodBank; }
    public void setParticipatingBloodBank(String participatingBloodBank) { this.participatingBloodBank = participatingBloodBank; }

    public String getState() { return state; }
    public void setState(String state) { this.state = state; }

    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }

    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    public String getVenueAddress() { return venueAddress; }
    public void setVenueAddress(String venueAddress) { this.venueAddress = venueAddress; }

    public LocalDate getCampDate() { return campDate; }
    public void setCampDate(LocalDate campDate) { this.campDate = campDate; }

    public LocalTime getStartTime() { return startTime; }
    public void setStartTime(LocalTime startTime) { this.startTime = startTime; }

    public LocalTime getEndTime() { return endTime; }
    public void setEndTime(LocalTime endTime) { this.endTime = endTime; }

    public int getTargetUnits() { return targetUnits; }
    public void setTargetUnits(int targetUnits) { this.targetUnits = targetUnits; }

    public int getRegisteredSlots() { return registeredSlots; }
    public void setRegisteredSlots(int registeredSlots) { this.registeredSlots = registeredSlots; }

    public int getMaxSlots() { return maxSlots; }
    public void setMaxSlots(int maxSlots) { this.maxSlots = maxSlots; }

    public String getContactNumber() { return contactNumber; }
    public void setContactNumber(String contactNumber) { this.contactNumber = contactNumber; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public boolean isDemoData() { return demoData; }
    public void setDemoData(boolean demoData) { this.demoData = demoData; }
}
