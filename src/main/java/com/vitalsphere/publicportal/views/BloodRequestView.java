package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.datepicker.DatePicker;
import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.IntegerField;
import com.vaadin.flow.component.textfield.TextArea;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.models.BloodComponent;
import com.vitalsphere.models.BloodGroup;
import com.vitalsphere.models.BloodRequest;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.services.SampleDataGeneratorService;

import java.time.LocalDate;
import java.util.UUID;

/**
 * Section 6, Module 6: Blood Request submission for patients and attendants.
 */
@Route(value = "request-blood", layout = PublicLayout.class)
@PageTitle("Submit Blood Requirement — VitalSphere")
@AnonymousAllowed
public class BloodRequestView extends VerticalLayout {

    private final VitalSphereDataStore dataStore;

    public BloodRequestView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setWidthFull();
        setPadding(false);

        VerticalLayout content = new VerticalLayout();
        content.setWidthFull();
        content.getStyle().set("padding", "32px");

        H2 title = new H2("Submit Patient Blood Requirement");
        title.getStyle().set("color", "#142B4A").set("margin-bottom", "6px");

        Paragraph sub = new Paragraph("Authorized medical centers and registered voluntary donors are alerted upon administrative approval of this emergency requirement.");
        sub.getStyle().set("color", "#64748B");

        FormLayout form = new FormLayout();
        form.setWidth("800px");
        form.getStyle().set("background", "#FFFFFF").set("padding", "24px").set("border-radius", "8px").set("border", "1px solid #E2E8F0");

        TextField patientName = new TextField("Patient Full Name");
        ComboBox<BloodGroup> bloodGroup = new ComboBox<>("Required Blood Group", BloodGroup.values());
        bloodGroup.setItemLabelGenerator(BloodGroup::getLabel);

        ComboBox<BloodComponent> component = new ComboBox<>("Blood Component", BloodComponent.values());
        component.setItemLabelGenerator(BloodComponent::getDisplayName);
        component.setValue(BloodComponent.PACKED_RED_CELLS);

        IntegerField unitsRequired = new IntegerField("Units Required");
        unitsRequired.setMin(1);
        unitsRequired.setMax(10);
        unitsRequired.setValue(2);

        TextField hospitalName = new TextField("Hospital / Trauma Center Name");
        ComboBox<String> district = new ComboBox<>("District (Andhra Pradesh)", SampleDataGeneratorService.AP_DISTRICTS);

        DatePicker requiredDate = new DatePicker("Date Required By");
        requiredDate.setValue(LocalDate.now().plusDays(1));

        ComboBox<String> urgency = new ComboBox<>("Clinical Urgency", "CRITICAL", "URGENT", "ROUTINE");
        urgency.setValue("URGENT");

        TextField contactPerson = new TextField("Attendant / Contact Person");
        TextField contactNumber = new TextField("Emergency Contact Mobile Number");
        TextArea notes = new TextArea("Clinical Diagnosis / Case Notes");

        form.add(patientName, bloodGroup, component, unitsRequired, hospitalName, district, requiredDate, urgency, contactPerson, contactNumber, notes);
        form.setColspan(notes, 2);

        Button submitBtn = new Button("Submit Blood Request", e -> {
            if (patientName.isEmpty() || bloodGroup.isEmpty() || hospitalName.isEmpty() || district.isEmpty() || contactNumber.isEmpty()) {
                Notification.show("Please fill all mandatory fields marked.", 3000, Notification.Position.MIDDLE)
                        .addThemeVariants(NotificationVariant.LUMO_ERROR);
                return;
            }

            BloodRequest req = new BloodRequest(
                    "REQ-" + UUID.randomUUID().toString().substring(0, 8),
                    patientName.getValue(), bloodGroup.getValue(), component.getValue(),
                    unitsRequired.getValue(), hospitalName.getValue(), district.getValue(),
                    district.getValue(), requiredDate.getValue(), contactPerson.getValue(),
                    contactNumber.getValue(), urgency.getValue()
            );
            req.setRequestDescription(notes.getValue());
            dataStore.saveBloodRequest(req);

            Notification.show("Blood requirement submitted successfully! Tracking ID: " + req.getId(), 5000, Notification.Position.MIDDLE)
                    .addThemeVariants(NotificationVariant.LUMO_SUCCESS);

            patientName.clear();
            hospitalName.clear();
            contactPerson.clear();
            contactNumber.clear();
            notes.clear();
        });
        submitBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);
        submitBtn.addClassName("btn-primary-vital");

        content.add(title, sub, form, submitBtn);
        add(content, new PublicFooterComponent());
    }
}
