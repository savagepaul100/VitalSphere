package com.vitalsphere;

import com.vitalsphere.compatibility.BloodCompatibilityService;
import com.vitalsphere.eligibility.ClinicalEligibilityEngine;
import com.vitalsphere.eligibility.EligibilityStatus;
import com.vitalsphere.models.BloodGroup;
import com.vitalsphere.repositories.VitalSphereDataStore;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class VitalSphereClinicalEngineTests {

    @Autowired
    private BloodCompatibilityService compatibilityService;

    @Autowired
    private ClinicalEligibilityEngine eligibilityEngine;

    @Autowired
    private VitalSphereDataStore dataStore;

    @Test
    void testOnegativeIsUniversalDonor() {
        for (BloodGroup recipient : BloodGroup.values()) {
            assertTrue(compatibilityService.isCompatible(BloodGroup.O_NEGATIVE, recipient),
                    "O- should be compatible with recipient: " + recipient.getCode());
        }
    }

    @Test
    void testAbPositiveIsUniversalRecipient() {
        for (BloodGroup donor : BloodGroup.values()) {
            assertTrue(compatibilityService.isCompatible(donor, BloodGroup.AB_POSITIVE),
                    "AB+ should accept donor: " + donor.getCode());
        }
    }

    @Test
    void testIncompatibleTransfusionBlocked() {
        assertFalse(compatibilityService.isCompatible(BloodGroup.A_POSITIVE, BloodGroup.B_POSITIVE),
                "A+ must never be transfused to B+ recipient");
        assertFalse(compatibilityService.isCompatible(BloodGroup.AB_POSITIVE, BloodGroup.O_POSITIVE),
                "AB+ must never be transfused to O+ recipient");
    }

    @Test
    void testCooldownDeferralUnder90DaysForMale() {
        LocalDate recentDonation = LocalDate.now().minusDays(45);
        var result = eligibilityEngine.evaluateDonor(25, 70.0, 14.0, "MALE", recentDonation, false, false);

        assertEquals(EligibilityStatus.TEMPORARILY_DEFERRED, result.getStatus());
        assertFalse(result.isEligibleToSchedule());
        assertEquals(45, result.getDaysRemainingInCooldown());
    }

    @Test
    void testEligibilityClearedWhenMetricsValid() {
        LocalDate olderDonation = LocalDate.now().minusDays(105);
        var result = eligibilityEngine.evaluateDonor(28, 68.0, 14.5, "MALE", olderDonation, false, false);

        assertEquals(EligibilityStatus.CLEARED_FOR_ASSESSMENT, result.getStatus());
        assertTrue(result.isEligibleToSchedule());
    }

    @Test
    void testUnderagePermanentlyDeferred() {
        var result = eligibilityEngine.evaluateDonor(16, 55.0, 13.0, "MALE", null, false, false);
        assertEquals(EligibilityStatus.PERMANENTLY_DEFERRED, result.getStatus());
    }

    @Test
    void testSeedDataPopulatedSuccessfully() {
        assertTrue(dataStore.countUsers() >= 1000, "Should generate at least 1,000 donors");
        assertTrue(dataStore.countBloodBanks() >= 100, "Should generate at least 100 blood banks");
        assertTrue(dataStore.findAllCamps().size() >= 100, "Should generate at least 100 camps");
        assertTrue(dataStore.findAllInventory().size() >= 800, "Should generate at least 800 inventory items");
    }
}
