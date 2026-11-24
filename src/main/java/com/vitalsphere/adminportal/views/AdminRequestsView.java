package com.vitalsphere.adminportal.views;

import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vitalsphere.adminportal.layouts.AdminLayout;
import com.vitalsphere.models.AuditLog;
import com.vitalsphere.models.BloodRequest;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.security.SecurityUtils;
import jakarta.annotation.security.PermitAll;

import java.util.UUID;

/**
 * Section 9: Blood Request Management and Transfusion Allocation.
 */
@Route(value = "admin/requests", layout = AdminLayout.class)
@PageTitle("Blood Requests — VitalSphere Admin")
@PermitAll
public class AdminRequestsView extends VerticalLayout {

    private final VitalSphereDataStore dataStore;
    private final Grid<BloodRequest> grid = new Grid<>(BloodRequest.class, false);

    public AdminRequestsView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setWidthFull();
        setPadding(true);

        H2 heading = new H2("Emergency & Clinical Blood Requirement Allocations");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Review inbound patient emergency requests, match with compatible blood banks, and authorize allocation.");
        sub.getStyle().set("color", "#64748B");

        configureGrid();
        refreshGrid();

        add(heading, sub, grid);
    }

    private void configureGrid() {
        grid.setWidthFull();
        grid.getStyle().set("min-height", "550px");

        grid.addColumn(BloodRequest::getId).setHeader("Req ID").setWidth("110px");
        grid.addColumn(BloodRequest::getPatientName).setHeader("Patient").setWidth("160px");
        grid.addColumn(r -> r.getBloodGroup().getCode()).setHeader("Blood Group").setWidth("110px");
        grid.addColumn(r -> r.getUnitsRequired() + " Units").setHeader("Required").setWidth("110px");
        grid.addColumn(BloodRequest::getHospitalName).setHeader("Hospital").setFlexGrow(1);
        grid.addColumn(BloodRequest::getDistrict).setHeader("District").setWidth("140px");
        grid.addColumn(BloodRequest::getUrgency).setHeader("Urgency").setWidth("110px");
        grid.addColumn(BloodRequest::getStatus).setHeader("Status").setWidth("130px");

        grid.addComponentColumn(req -> {
            Button fulfillBtn = new Button("Mark Fulfilled", e -> {
                req.setStatus("FULFILLED");
                dataStore.saveBloodRequest(req);

                dataStore.logAudit(new AuditLog(
                        "AUDIT-" + UUID.randomUUID().toString().substring(0, 8),
                        "REQUEST_FULFILLED",
                        SecurityUtils.getCurrentUsername() != null ? SecurityUtils.getCurrentUsername() : "admin",
                        "SUPER_ADMIN", "BloodRequest", req.getId(), "Allocated units and fulfilled"
                ));

                refreshGrid();
                Notification.show("Blood requirement " + req.getId() + " marked as FULFILLED.", 3000, Notification.Position.MIDDLE)
                        .addThemeVariants(NotificationVariant.LUMO_SUCCESS);
            });
            fulfillBtn.addThemeVariants(ButtonVariant.LUMO_SMALL, ButtonVariant.LUMO_PRIMARY);
            fulfillBtn.addClassName("btn-primary-vital");
            return fulfillBtn;
        }).setHeader("Action").setWidth("140px");
    }

    private void refreshGrid() {
        grid.setItems(dataStore.findAllBloodRequests());
    }
}
