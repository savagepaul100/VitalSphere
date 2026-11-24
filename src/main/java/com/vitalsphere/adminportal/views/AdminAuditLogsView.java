package com.vitalsphere.adminportal.views;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vitalsphere.adminportal.layouts.AdminLayout;
import com.vitalsphere.models.AuditLog;
import com.vitalsphere.repositories.VitalSphereDataStore;
import jakarta.annotation.security.PermitAll;

/**
 * Section 9 & 10: Regulatory and Clinical Audit Logs.
 */
@Route(value = "admin/audit-logs", layout = AdminLayout.class)
@PageTitle("Audit Logs — VitalSphere Admin")
@PermitAll
public class AdminAuditLogsView extends VerticalLayout {

    public AdminAuditLogsView(VitalSphereDataStore dataStore) {
        setWidthFull();
        setPadding(true);

        H2 heading = new H2("Administrative & Clinical Audit Trails");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Immutable logging of sensitive operations, medical status changes, user clearances, and blood stock approvals.");
        sub.getStyle().set("color", "#64748B");

        Grid<AuditLog> grid = new Grid<>(AuditLog.class, false);
        grid.setWidthFull();
        grid.getStyle().set("min-height", "550px");

        grid.addColumn(AuditLog::getId).setHeader("Log ID").setWidth("120px");
        grid.addColumn(AuditLog::getAction).setHeader("Operation").setWidth("220px");
        grid.addColumn(AuditLog::getPerformedBy).setHeader("Performed By").setWidth("180px");
        grid.addColumn(AuditLog::getUserRole).setHeader("Role").setWidth("160px");
        grid.addColumn(AuditLog::getTargetEntity).setHeader("Entity").setWidth("140px");
        grid.addColumn(AuditLog::getDetails).setHeader("Details").setFlexGrow(1);
        grid.addColumn(AuditLog::getTimestamp).setHeader("Timestamp").setWidth("180px");

        grid.setItems(dataStore.findAllAuditLogs());

        add(heading, sub, grid);
    }
}
