package com.vitalsphere.adminportal.views;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vitalsphere.adminportal.layouts.AdminLayout;
import com.vitalsphere.models.BloodBank;
import com.vitalsphere.repositories.VitalSphereDataStore;
import jakarta.annotation.security.PermitAll;

/**
 * Section 9: Blood Bank directory and authorized center management.
 */
@Route(value = "admin/blood-banks", layout = AdminLayout.class)
@PageTitle("Blood Banks — VitalSphere Admin")
@PermitAll
public class AdminBloodBanksView extends VerticalLayout {

    public AdminBloodBanksView(VitalSphereDataStore dataStore) {
        setWidthFull();
        setPadding(true);

        H2 heading = new H2("Authorized Blood Centers & Storage Units (100 Sample Centers)");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Accredited government hospitals, Red Cross blood societies, and charitable blood banks across 26 Andhra Pradesh districts.");
        sub.getStyle().set("color", "#64748B");

        Grid<BloodBank> grid = new Grid<>(BloodBank.class, false);
        grid.setWidthFull();
        grid.getStyle().set("min-height", "550px");

        grid.addColumn(BloodBank::getId).setHeader("Center ID").setWidth("110px");
        grid.addColumn(BloodBank::getName).setHeader("Blood Bank / Medical Center").setFlexGrow(2);
        grid.addColumn(BloodBank::getLicenseNumber).setHeader("CDSCO License").setWidth("160px");
        grid.addColumn(BloodBank::getCategory).setHeader("Category").setWidth("140px");
        grid.addColumn(BloodBank::getDistrict).setHeader("District").setWidth("160px");
        grid.addColumn(BloodBank::getContactNumber).setHeader("Contact Helpline").setWidth("160px");
        grid.addColumn(b -> b.isComponentSeparationAvailable() ? "Available" : "No").setHeader("Component Unit").setWidth("140px");

        grid.setItems(dataStore.findAllBloodBanks());

        add(heading, sub, grid);
    }
}
