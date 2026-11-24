package com.vitalsphere.adminportal.views;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vitalsphere.adminportal.layouts.AdminLayout;
import com.vitalsphere.models.DonationCamp;
import com.vitalsphere.repositories.VitalSphereDataStore;
import jakarta.annotation.security.PermitAll;

/**
 * Section 9: Camp Management and Scheduling.
 */
@Route(value = "admin/camps", layout = AdminLayout.class)
@PageTitle("Camp Management — VitalSphere Admin")
@PermitAll
public class AdminCampsView extends VerticalLayout {

    public AdminCampsView(VitalSphereDataStore dataStore) {
        setWidthFull();
        setPadding(true);

        H2 heading = new H2("Voluntary Blood Camp Management (100 Sample Camps)");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Schedule, track attendance, and monitor collection targets for community donation drives.");
        sub.getStyle().set("color", "#64748B");

        Grid<DonationCamp> grid = new Grid<>(DonationCamp.class, false);
        grid.setWidthFull();
        grid.getStyle().set("min-height", "550px");

        grid.addColumn(DonationCamp::getId).setHeader("Camp ID").setWidth("110px");
        grid.addColumn(DonationCamp::getCampTitle).setHeader("Camp Title").setFlexGrow(2);
        grid.addColumn(DonationCamp::getDistrict).setHeader("District").setWidth("140px");
        grid.addColumn(DonationCamp::getCampDate).setHeader("Date").setWidth("130px");
        grid.addColumn(DonationCamp::getOrganizerName).setHeader("Organizer").setWidth("180px");
        grid.addColumn(DonationCamp::getParticipatingBloodBank).setHeader("Assigned Center").setFlexGrow(1);
        grid.addColumn(c -> c.getRegisteredSlots() + " / " + c.getMaxSlots()).setHeader("Registered").setWidth("120px");
        grid.addColumn(DonationCamp::getStatus).setHeader("Status").setWidth("120px");

        grid.setItems(dataStore.findAllCamps());

        add(heading, sub, grid);
    }
}
