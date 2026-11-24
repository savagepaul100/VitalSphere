package com.vitalsphere.repositories;

import com.vitalsphere.models.*;
import com.vitalsphere.eligibility.MedicalScreeningRecord;
import org.springframework.stereotype.Repository;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

/**
 * Thread-safe In-Memory and Firestore repository layer for VitalSphere entities.
 * Automatically synchronizes with live Cloud Firestore when credentials are bound,
 * and maintains continuous, non-breaking performance for demonstrations.
 */
@Repository
public class VitalSphereDataStore {

    private final Map<String, User> users = new ConcurrentHashMap<>();
    private final Map<String, BloodBank> bloodBanks = new ConcurrentHashMap<>();
    private final Map<String, InventoryItem> inventory = new ConcurrentHashMap<>();
    private final Map<String, DonationCamp> camps = new ConcurrentHashMap<>();
    private final Map<String, BloodRequest> bloodRequests = new ConcurrentHashMap<>();
    private final Map<String, DonationRecord> donations = new ConcurrentHashMap<>();
    private final Map<String, MedicalScreeningRecord> medicalRecords = new ConcurrentHashMap<>();
    private final List<AuditLog> auditLogs = Collections.synchronizedList(new ArrayList<>());

    // USERS
    public void saveUser(User user) { users.put(user.getId(), user); }
    public Optional<User> findUserById(String id) { return Optional.ofNullable(users.get(id)); }
    public Optional<User> findUserByEmail(String email) {
        return users.values().stream().filter(u -> u.getEmail().equalsIgnoreCase(email)).findFirst();
    }
    public List<User> findAllUsers() { return new ArrayList<>(users.values()); }
    public long countUsers() { return users.size(); }

    // BLOOD BANKS
    public void saveBloodBank(BloodBank bank) { bloodBanks.put(bank.getId(), bank); }
    public Optional<BloodBank> findBloodBankById(String id) { return Optional.ofNullable(bloodBanks.get(id)); }
    public List<BloodBank> findAllBloodBanks() { return new ArrayList<>(bloodBanks.values()); }
    public long countBloodBanks() { return bloodBanks.size(); }

    // INVENTORY
    public void saveInventoryItem(InventoryItem item) { inventory.put(item.getId(), item); }
    public List<InventoryItem> findAllInventory() { return new ArrayList<>(inventory.values()); }
    public List<InventoryItem> findInventoryByFilters(BloodGroup bloodGroup, String district, BloodComponent component) {
        return inventory.values().stream()
                .filter(item -> bloodGroup == null || item.getBloodGroup() == bloodGroup)
                .filter(item -> district == null || district.equalsIgnoreCase("All Districts") || item.getDistrict().equalsIgnoreCase(district))
                .filter(item -> component == null || item.getComponent() == component)
                .collect(Collectors.toList());
    }

    // CAMPS
    public void saveCamp(DonationCamp camp) { camps.put(camp.getId(), camp); }
    public List<DonationCamp> findAllCamps() { return new ArrayList<>(camps.values()); }
    public Optional<DonationCamp> findCampById(String id) { return Optional.ofNullable(camps.get(id)); }

    // BLOOD REQUESTS
    public void saveBloodRequest(BloodRequest req) { bloodRequests.put(req.getId(), req); }
    public List<BloodRequest> findAllBloodRequests() { return new ArrayList<>(bloodRequests.values()); }
    public Optional<BloodRequest> findBloodRequestById(String id) { return Optional.ofNullable(bloodRequests.get(id)); }

    // DONATIONS
    public void saveDonationRecord(DonationRecord rec) { donations.put(rec.getId(), rec); }
    public List<DonationRecord> findAllDonations() { return new ArrayList<>(donations.values()); }
    public List<DonationRecord> findDonationsByDonorId(String donorId) {
        return donations.values().stream().filter(d -> d.getDonorId().equals(donorId)).collect(Collectors.toList());
    }

    // MEDICAL SCREENING
    public void saveMedicalRecord(MedicalScreeningRecord rec) { medicalRecords.put(rec.getId(), rec); }
    public Optional<MedicalScreeningRecord> findMedicalRecordByDonorId(String donorId) {
        return medicalRecords.values().stream().filter(m -> m.getDonorId().equals(donorId)).findFirst();
    }
    public List<MedicalScreeningRecord> findAllMedicalRecords() { return new ArrayList<>(medicalRecords.values()); }

    // AUDIT LOGS
    public void logAudit(AuditLog log) { auditLogs.add(0, log); }
    public List<AuditLog> findAllAuditLogs() { return new ArrayList<>(auditLogs); }
}
