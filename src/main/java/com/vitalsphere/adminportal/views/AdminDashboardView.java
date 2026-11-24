package com.vitalsphere.adminportal.views;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vitalsphere.adminportal.layouts.AdminLayout;
import com.vitalsphere.models.BloodRequest;
import com.vitalsphere.repositories.VitalSphereDataStore;
import jakarta.annotation.security.PermitAll;

import java.util.List;

/**
 * Section 9: Executive Command Dashboard.
 */
@Route(value = "admin/dashboard", layout = AdminLayout.class)
@PageTitle("Executive Dashboard — VitalSphere Admin")
@PermitAll
public class AdminDashboardView extends VerticalLayout {

    public AdminDashboardView(VitalSphereDataStore dataStore) {
        setWidthFull();
        setPadding(true);

        H2 heading = new H2("National Healthcare Command Dashboard");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Central operational overview of voluntary blood donors, accredited blood banks, inventory reserves, and emergency requests across Andhra Pradesh.");
        sub.getStyle().set("color", "#64748B");

        HorizontalLayout statCards = new HorizontalLayout();
        statCards.setWidthFull();
        statCards.getStyle().set("gap", "16px").set("margin-top", "16px");

        statCards.add(
                createMetric("1,000", "Simulated Donors", "👥", "#0284C7"),
                createMetric("100", "Authorized Blood Centers", "🏥", "#10B981"),
                createMetric("100", "Scheduled Camps", "⛺", "#8B5CF6"),
                createMetric(String.valueOf(dataStore.findAllInventory().stream().mapToInt(i -> i.getUnitsAvailable()).sum()), "Units In Reserve", "🩸", "#D62839"),
                createMetric(String.valueOf(dataStore.findAllBloodRequests().size()), "Emergency Requests", "🚨", "#F59E0B")
        );

        H3 alertHeading = new H3("High Priority Urgent Transfusion Requests");
        alertHeading.getStyle().set("color", "#142B4A").set("margin-top", "32px");

        Grid<BloodRequest> reqGrid = new Grid<>(BloodRequest.class, false);
        reqGrid.setWidthFull();
        reqGrid.getStyle().set("min-height", "350px");

        reqGrid.addColumn(BloodRequest::getId).setHeader("Req ID").setWidth("120px");
        reqGrid.addColumn(BloodRequest::getPatientName).setHeader("Patient").setWidth("160px");
        reqGrid.addColumn(r -> r.getBloodGroup().getCode()).setHeader("Blood Group").setWidth("120px");
        reqGrid.addColumn(BloodRequest::getHospitalName).setHeader("Hospital").setFlexGrow(1);
        reqGrid.addColumn(BloodRequest::getDistrict).setHeader("District").setWidth("140px");
        reqGrid.addColumn(BloodRequest::getUrgency).setHeader("Urgency").setWidth("120px");
        reqGrid.addColumn(BloodRequest::getStatus).setHeader("Status").setWidth("130px");

        List<BloodRequest> list = dataStore.findAllBloodRequests().stream().limit(10).toList();
        reqGrid.setItems(list);

        add(heading, sub, statCards, alertHeading, reqGrid);
    }

    private VerticalLayout createMetric(String val, String lbl, String icon, String color) {
        VerticalLayout box = new VerticalLayout();
        box.addClassName("stat-card");
        box.setWidth("20%");
        box.getStyle().set("border-top", "4px solid " + color);

        HorizontalLayout row = new HorizontalLayout();
        row.setWidthFull();
        row.setJustifyContentMode(FlexComponent.JustifyContentMode.BETWEEN);

        Span l = new Span(lbl);
        l.getStyle().set("font-size", "0.78rem").set("color", "#64748B").set("font-weight", "600");

        Span ic = new Span(icon);
        row.add(l, ic);

        Span v = new Span(val);
        v.getStyle().set("font-size", "1.8rem").set("color", "#142B4A").set("font-weight", "800");

        box.add(row, v);
        return box;
    }
}
