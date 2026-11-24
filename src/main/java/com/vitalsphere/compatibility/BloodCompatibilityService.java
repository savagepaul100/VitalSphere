package com.vitalsphere.compatibility;

import com.vitalsphere.models.BloodGroup;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * Red-cell compatibility engine based on standard ABO/RhD immunohematology rules.
 * Implements compatibility matrix, compatible donor lookup, and recipient transfusion safety checks.
 */
@Service
public class BloodCompatibilityService {

    /**
     * Map of recipient blood group to list of compatible red cell donor blood groups.
     */
    private static final Map<BloodGroup, List<BloodGroup>> RECIPIENT_TO_DONORS = new EnumMap<>(BloodGroup.class);

    static {
        // O- can only receive O-
        RECIPIENT_TO_DONORS.put(BloodGroup.O_NEGATIVE, List.of(BloodGroup.O_NEGATIVE));
        // O+ can receive O-, O+
        RECIPIENT_TO_DONORS.put(BloodGroup.O_POSITIVE, List.of(BloodGroup.O_NEGATIVE, BloodGroup.O_POSITIVE));
        // A- can receive O-, A-
        RECIPIENT_TO_DONORS.put(BloodGroup.A_NEGATIVE, List.of(BloodGroup.O_NEGATIVE, BloodGroup.A_NEGATIVE));
        // A+ can receive O-, O+, A-, A+
        RECIPIENT_TO_DONORS.put(BloodGroup.A_POSITIVE, List.of(BloodGroup.O_NEGATIVE, BloodGroup.O_POSITIVE, BloodGroup.A_NEGATIVE, BloodGroup.A_POSITIVE));
        // B- can receive O-, B-
        RECIPIENT_TO_DONORS.put(BloodGroup.B_NEGATIVE, List.of(BloodGroup.O_NEGATIVE, BloodGroup.B_NEGATIVE));
        // B+ can receive O-, O+, B-, B+
        RECIPIENT_TO_DONORS.put(BloodGroup.B_POSITIVE, List.of(BloodGroup.O_NEGATIVE, BloodGroup.O_POSITIVE, BloodGroup.B_NEGATIVE, BloodGroup.B_POSITIVE));
        // AB- can receive O-, A-, B-, AB-
        RECIPIENT_TO_DONORS.put(BloodGroup.AB_NEGATIVE, List.of(BloodGroup.O_NEGATIVE, BloodGroup.A_NEGATIVE, BloodGroup.B_NEGATIVE, BloodGroup.AB_NEGATIVE));
        // AB+ Universal Recipient: can receive all 8
        RECIPIENT_TO_DONORS.put(BloodGroup.AB_POSITIVE, Arrays.asList(BloodGroup.values()));
    }

    public List<BloodGroup> getCompatibleDonorsForRecipient(BloodGroup recipientGroup) {
        if (recipientGroup == null) return Collections.emptyList();
        return RECIPIENT_TO_DONORS.getOrDefault(recipientGroup, Collections.emptyList());
    }

    public List<BloodGroup> getCompatibleRecipientsForDonor(BloodGroup donorGroup) {
        if (donorGroup == null) return Collections.emptyList();
        List<BloodGroup> compatibleRecipients = new ArrayList<>();
        for (Map.Entry<BloodGroup, List<BloodGroup>> entry : RECIPIENT_TO_DONORS.entrySet()) {
            if (entry.getValue().contains(donorGroup)) {
                compatibleRecipients.add(entry.getKey());
            }
        }
        return compatibleRecipients;
    }

    public boolean isCompatible(BloodGroup donorGroup, BloodGroup recipientGroup) {
        if (donorGroup == null || recipientGroup == null) return false;
        List<BloodGroup> compatibleDonors = getCompatibleDonorsForRecipient(recipientGroup);
        return compatibleDonors.contains(donorGroup);
    }
}
