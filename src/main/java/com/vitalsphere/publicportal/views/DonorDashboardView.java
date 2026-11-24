package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.models.DonationRecord;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;
import com.vitalsphere.repositories.VitalSphereDataStore;

import java.util.List;

/**
 * Section 6, Module 3: Donor Dashboard with cooldown indicator, certificates, and donation history.
 */
@Route(value = "dashboard", layout = PublicLayout.class)
@PageTitle("Donor Dashboard — VitalSphere")
@AnonymousAllowed
public class DonorDashboardView extends VerticalLayout {

    public DonorDashboardView(VitalSphereDataStore dataStore) {
        setWidthFull();
        setPadding(false);

        VerticalLayout content = new VerticalLayout();
        content.setWidthFull();
        content.getStyle().set("padding", "32px");

        H2 title = new H2("Voluntary Donor Portal");
        title.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Welcome back, Rajesh Kumar. Review your donation history, cooldown rest status, and simulated digital certificates.");
        sub.getStyle().set("color", "#64748B");

        HorizontalLayout cardsRow = new HorizontalLayout();
        cardsRow.setWidthFull();
        cardsRow.getStyle().set("gap", "20px");

        cardsRow.add(
                createCard("Blood Group", "O- (Universal RBC)", "🩸"),
                createCard("Screening Status", "CLEARED FOR ASSESSMENT", "✅"),
                createCard("Cooldown Status", "Eligible to Donate (110d elapsed)", "⏳"),
                createCard("Completed Donations", "4 Units Donated", "🏆")
        );

        H3 histTitle = new H3("Previous Donation History & Certificates");
        histTitle.getStyle().set("color", "#142B4A").set("margin-top", "32px");

        Grid<DonationRecord> grid = new Grid<>(DonationRecord.class, false);
        grid.setWidthFull();
        grid.getStyle().set("min-height", "300px");

        grid.addColumn(DonationRecord::getId).setHeader("Donation Ref").setWidth("120px");
        grid.addColumn(DonationRecord::getDonationDate).setHeader("Date").setWidth("140px");
        grid.addColumn(DonationRecord::getBloodBankOrCamp).setHeader("Center / Camp").setFlexGrow(1);
        grid.addColumn(d -> d.getUnitsDonated() + " Unit").setHeader("Units").setWidth("100px");
        grid.addColumn(DonationRecord::getStatus).setHeader("Status").setWidth("140px");

        List<DonationRecord> sampleList = dataStore.findAllDonations().stream().limit(5).toList();
        grid.setItems(sampleList);

        content.add(title, sub, cardsRow, histTitle, grid);
        add(content, new PublicFooterComponent());
    }

    private VerticalLayout createCard(String title, String val, String icon) {
        VerticalLayout card = new VerticalLayout();
        card.addClassName("stat-card");
        card.setWidth("25%");

        Span i = new Span(icon);
        i.getStyle().set("font-size", "1.6rem");

        Span t = new Span(title);
        t.getStyle().set("font-size", "0.8rem").set("color", "#64748B").set("font-weight", "600");

        Span v = new Span(val);
        v.getStyle().set("font-size", "1.1rem").set("color", "#142B4A").set("font-weight", "800");

        card.add(i, t, v);
        return card;
    }
}
