package com.vitalsphere.adminportal.views;

import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.data.value.ValueChangeMode;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vitalsphere.adminportal.layouts.AdminLayout;
import com.vitalsphere.models.BloodGroup;
import com.vitalsphere.models.User;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.services.SampleDataGeneratorService;
import jakarta.annotation.security.PermitAll;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Section 9: Donor Directory & Voluntary Registry Management.
 */
@Route(value = "admin/donors", layout = AdminLayout.class)
@PageTitle("Donor Management — VitalSphere Admin")
@PermitAll
public class AdminDonorsView extends VerticalLayout {

    private final VitalSphereDataStore dataStore;
    private final Grid<User> donorGrid = new Grid<>(User.class, false);
    private final TextField searchField = new TextField("Search Donor Name or Email");
    private final ComboBox<BloodGroup> groupFilter = new ComboBox<>("Blood Group", BloodGroup.values());
    private final ComboBox<String> districtFilter = new ComboBox<>("District", SampleDataGeneratorService.AP_DISTRICTS);

    public AdminDonorsView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setWidthFull();
        setPadding(true);

        H2 heading = new H2("Voluntary Donor Directory (1,000 Sample Records)");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Review verified citizen voluntary donors, blood groups, and district registration details.");
        sub.getStyle().set("color", "#64748B");

        HorizontalLayout filterRow = new HorizontalLayout();
        filterRow.setWidthFull();
        filterRow.setAlignItems(FlexComponent.Alignment.END);

        searchField.setPlaceholder("e.g. Ramesh or kumar@...");
        searchField.setValueChangeMode(ValueChangeMode.EAGER);
        searchField.addValueChangeListener(e -> refreshDonors());

        groupFilter.setItemLabelGenerator(BloodGroup::getLabel);
        groupFilter.setPlaceholder("All Groups");
        groupFilter.setClearButtonVisible(true);
        groupFilter.addValueChangeListener(e -> refreshDonors());

        districtFilter.setPlaceholder("All Districts");
        districtFilter.setClearButtonVisible(true);
        districtFilter.addValueChangeListener(e -> refreshDonors());

        filterRow.add(searchField, groupFilter, districtFilter);

        configureGrid();
        refreshDonors();

        add(heading, sub, filterRow, donorGrid);
    }

    private void configureGrid() {
        donorGrid.setWidthFull();
        donorGrid.getStyle().set("min-height", "550px");

        donorGrid.addColumn(User::getId).setHeader("Donor ID").setWidth("120px");
        donorGrid.addColumn(User::getFullName).setHeader("Full Name").setFlexGrow(1);
        donorGrid.addColumn(u -> u.getBloodGroup() != null ? u.getBloodGroup().getCode() : "N/A").setHeader("Blood Group").setWidth("120px");
        donorGrid.addColumn(User::getGender).setHeader("Gender").setWidth("100px");
        donorGrid.addColumn(User::getDistrict).setHeader("District").setWidth("160px");
        donorGrid.addColumn(User::getMobileNumber).setHeader("Contact").setWidth("160px");
        donorGrid.addColumn(User::getVerificationStatus).setHeader("Status").setWidth("130px");
    }

    private void refreshDonors() {
        String query = searchField.getValue() != null ? searchField.getValue().toLowerCase().trim() : "";
        BloodGroup group = groupFilter.getValue();
        String district = districtFilter.getValue();

        List<User> filtered = dataStore.findAllUsers().stream()
                .filter(u -> query.isEmpty() || u.getFullName().toLowerCase().contains(query) || u.getEmail().toLowerCase().contains(query))
                .filter(u -> group == null || u.getBloodGroup() == group)
                .filter(u -> district == null || u.getDistrict().equalsIgnoreCase(district))
                .collect(Collectors.toList());

        donorGrid.setItems(filtered);
    }
}
