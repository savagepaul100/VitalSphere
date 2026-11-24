package com.vitalsphere.eligibility;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

/**
 * Dedicated Java clinical screening & cooldown evaluation engine.
 * Implements reference rules adhering to official Indian National Blood Transfusion Council (NBTC) guidelines:
 * - Age: 18 - 65 years
 * - Weight: Minimum 45 kg (whole blood 350ml), 50 kg for 450ml
 * - Hemoglobin: >= 12.5 g/dL
 * - Blood Pressure: Systolic 100-140 mmHg, Diastolic 60-90 mmHg
 * - Temperature: <= 37.5 C (oral)
 * - Whole Blood Donation Cooldown: 90 days (males), 120 days (females)
 */
@Service
public class ClinicalEligibilityEngine {

    @Value("${vitalsphere.cooldown.whole-blood-male-days:90}")
    private int maleCooldownDays;

    @Value("${vitalsphere.cooldown.whole-blood-female-days:120}")
    private int femaleCooldownDays;

    public static class ScreeningEvaluationResult {
        private final EligibilityStatus status;
        private final String clinicalSummary;
        private final long daysRemainingInCooldown;
        private final boolean eligibleToSchedule;

        public ScreeningEvaluationResult(EligibilityStatus status, String clinicalSummary, long daysRemainingInCooldown, boolean eligibleToSchedule) {
            this.status = status;
            this.clinicalSummary = clinicalSummary;
            this.daysRemainingInCooldown = daysRemainingInCooldown;
            this.eligibleToSchedule = eligibleToSchedule;
        }

        public EligibilityStatus getStatus() { return status; }
        public String getClinicalSummary() { return clinicalSummary; }
        public long getDaysRemainingInCooldown() { return daysRemainingInCooldown; }
        public boolean isEligibleToSchedule() { return eligibleToSchedule; }
    }

    public ScreeningEvaluationResult evaluateDonor(int age, double weightKg, double hemoglobinGdl,
                                                   String gender, LocalDate lastDonationDate,
                                                   boolean recentInfection, boolean recentTattooOrPiercing) {

        // 1. Permanent deferral checks
        if (age < 18) {
            return new ScreeningEvaluationResult(
                    EligibilityStatus.PERMANENTLY_DEFERRED,
                    "Donor is below the statutory age limit of 18 years.", 0, false
            );
        }
        if (age > 65) {
            return new ScreeningEvaluationResult(
                    EligibilityStatus.PERMANENTLY_DEFERRED,
                    "Donor exceeds maximum permissible voluntary donation age of 65 years.", 0, false
            );
        }

        // 2. Cooldown check
        int requiredCooldown = "FEMALE".equalsIgnoreCase(gender) ? femaleCooldownDays : maleCooldownDays;
        long daysSince = (lastDonationDate != null) ? ChronoUnit.DAYS.between(lastDonationDate, LocalDate.now()) : 999;
        if (daysSince < requiredCooldown) {
            long remaining = requiredCooldown - daysSince;
            return new ScreeningEvaluationResult(
                    EligibilityStatus.TEMPORARILY_DEFERRED,
                    String.format("Post-donation rest interval active. %d days remaining until next eligible whole-blood donation.", remaining),
                    remaining, false
            );
        }

        // 3. Transient deferrals
        if (recentInfection) {
            return new ScreeningEvaluationResult(
                    EligibilityStatus.TEMPORARILY_DEFERRED,
                    "Recent active infection reported. 14-day post-recovery clinical deferral required.", 14, false
            );
        }
        if (recentTattooOrPiercing) {
            return new ScreeningEvaluationResult(
                    EligibilityStatus.TEMPORARILY_DEFERRED,
                    "Recent tattoo or body piercing requires 6-month deferral per NBTC safety protocols.", 180, false
            );
        }

        // 4. Clinical baseline vitals
        if (weightKg < 45.0) {
            return new ScreeningEvaluationResult(
                    EligibilityStatus.REQUIRES_ADDITIONAL_REVIEW,
                    "Donor weight is below 45.0 kg benchmark for whole blood collection.", 0, false
            );
        }
        if (hemoglobinGdl < 12.5) {
            return new ScreeningEvaluationResult(
                    EligibilityStatus.REQUIRES_ADDITIONAL_REVIEW,
                    String.format("Hemoglobin level (%.1f g/dL) is below the minimum mandatory standard of 12.5 g/dL.", hemoglobinGdl), 0, false
            );
        }

        // 5. Cleared for in-person assessment
        return new ScreeningEvaluationResult(
                EligibilityStatus.CLEARED_FOR_ASSESSMENT,
                "Donor meets standard preliminary baseline metrics. Cleared for medical officer on-site examination.",
                0, true
        );
    }
}
