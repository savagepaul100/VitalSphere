package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.datepicker.DatePicker;
import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.NumberField;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.eligibility.ClinicalEligibilityEngine;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;

import java.time.LocalDate;

/**
 * Section 6, Module 1: Donate Blood & Preliminary Clinical Self-Screening.
 */
@Route(value = "donate", layout = PublicLayout.class)
@PageTitle("Donate Blood & Self-Screening — VitalSphere")
@AnonymousAllowed
public class DonateView extends VerticalLayout {

    private final ClinicalEligibilityEngine eligibilityEngine;

    public DonateView(ClinicalEligibilityEngine eligibilityEngine) {
        this.eligibilityEngine = eligibilityEngine;
        setWidthFull();
        setPadding(false);

        VerticalLayout content = new VerticalLayout();
        content.setWidthFull();
        content.setAlignItems(FlexComponent.Alignment.CENTER);
        content.getStyle().set("padding", "32px");

        H2 title = new H2("Voluntary Donation & Eligibility Check");
        title.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Evaluate your current clinical fitness and post-donation rest cooldown before heading to a donation camp.");
        sub.getStyle().set("color", "#64748B");

        FormLayout form = new FormLayout();
        form.setWidth("750px");
        form.getStyle().set("background", "#FFFFFF").set("padding", "28px").set("border-radius", "8px").set("border", "1px solid #E2E8F0");

        NumberField age = new NumberField("Age (Years)");
        age.setValue(24.0);

        NumberField weight = new NumberField("Weight (Kg)");
        weight.setValue(65.0);

        NumberField hemoglobin = new NumberField("Estimated Hemoglobin (g/dL)");
        hemoglobin.setValue(13.5);

        ComboBox<String> gender = new ComboBox<>("Gender", "MALE", "FEMALE");
        gender.setValue("MALE");

        DatePicker lastDonationDate = new DatePicker("Date of Previous Donation (If any)");
        lastDonationDate.setValue(LocalDate.now().minusDays(110));

        ComboBox<String> recentInfection = new ComboBox<>("Active Infection in Past 14 Days?", "NO", "YES");
        recentInfection.setValue("NO");

        ComboBox<String> tattoo = new ComboBox<>("Tattoo / Body Piercing in Past 6 Months?", "NO", "YES");
        tattoo.setValue("NO");

        form.add(age, weight, hemoglobin, gender, lastDonationDate, recentInfection, tattoo);

        Div resultContainer = new Div();
        resultContainer.setWidth("750px");
        resultContainer.getStyle().set("margin-top", "16px").set("display", "none");

        Button checkBtn = new Button("Run Simulated Screening", e -> {
            var result = eligibilityEngine.evaluateDonor(
                    age.getValue().intValue(),
                    weight.getValue(),
                    hemoglobin.getValue(),
                    gender.getValue(),
                    lastDonationDate.getValue(),
                    "YES".equals(recentInfection.getValue()),
                    "YES".equals(tattoo.getValue())
            );

            resultContainer.removeAll();
            resultContainer.getStyle().set("display", "block").set("padding", "20px").set("border-radius", "8px");

            H4 resTitle = new H4("Screening Status: " + result.getStatus().getLabel());
            Paragraph resSummary = new Paragraph(result.getClinicalSummary());

            if (result.isEligibleToSchedule()) {
                resultContainer.getStyle().set("background", "#ECFDF5").set("border", "1px solid #10B981");
                resTitle.getStyle().set("color", "#065F46");
                Button findCampBtn = new Button("Proceed to Locate Camps", ev -> UI.getCurrent().navigate(CampsView.class));
                findCampBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
                findCampBtn.addClassName("btn-primary-vital");
                resultContainer.add(resTitle, resSummary, findCampBtn);
            } else {
                resultContainer.getStyle().set("background", "#FFFBEB").set("border", "1px solid #F59E0B");
                resTitle.getStyle().set("color", "#92400E");
                resultContainer.add(resTitle, resSummary);
            }
        });
        checkBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);
        checkBtn.addClassName("btn-primary-vital");

        content.add(title, sub, form, checkBtn, resultContainer);
        add(content, new PublicFooterComponent());
    }
}
