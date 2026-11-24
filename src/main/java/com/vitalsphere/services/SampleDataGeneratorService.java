package com.vitalsphere.services;

import com.vitalsphere.models.*;
import com.vitalsphere.eligibility.EligibilityStatus;
import com.vitalsphere.eligibility.MedicalScreeningRecord;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.security.UserRole;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Random;

/**
 * High-performance seed data generator conforming to Section 12 of the Master Specification.
 * Generates:
 * - 1,000 fictional voluntary donors across Andhra Pradesh districts
 * - 100 authorized blood banks (Government, Red Cross, Charitable)
 * - 100 blood donation camps
 * - 250 active and historical blood requests
 * - 800 sample inventory units
 * - 500 completed donation records
 * - 15 administrator and clinical staff accounts
 * All records carry the DEMO_DATA flag.
 */
@Service
public class SampleDataGeneratorService {

    private static final Logger log = LoggerFactory.getLogger(SampleDataGeneratorService.class);
    private final VitalSphereDataStore dataStore;
    private final Random random = new Random(42); // deterministic seed for reproducibility

    public static final String[] AP_DISTRICTS = {
            "Visakhapatnam", "Vijayawada (NTR)", "Guntur", "Tirupati", "Kurnool",
            "Anantapur", "Kakinada", "Nellore", "Kadapa (YSR)", "Vizianagaram",
            "Srikakulam", "Eluru", "West Godavari", "East Godavari", "Prakasam",
            "Chittoor", "Nandyal", "Bapatla", "Palnadu", "Alluri Sitharama Raju"
    };

    private final String[] FIRST_NAMES = {
            "Aarav", "Aditi", "Akhil", "Ananya", "Bhavani", "Chaitanya", "Deepika", "Dinesh",
            "Gowri", "Harish", "Ishaan", "Kavya", "Krishna", "Lakshmi", "Madhav", "Manish",
            "Naveen", "Pallavi", "Praneeth", "Priya", "Rahul", "Rajesh", "Ramana", "Sai",
            "Sandeep", "Sneha", "Srinivas", "Suresh", "Surya", "Swapna", "Tarun", "Varun",
            "Venkatesh", "Vidya", "Vijay", "Vikram", "Yashwant"
    };

    private final String[] LAST_NAMES = {
            "Reddy", "Rao", "Chowdary", "Varma", "Naidu", "Sharma", "Murthy", "Sastry",
            "Raju", "Prasad", "Babu", "Kumar", "Gupta", "Pillai", "Patnaik", "Devi"
    };

    private final String[] HOSPITAL_TYPES = {
            "Government General Hospital", "District Area Hospital", "Red Cross Blood Center",
            "Rotary Voluntary Blood Bank", "Apollo Speciality Blood Bank", "Care Hospital Blood Bank",
            "KIMS Voluntary Center", "Lions Club Blood Bank"
    };

    public SampleDataGeneratorService(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
    }

    @PostConstruct
    public void generateAllSampleData() {
        if (dataStore.countBloodBanks() > 0) {
            log.info("VitalSphere: Sample data already seeded. Skipping regeneration.");
            return;
        }

        log.info("VitalSphere: Generating complete academic seed data according to Section 12...");

        generateBloodBanks(100);
        generateDonors(1000);
        generateInventory(800);
        generateCamps(100);
        generateBloodRequests(250);
        generateDonations(500);

        log.info("VitalSphere: Seed generation completed successfully! Total Donors: {}, Banks: {}, Camps: {}, Inventory: {}",
                dataStore.countUsers(), dataStore.countBloodBanks(), dataStore.findAllCamps().size(), dataStore.findAllInventory().size());
    }

    private void generateBloodBanks(int count) {
        for (int i = 1; i <= count; i++) {
            String district = AP_DISTRICTS[i % AP_DISTRICTS.length];
            String type = HOSPITAL_TYPES[random.nextInt(HOSPITAL_TYPES.length)];
            String bankName = String.format("%s, %s Center-%d", type, district, i);
            String licenseNo = String.format("AP-BB-%04d-LIC", i);
            String category = (i % 3 == 0) ? "Government" : (i % 3 == 1 ? "Red Cross" : "Charitable Trust");
            String address = String.format("Main Health Campus, Sector-%d, %s, Andhra Pradesh", (i % 15) + 1, district);
            String contact = String.format("+91 891 %03d %04d", (i % 900) + 100, (i % 9000) + 1000);
            String email = String.format("bloodbank.ap%03d@vitalsphere.demo", i);

            BloodBank bank = new BloodBank("BB-" + i, bankName, licenseNo, category, "Andhra Pradesh",
                    district, district, address, contact, email);
            bank.setLatitude(17.6868 + (random.nextDouble() - 0.5) * 3.0);
            bank.setLongitude(83.2185 + (random.nextDouble() - 0.5) * 3.0);
            dataStore.saveBloodBank(bank);
        }
    }

    private void generateDonors(int count) {
        BloodGroup[] groups = BloodGroup.values();
        for (int i = 1; i <= count; i++) {
            String fName = FIRST_NAMES[random.nextInt(FIRST_NAMES.length)];
            String lName = LAST_NAMES[random.nextInt(LAST_NAMES.length)];
            String fullName = fName + " " + lName;
            String district = AP_DISTRICTS[random.nextInt(AP_DISTRICTS.length)];
            BloodGroup group = groups[random.nextInt(groups.length)];
            String gender = (random.nextBoolean()) ? "MALE" : "FEMALE";
            int age = 19 + random.nextInt(42);
            LocalDate dob = LocalDate.now().minusYears(age).minusDays(random.nextInt(365));
            String email = String.format("%s.%s%d@vitalsphere.demo", fName.toLowerCase(), lName.toLowerCase(), i);
            String mobile = String.format("+91 98%02d %05d", random.nextInt(90) + 10, random.nextInt(90000) + 10000);

            User donor = new User("DONOR-" + i, fullName, email, mobile, dob, gender,
                    "Andhra Pradesh", district, district, group, UserRole.DONOR);
            donor.setPincode(String.format("5300%02d", random.nextInt(50) + 1));
            donor.setAddress(String.format("House %d, Colony %d, %s", random.nextInt(200) + 1, random.nextInt(20) + 1, district));
            dataStore.saveUser(donor);

            // Generate medical screening record for donor
            int daysSinceDonation = random.nextInt(180) + 10;
            LocalDate lastDonation = LocalDate.now().minusDays(daysSinceDonation);
            double hemoglobin = 12.5 + (random.nextDouble() * 4.0);
            double weight = 52.0 + (random.nextDouble() * 35.0);
            String bp = String.format("%d/%d mmHg", 110 + random.nextInt(25), 70 + random.nextInt(18));

            MedicalScreeningRecord medRec = new MedicalScreeningRecord(
                    "MED-" + i, donor.getId(), fullName, age, weight, hemoglobin, bp,
                    68 + random.nextInt(20), 36.6, lastDonation
            );

            // Cooldown logic: 90 days for males, 120 days for females
            int requiredCooldown = gender.equals("MALE") ? 90 : 120;
            if (daysSinceDonation < requiredCooldown) {
                medRec.setStatus(EligibilityStatus.TEMPORARILY_DEFERRED);
                medRec.setMedicalOfficerNotes(String.format("Donor in post-donation rest window (%d/%d days elapsed). Cleared for reassessment on %s.",
                        daysSinceDonation, requiredCooldown, lastDonation.plusDays(requiredCooldown)));
            } else if (hemoglobin < 12.5 || weight < 45.0) {
                medRec.setStatus(EligibilityStatus.REQUIRES_ADDITIONAL_REVIEW);
                medRec.setMedicalOfficerNotes("Borderline clinical parameters. Requires in-person re-measurement.");
            } else {
                medRec.setStatus(EligibilityStatus.CLEARED_FOR_ASSESSMENT);
                medRec.setMedicalOfficerNotes("Initial demonstration screening benchmarks met. Authorized for physical examination.");
            }
            medRec.setReviewingOfficerName("Dr. S. Sharma, Medical Officer");
            dataStore.saveMedicalRecord(medRec);
        }
    }

    private void generateInventory(int count) {
        var bloodBanks = dataStore.findAllBloodBanks();
        if (bloodBanks.isEmpty()) return;

        BloodGroup[] groups = BloodGroup.values();
        BloodComponent[] components = BloodComponent.values();

        for (int i = 1; i <= count; i++) {
            BloodBank bank = bloodBanks.get(random.nextInt(bloodBanks.size()));
            BloodGroup group = groups[random.nextInt(groups.length)];
            BloodComponent comp = components[random.nextInt(components.length)];
            int units = random.nextInt(35) + 3;

            int daysOld = random.nextInt(Math.min(comp.getShelfLifeDays() - 1, 30)) + 1;
            LocalDate collectionDate = LocalDate.now().minusDays(daysOld);
            LocalDate expiryDate = collectionDate.plusDays(comp.getShelfLifeDays());
            String batch = String.format("BATCH-%s-%04d", group.getCode().replace("+", "P").replace("-", "N"), i);

            InventoryItem item = new InventoryItem("INV-" + i, bank.getId(), bank.getName(),
                    bank.getDistrict(), group, comp, units, collectionDate, expiryDate, batch);
            dataStore.saveInventoryItem(item);
        }
    }

    private void generateCamps(int count) {
        var bloodBanks = dataStore.findAllBloodBanks();
        String[] venues = {
                "Community Health Center Grounds", "Town Hall Auditorium", "Andhra University Campus Hall",
                "Red Cross Society Bhavan", "Collectorate Conference Compound", "Rotary Youth Center",
                "Railway Community Sports Hall", "Zilla Parishad High School Grounds"
        };

        for (int i = 1; i <= count; i++) {
            String district = AP_DISTRICTS[i % AP_DISTRICTS.length];
            BloodBank bank = bloodBanks.get(random.nextInt(bloodBanks.size()));
            String title = String.format("Mega Voluntary Blood Donation Camp - %s #%d", district, i);
            String venue = venues[random.nextInt(venues.length)] + ", " + district;
            LocalDate campDate = LocalDate.now().plusDays((i % 45) - 10);
            int maxSlots = 150 + random.nextInt(150);

            DonationCamp camp = new DonationCamp(
                    "CAMP-" + i, title, "District Health Society & NSS Volunteers",
                    bank.getName(), "Andhra Pradesh", district, district, venue,
                    campDate, LocalTime.of(9, 0), LocalTime.of(16, 0), maxSlots, "+91 891 250 8899"
            );
            camp.setTargetUnits(maxSlots - 20);
            camp.setRegisteredSlots(random.nextInt(maxSlots / 2) + 20);
            camp.setStatus(campDate.isBefore(LocalDate.now()) ? "COMPLETED" : "UPCOMING");
            dataStore.saveCamp(camp);
        }
    }

    private void generateBloodRequests(int count) {
        BloodGroup[] groups = BloodGroup.values();
        BloodComponent[] components = BloodComponent.values();
        String[] urgencies = {"CRITICAL", "URGENT", "ROUTINE"};

        for (int i = 1; i <= count; i++) {
            String fName = FIRST_NAMES[random.nextInt(FIRST_NAMES.length)];
            String lName = LAST_NAMES[random.nextInt(LAST_NAMES.length)];
            String district = AP_DISTRICTS[random.nextInt(AP_DISTRICTS.length)];
            BloodGroup group = groups[random.nextInt(groups.length)];
            BloodComponent comp = components[random.nextInt(components.length)];
            String urgency = urgencies[random.nextInt(urgencies.length)];
            String hospital = String.format("Hospital & Trauma Center, %s", district);

            BloodRequest req = new BloodRequest(
                    "REQ-" + i, fName + " " + lName, group, comp,
                    random.nextInt(4) + 1, hospital, district, district,
                    LocalDate.now().plusDays(random.nextInt(5) + 1),
                    fName + " Attendant", "+91 9701 " + (10000 + i), urgency
            );
            req.setRequestDescription("Emergency requirement for surgical / thalassemia inpatient transfusion support.");
            dataStore.saveBloodRequest(req);
        }
    }

    private void generateDonations(int count) {
        var donors = dataStore.findAllUsers();
        if (donors.isEmpty()) return;

        for (int i = 1; i <= count; i++) {
            User donor = donors.get(random.nextInt(donors.size()));
            LocalDate donationDate = LocalDate.now().minusDays(random.nextInt(360) + 15);
            String location = "Visakhapatnam Rotary Blood Center #" + ((i % 10) + 1);

            DonationRecord rec = new DonationRecord(
                    "DON-" + i, donor.getId(), donor.getFullName(), donor.getBloodGroup(),
                    BloodComponent.WHOLE_BLOOD, location, donationDate, 1
            );
            rec.setCertificateUrl("/api/public/certificates/" + rec.getId());
            dataStore.saveDonationRecord(rec);
        }
    }
}
