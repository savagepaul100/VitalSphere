package com.vitalsphere.adminportal.views;

import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.TextArea;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vitalsphere.adminportal.layouts.AdminLayout;
import com.vitalsphere.eligibility.EligibilityStatus;
import com.vitalsphere.eligibility.MedicalScreeningRecord;
import com.vitalsphere.models.AuditLog;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.security.SecurityUtils;
import jakarta.annotation.security.PermitAll;

import java.util.UUID;

/**
 * Section 7 & 9: Medical Officer Clinical Verification & Screening Review.
 */
@Route(value = "admin/medical-verification", layout = AdminLayout.class)
@PageTitle("Medical Verification — VitalSphere Admin")
@PermitAll
public class AdminMedicalVerificationView extends VerticalLayout {

    private final VitalSphereDataStore dataStore;
    private final Grid<MedicalScreeningRecord> medGrid = new Grid<>(MedicalScreeningRecord.class, false);

    public AdminMedicalVerificationView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setWidthFull();
        setPadding(true);

        H2 heading = new H2("Clinical Medical Screening & Donor Deferral Verification");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Medical Officer console for reviewing physical vitals, hemoglobin thresholds, and cooldown deferrals. Sensitive clinical records are strictly masked.");
        sub.getStyle().set("color", "#64748B");

        configureGrid();
        refreshGrid();

        add(heading, sub, medGrid);
    }

    private void configureGrid() {
        medGrid.setWidthFull();
        medGrid.getStyle().set("min-height", "550px");

        medGrid.addColumn(MedicalScreeningRecord::getId).setHeader("Screening ID").setWidth("120px");
        medGrid.addColumn(MedicalScreeningRecord::getDonorName).setHeader("Donor Name").setFlexGrow(1);
        medGrid.addColumn(m -> m.getWeightKg() + " kg").setHeader("Weight").setWidth("100px");
        medGrid.addColumn(m -> m.getHemoglobinGdl() + " g/dL").setHeader("Hemoglobin").setWidth("120px");
        medGrid.addColumn(MedicalScreeningRecord::getBloodPressure).setHeader("BP").setWidth("120px");
        medGrid.addColumn(m -> m.getStatus().getLabel()).setHeader("Clinical Status").setWidth("200px");

        medGrid.addComponentColumn(rec -> {
            Button reviewBtn = new Button("Review", e -> openReviewDialog(rec));
            reviewBtn.addThemeVariants(ButtonVariant.LUMO_SMALL, ButtonVariant.LUMO_PRIMARY);
            reviewBtn.addClassName("btn-primary-vital");
            return reviewBtn;
        }).setHeader("Action").setWidth("120px");
    }

    private void refreshGrid() {
        medGrid.setItems(dataStore.findAllMedicalRecords());
    }

    private void openReviewDialog(MedicalScreeningRecord rec) {
        Dialog dialog = new Dialog();
        dialog.setHeaderTitle("Clinical Decision: " + rec.getDonorName());

        VerticalLayout layout = new VerticalLayout();
        layout.add(
                new Paragraph("Hemoglobin: " + rec.getHemoglobinGdl() + " g/dL | Weight: " + rec.getWeightKg() + " kg | BP: " + rec.getBloodPressure()),
                new Paragraph("Current Status: " + rec.getStatus().getLabel())
        );

        TextArea officerNotes = new TextArea("Medical Officer Assessment Notes");
        officerNotes.setValue(rec.getMedicalOfficerNotes() != null ? rec.getMedicalOfficerNotes() : "");
        officerNotes.setWidthFull();

        layout.add(officerNotes);

        Button clearBtn = new Button("Clear for Assessment", e -> {
            rec.setStatus(EligibilityStatus.CLEARED_FOR_ASSESSMENT);
            rec.setMedicalOfficerNotes(officerNotes.getValue());
            dataStore.saveMedicalRecord(rec);

            dataStore.logAudit(new AuditLog(
                    "AUDIT-" + UUID.randomUUID().toString().substring(0, 8),
                    "MEDICAL_CLEARANCE_UPDATED",
                    SecurityUtils.getCurrentUsername() != null ? SecurityUtils.getCurrentUsername() : "doctor.sharma",
                    "MEDICAL_OFFICER", "MedicalRecord", rec.getId(), "Cleared donor for assessment"
            ));

            dialog.close();
            refreshGrid();
            Notification.show("Screening status updated to CLEARED FOR ASSESSMENT.", 3000, Notification.Position.MIDDLE)
                    .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
        });
        clearBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        clearBtn.addClassName("btn-primary-vital");

        Button deferBtn = new Button("Temporarily Defer", e -> {
            rec.setStatus(EligibilityStatus.TEMPORARILY_DEFERRED);
            rec.setMedicalOfficerNotes(officerNotes.getValue());
            dataStore.saveMedicalRecord(rec);

            dataStore.logAudit(new AuditLog(
                    "AUDIT-" + UUID.randomUUID().toString().substring(0, 8),
                    "DONOR_TEMPORARILY_DEFERRED",
                    SecurityUtils.getCurrentUsername() != null ? SecurityUtils.getCurrentUsername() : "doctor.sharma",
                    "MEDICAL_OFFICER", "MedicalRecord", rec.getId(), "Donor deferred"
            ));

            dialog.close();
            refreshGrid();
            Notification.show("Donor temporarily deferred.", 3000, Notification.Position.MIDDLE)
                    .addThemeVariants(NotificationVariant.LUMO_WARNING);
        });
        deferBtn.addThemeVariants(ButtonVariant.LUMO_ERROR);

        dialog.add(layout);
        dialog.getFooter().add(new Button("Cancel", e -> dialog.close()), deferBtn, clearBtn);
        dialog.open();
    }
}
