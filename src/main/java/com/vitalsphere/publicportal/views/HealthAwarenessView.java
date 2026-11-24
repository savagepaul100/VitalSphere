package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.models.BloodGroup;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;

/**
 * Section 6, Module 7 & Section 8: Health Awareness & ABO/Rh Compatibility Matrix.
 */
@Route(value = "awareness", layout = PublicLayout.class)
@PageTitle("Health Awareness & Compatibility — VitalSphere")
@AnonymousAllowed
public class HealthAwarenessView extends VerticalLayout {

    public HealthAwarenessView() {
        setWidthFull();
        setPadding(false);

        VerticalLayout content = new VerticalLayout();
        content.setWidthFull();
        content.getStyle().set("padding", "32px");

        H2 title = new H2("Blood Group Compatibility & Clinical Health Guidance");
        title.getStyle().set("color", "#142B4A").set("margin-bottom", "6px");

        Paragraph sub = new Paragraph("Evidence-based voluntary transfusion guidance conforming to National Blood Transfusion Council (NBTC) clinical reference standards.");
        sub.getStyle().set("color", "#64748B");

        // Compatibility Table
        H3 matrixHeading = new H3("Red Blood Cell (RBC) Transfusion Compatibility Matrix");
        matrixHeading.getStyle().set("color", "#142B4A").set("margin-top", "24px");

        Div tableContainer = createCompatibilityTable();

        // Clinical Preparation & Post-care
        HorizontalLayout infoGrid = new HorizontalLayout();
        infoGrid.setWidthFull();
        infoGrid.getStyle().set("margin-top", "32px").set("gap", "24px");

        VerticalLayout prepCard = createInfoCard("Preparation Before Donation",
                "• Drink an extra 500ml of water or fluids before arrival.\n" +
                "• Consume a healthy, iron-rich meal; avoid fatty snacks prior to donation.\n" +
                "• Get at least 7 hours of adequate sleep the previous night.\n" +
                "• Carry a government photo identity card for voluntary registration.");

        VerticalLayout postCard = createInfoCard("Post-Donation Recovery Care",
                "• Rest in the observation lounge for 15 minutes and enjoy light refreshments.\n" +
                "• Keep the bandage clean and dry on your venipuncture site for at least 4 hours.\n" +
                "• Avoid strenuous physical workouts or heavy lifting for the rest of the day.\n" +
                "• Maintain high fluid hydration throughout the next 48 hours.");

        infoGrid.add(prepCard, postCard);

        content.add(title, sub, matrixHeading, tableContainer, infoGrid);
        add(content, new PublicFooterComponent());
    }

    private Div createCompatibilityTable() {
        Div container = new Div();
        container.getStyle().set("overflow-x", "auto").set("background", "#FFFFFF").set("padding", "20px").set("border-radius", "8px").set("border", "1px solid #E2E8F0");

        String html = "<table style='width:100%; border-collapse:collapse; text-align:left; font-size:0.9rem;'>" +
                "<tr style='background-color:#142B4A; color:#FFFFFF;'>" +
                "<th style='padding:12px;'>Recipient Blood Group</th>" +
                "<th style='padding:12px;'>Compatible Red Cell Donors</th>" +
                "<th style='padding:12px;'>Universal Clinical Notes</th>" +
                "</tr>" +
                "<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:10px; font-weight:700; color:#D62839;'>O-</td><td>O-</td><td>Universal Red Cell Donor (can donate to all). Can only receive O-.</td></tr>" +
                "<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:10px; font-weight:700;'>O+</td><td>O-, O+</td><td>Most common blood group in India.</td></tr>" +
                "<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:10px; font-weight:700;'>A-</td><td>O-, A-</td><td>Can receive from Rh-negative O and A donors.</td></tr>" +
                "<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:10px; font-weight:700;'>A+</td><td>O-, O+, A-, A+</td><td>Can receive from A and O types.</td></tr>" +
                "<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:10px; font-weight:700;'>B-</td><td>O-, B-</td><td>Can receive from Rh-negative O and B donors.</td></tr>" +
                "<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:10px; font-weight:700;'>B+</td><td>O-, O+, B-, B+</td><td>High prevalence in Indian population.</td></tr>" +
                "<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:10px; font-weight:700;'>AB-</td><td>O-, A-, B-, AB-</td><td>Can receive all Rh-negative red cells.</td></tr>" +
                "<tr><td style='padding:10px; font-weight:700; color:#10B981;'>AB+</td><td>All 8 Groups (O-, O+, A-, A+, B-, B+, AB-, AB+)</td><td>Universal Red Cell Recipient.</td></tr>" +
                "</table>";

        container.getElement().setProperty("innerHTML", html);
        return container;
    }

    private VerticalLayout createInfoCard(String heading, String points) {
        VerticalLayout card = new VerticalLayout();
        card.addClassName("stat-card");
        card.setWidth("50%");

        H4 h = new H4(heading);
        h.getStyle().set("color", "#142B4A").set("margin", "0 0 12px 0");

        String formatted = points.replace("\n", "<br/><br/>");
        Paragraph p = new Paragraph();
        p.getElement().setProperty("innerHTML", formatted);
        p.getStyle().set("font-size", "0.88rem").set("color", "#334155").set("line-height", "1.6");

        card.add(h, p);
        return card;
    }
}
