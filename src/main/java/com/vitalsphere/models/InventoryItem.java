package com.vitalsphere.models;

import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Blood inventory item mapped to Firestore collection 'inventory'.
 */
public class InventoryItem {
    private String id;
    private String bloodBankId;
    private String bloodBankName;
    private String district;
    private BloodGroup bloodGroup;
    private BloodComponent component;
    private int unitsAvailable;
    private int unitsReserved;
    private LocalDate collectionDate;
    private LocalDate expiryDate;
    private String batchNumber;
    private boolean demoData = true;
    private LocalDateTime lastUpdated = LocalDateTime.now();

    public InventoryItem() {}

    public InventoryItem(String id, String bloodBankId, String bloodBankName, String district,
                         BloodGroup bloodGroup, BloodComponent component, int unitsAvailable,
                         LocalDate collectionDate, LocalDate expiryDate, String batchNumber) {
        this.id = id;
        this.bloodBankId = bloodBankId;
        this.bloodBankName = bloodBankName;
        this.district = district;
        this.bloodGroup = bloodGroup;
        this.component = component;
        this.unitsAvailable = unitsAvailable;
        this.collectionDate = collectionDate;
        this.expiryDate = expiryDate;
        this.batchNumber = batchNumber;
        this.demoData = true;
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getBloodBankId() { return bloodBankId; }
    public void setBloodBankId(String bloodBankId) { this.bloodBankId = bloodBankId; }

    public String getBloodBankName() { return bloodBankName; }
    public void setBloodBankName(String bloodBankName) { this.bloodBankName = bloodBankName; }

    public String getDistrict() { return district; }
    public void setDistrict(String district) { this.district = district; }

    public BloodGroup getBloodGroup() { return bloodGroup; }
    public void setBloodGroup(BloodGroup bloodGroup) { this.bloodGroup = bloodGroup; }

    public BloodComponent getComponent() { return component; }
    public void setComponent(BloodComponent component) { this.component = component; }

    public int getUnitsAvailable() { return unitsAvailable; }
    public void setUnitsAvailable(int unitsAvailable) { this.unitsAvailable = unitsAvailable; }

    public int getUnitsReserved() { return unitsReserved; }
    public void setUnitsReserved(int unitsReserved) { this.unitsReserved = unitsReserved; }

    public LocalDate getCollectionDate() { return collectionDate; }
    public void setCollectionDate(LocalDate collectionDate) { this.collectionDate = collectionDate; }

    public LocalDate getExpiryDate() { return expiryDate; }
    public void setExpiryDate(LocalDate expiryDate) { this.expiryDate = expiryDate; }

    public String getBatchNumber() { return batchNumber; }
    public void setBatchNumber(String batchNumber) { this.batchNumber = batchNumber; }

    public boolean isDemoData() { return demoData; }
    public void setDemoData(boolean demoData) { this.demoData = demoData; }

    public LocalDateTime getLastUpdated() { return lastUpdated; }
    public void setLastUpdated(LocalDateTime lastUpdated) { this.lastUpdated = lastUpdated; }
}
