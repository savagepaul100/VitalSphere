package com.vitalsphere.publicportal.components;

import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.RouterLink;
import com.vitalsphere.publicportal.views.*;

/**
 * Clean, professional government-inspired footer for public pages.
 */
public class PublicFooterComponent extends VerticalLayout {

    public PublicFooterComponent() {
        addClassName("public-footer");
        setWidthFull();
        setPadding(true);
        setSpacing(true);

        HorizontalLayout grid = new HorizontalLayout();
        grid.setWidthFull();
        grid.setJustifyContentMode(FlexComponent.JustifyContentMode.BETWEEN);

        // Col 1: About
        VerticalLayout col1 = new VerticalLayout();
        col1.setPadding(false);
        col1.setWidth("30%");
        H4 h1 = new H4("VitalSphere Platform");
        Paragraph p1 = new Paragraph("A smart, centralized healthcare coordination prototype connecting voluntary blood donors, blood banks, hospitals, and recipients with verified clinical eligibility standards.");
        p1.getStyle().set("font-size", "0.85rem").set("line-height", "1.6");
        Span demoNotice = new Span("Notice: This is an academic demonstration system. Fictional data is utilized for simulation purposes.");
        demoNotice.getStyle().set("font-size", "0.75rem").set("color", "#EF4444").set("font-weight", "600");
        col1.add(h1, p1, demoNotice);

        // Col 2: Citizen Services
        VerticalLayout col2 = new VerticalLayout();
        col2.setPadding(false);
        col2.setWidth("20%");
        H4 h2 = new H4("Citizen Services");
        col2.add(h2,
                new RouterLink("Find Available Blood", FindBloodView.class),
                new RouterLink("Voluntary Donor Registration", RegisterView.class),
                new RouterLink("Locate Donation Camps", CampsView.class),
                new RouterLink("Submit Blood Requirement", BloodRequestView.class),
                new RouterLink("Compatibility Matrix", HealthAwarenessView.class)
        );

        // Col 3: Guidelines & Education
        VerticalLayout col3 = new VerticalLayout();
        col3.setPadding(false);
        col3.setWidth("20%");
        H4 h3 = new H4("Health & Safety");
        col3.add(h3,
                new RouterLink("Eligibility Criteria", HealthAwarenessView.class),
                new RouterLink("Donation Cooldown Standards", HealthAwarenessView.class),
                new RouterLink("Post-Donation Care", HealthAwarenessView.class),
                new RouterLink("ABO & Rh Compatibility Guide", HealthAwarenessView.class),
                new RouterLink("Frequently Asked Questions", HealthAwarenessView.class)
        );

        // Col 4: Administrative
        VerticalLayout col4 = new VerticalLayout();
        col4.setPadding(false);
        col4.setWidth("20%");
        H4 h4 = new H4("Authority Access");
        col4.add(h4,
                new RouterLink("Blood Bank Login", LoginView.class),
                new RouterLink("Medical Officer Verification", LoginView.class),
                new RouterLink("Camp Organizer Portal", LoginView.class),
                new RouterLink("Audit & Regulatory Logs", AdminDashboardRedirectView.class)
        );

        grid.add(col1, col2, col3, col4);

        Div bottomBar = new Div();
        bottomBar.setWidthFull();
        bottomBar.getStyle().set("border-top", "1px solid rgba(255,255,255,0.1)")
                .set("padding-top", "16px").set("margin-top", "24px").set("text-align", "center");
        Span copyright = new Span("© 2026 VitalSphere. Designed for Academic Healthcare Engineering. All simulated records conform to official CDSCO / DGHS reference benchmarks.");
        copyright.getStyle().set("font-size", "0.78rem").set("color", "#64748B");
        bottomBar.add(copyright);

        add(grid, bottomBar);
    }
}
