package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.dialog.Dialog;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.models.DonationCamp;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.services.SampleDataGeneratorService;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Section 6, Module 5: Voluntary Blood Donation Camps listing and registration with simulated QR attendance.
 */
@Route(value = "camps", layout = PublicLayout.class)
@PageTitle("Donation Camps — VitalSphere")
@AnonymousAllowed
public class CampsView extends VerticalLayout {

    private final VitalSphereDataStore dataStore;
    private final Grid<DonationCamp> campGrid = new Grid<>(DonationCamp.class, false);
    private final ComboBox<String> districtFilter = new ComboBox<>("District");

    public CampsView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setWidthFull();
        setPadding(false);

        VerticalLayout content = new VerticalLayout();
        content.setWidthFull();
        content.getStyle().set("padding", "32px");

        H2 title = new H2("Voluntary Blood Donation Camps in Andhra Pradesh");
        title.getStyle().set("color", "#142B4A").set("margin-bottom", "6px");

        Paragraph sub = new Paragraph("Locate government and community organized donation camps, explore timing schedules, and register for an attendance slot.");
        sub.getStyle().set("color", "#64748B");

        HorizontalLayout filterRow = new HorizontalLayout();
        filterRow.setAlignItems(FlexComponent.Alignment.END);

        districtFilter.setItems(SampleDataGeneratorService.AP_DISTRICTS);
        districtFilter.setPlaceholder("All Districts");
        districtFilter.setClearButtonVisible(true);
        districtFilter.addValueChangeListener(e -> refreshCamps());

        Button resetBtn = new Button("Clear Filter", e -> {
            districtFilter.clear();
            refreshCamps();
        });

        filterRow.add(districtFilter, resetBtn);

        configureGrid();
        refreshCamps();

        content.add(title, sub, filterRow, campGrid);
        add(content, new PublicFooterComponent());
    }

    private void configureGrid() {
        campGrid.setWidthFull();
        campGrid.getStyle().set("min-height", "500px");

        campGrid.addColumn(DonationCamp::getCampTitle)
                .setHeader("Camp Title & Details")
                .setFlexGrow(2);

        campGrid.addColumn(c -> c.getCampDate() + " (" + c.getStartTime() + " - " + c.getEndTime() + ")")
                .setHeader("Date & Timings")
                .setWidth("200px");

        campGrid.addColumn(DonationCamp::getDistrict)
                .setHeader("District")
                .setWidth("150px");

        campGrid.addColumn(DonationCamp::getVenueAddress)
                .setHeader("Venue")
                .setFlexGrow(1);

        campGrid.addColumn(c -> c.getRegisteredSlots() + " / " + c.getMaxSlots())
                .setHeader("Slots Filled")
                .setWidth("130px");

        campGrid.addComponentColumn(camp -> {
            Button registerBtn = new Button("Book Slot", e -> openBookingDialog(camp));
            registerBtn.addThemeVariants(ButtonVariant.LUMO_SMALL, ButtonVariant.LUMO_PRIMARY);
            registerBtn.addClassName("btn-primary-vital");
            return registerBtn;
        }).setHeader("Registration").setWidth("140px");
    }

    private void refreshCamps() {
        String dist = districtFilter.getValue();
        List<DonationCamp> list = dataStore.findAllCamps();
        if (dist != null && !dist.isEmpty()) {
            list = list.stream().filter(c -> c.getDistrict().equalsIgnoreCase(dist)).collect(Collectors.toList());
        }
        campGrid.setItems(list);
    }

    private void openBookingDialog(DonationCamp camp) {
        Dialog dialog = new Dialog();
        dialog.setHeaderTitle("Camp Registration: " + camp.getCampTitle());

        VerticalLayout layout = new VerticalLayout();
        TextField nameField = new TextField("Donor Full Name");
        TextField mobileField = new TextField("Mobile Number");
        TextField emailField = new TextField("Email Address");

        layout.add(
                new Paragraph("Date: " + camp.getCampDate() + " | Venue: " + camp.getVenueAddress()),
                nameField, mobileField, emailField
        );

        Button confirmBtn = new Button("Confirm Registration", e -> {
            if (nameField.isEmpty() || mobileField.isEmpty()) {
                Notification.show("Please enter donor name and contact number", 3000, Notification.Position.MIDDLE)
                        .addThemeVariants(NotificationVariant.LUMO_ERROR);
                return;
            }
            camp.setRegisteredSlots(camp.getRegisteredSlots() + 1);
            dataStore.saveCamp(camp);
            refreshCamps();
            dialog.close();

            Notification notif = Notification.show("Registration Confirmed! Your simulated QR Pass is generated.", 4000, Notification.Position.MIDDLE);
            notif.addThemeVariants(NotificationVariant.LUMO_SUCCESS);
        });
        confirmBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        confirmBtn.addClassName("btn-primary-vital");

        Button cancelBtn = new Button("Cancel", e -> dialog.close());

        dialog.add(layout);
        dialog.getFooter().add(cancelBtn, confirmBtn);
        dialog.open();
    }
}
