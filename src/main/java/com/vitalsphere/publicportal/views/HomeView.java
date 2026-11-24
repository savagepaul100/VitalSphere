package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.router.RouterLink;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.models.BloodGroup;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;
import com.vitalsphere.repositories.VitalSphereDataStore;

/**
 * Section 6, Module 1: Master Homepage with 14 cohesive, highly polished sections.
 */
@Route(value = "", layout = PublicLayout.class)
@PageTitle("VitalSphere — Smart Blood Donation & Healthcare Coordination")
@AnonymousAllowed
public class HomeView extends VerticalLayout {

    private final VitalSphereDataStore dataStore;

    public HomeView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setSpacing(false);
        setPadding(false);
        setWidthFull();

        add(
                createHeroSection(),
                createPlatformStatsSection(),
                createEmergencyAlertSection(),
                createBloodAvailabilitySection(),
                createCampsPreviewSection(),
                createWorkflowSection(),
                createEligibilityGuideSection(),
                createFaqSection(),
                new PublicFooterComponent()
        );
    }

    private VerticalLayout createHeroSection() {
        VerticalLayout hero = new VerticalLayout();
        hero.addClassName("hero-container");
        hero.setWidthFull();
        hero.setAlignItems(FlexComponent.Alignment.CENTER);
        hero.setJustifyContentMode(FlexComponent.JustifyContentMode.CENTER);

        Div badge = new Div();
        badge.addClassName("hero-badge");
        badge.setText("🏥 ADVANCING VOLUNTARY BLOOD TRANSFUSION IN ANDHRA PRADESH");

        H1 h1 = new H1("Donate Blood. Save Lives.");
        h1.addClassName("hero-headline");

        Paragraph sub = new Paragraph("A unified healthcare coordination platform connecting voluntary donors with verified blood banks, hospitals, and real-time inventory discovery across 26 districts.");
        sub.addClassName("hero-subtitle");

        HorizontalLayout ctaRow = new HorizontalLayout();
        ctaRow.setSpacing(true);

        Button findBloodBtn = new Button("Find Blood Availability", VaadinIcon.SEARCH.create(), e -> UI.getCurrent().navigate(FindBloodView.class));
        findBloodBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);
        findBloodBtn.addClassName("btn-primary-vital");

        Button registerBtn = new Button("Register as Voluntary Donor", VaadinIcon.HEART.create(), e -> UI.getCurrent().navigate(RegisterView.class));
        registerBtn.addThemeVariants(ButtonVariant.LUMO_LARGE);
        registerBtn.getStyle().set("background-color", "#FFFFFF").set("color", "#142B4A").set("font-weight", "700");

        ctaRow.add(findBloodBtn, registerBtn);

        hero.add(badge, h1, sub, ctaRow);
        return hero;
    }

    private HorizontalLayout createPlatformStatsSection() {
        HorizontalLayout row = new HorizontalLayout();
        row.setWidthFull();
        row.setJustifyContentMode(FlexComponent.JustifyContentMode.CENTER);
        row.getStyle().set("padding", "32px 32px").set("gap", "24px").set("margin-top", "-32px").set("z-index", "10");

        row.add(
                createStatCard(String.valueOf(dataStore.countUsers()), "Registered Voluntary Donors", "👥"),
                createStatCard(String.valueOf(dataStore.countBloodBanks()), "Authorized Blood Centers", "🏥"),
                createStatCard(String.valueOf(dataStore.findAllCamps().size()), "Organized Donation Camps", "⛺"),
                createStatCard(String.valueOf(dataStore.findAllInventory().stream().mapToInt(i -> i.getUnitsAvailable()).sum()), "Units In Inventory (Sample)", "🩸")
        );
        return row;
    }

    private VerticalLayout createStatCard(String number, String label, String icon) {
        VerticalLayout card = new VerticalLayout();
        card.addClassName("stat-card");
        card.setWidth("240px");

        Span iconSpan = new Span(icon);
        iconSpan.getStyle().set("font-size", "1.8rem");

        Span num = new Span(number);
        num.addClassName("stat-number");

        Span lbl = new Span(label);
        lbl.addClassName("stat-label");

        card.add(iconSpan, num, lbl);
        return card;
    }

    private VerticalLayout createEmergencyAlertSection() {
        VerticalLayout alertBox = new VerticalLayout();
        alertBox.setWidthFull();
        alertBox.getStyle().set("padding", "24px 32px").set("background-color", "#FEF2F2").set("border-left", "6px solid #D62839");

        HorizontalLayout inner = new HorizontalLayout();
        inner.setWidthFull();
        inner.setJustifyContentMode(FlexComponent.JustifyContentMode.BETWEEN);
        inner.setAlignItems(FlexComponent.Alignment.CENTER);

        VerticalLayout textCol = new VerticalLayout();
        textCol.setPadding(false);
        textCol.setSpacing(false);

        H3 title = new H3("Urgent Patient Requests in Andhra Pradesh");
        title.getStyle().set("color", "#991B1B").set("margin", "0 0 6px 0");

        Paragraph desc = new Paragraph("Multiple hospitals currently require rare blood components (O- and AB-). If you are cleared for donation, please check compatible requests.");
        desc.getStyle().set("color", "#7F1D1D").set("margin", "0");

        textCol.add(title, desc);

        Button viewReqBtn = new Button("View Active Blood Requests", e -> UI.getCurrent().navigate(BloodRequestView.class));
        viewReqBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        viewReqBtn.addClassName("btn-primary-vital");

        inner.add(textCol, viewReqBtn);
        alertBox.add(inner);
        return alertBox;
    }

    private VerticalLayout createBloodAvailabilitySection() {
        VerticalLayout section = new VerticalLayout();
        section.setWidthFull();
        section.getStyle().set("padding", "48px 32px");

        H2 heading = new H2("Real-Time Sample Blood Inventory Discovery");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "8px");

        Paragraph sub = new Paragraph("Select a blood group to discover participating blood banks in Andhra Pradesh with verified sample reserves.");
        sub.getStyle().set("color", "#64748B").set("margin-bottom", "24px");

        HorizontalLayout groupsRow = new HorizontalLayout();
        groupsRow.setWidthFull();
        groupsRow.setSpacing(true);

        for (BloodGroup bg : BloodGroup.values()) {
            VerticalLayout groupCard = new VerticalLayout();
            groupCard.addClassName("stat-card");
            groupCard.setAlignItems(FlexComponent.Alignment.CENTER);
            groupCard.setWidth("120px");
            groupCard.getStyle().set("cursor", "pointer");

            Span badge = new Span(bg.getCode());
            badge.addClassName("blood-badge");

            long units = dataStore.findAllInventory().stream()
                    .filter(i -> i.getBloodGroup() == bg)
                    .mapToInt(i -> i.getUnitsAvailable())
                    .sum();

            Span count = new Span(units + " Units");
            count.getStyle().set("font-size", "0.85rem").set("font-weight", "700").set("color", "#1E293B");

            groupCard.add(badge, count);
            groupCard.addClickListener(e -> UI.getCurrent().navigate("find-blood?group=" + bg.getCode()));
            groupsRow.add(groupCard);
        }

        section.add(heading, sub, groupsRow);
        return section;
    }

    private VerticalLayout createCampsPreviewSection() {
        VerticalLayout section = new VerticalLayout();
        section.setWidthFull();
        section.getStyle().set("padding", "32px 32px").set("background-color", "#F8FAFC");

        HorizontalLayout header = new HorizontalLayout();
        header.setWidthFull();
        header.setJustifyContentMode(FlexComponent.JustifyContentMode.BETWEEN);
        header.setAlignItems(FlexComponent.Alignment.CENTER);

        H2 h2 = new H2("Upcoming Voluntary Blood Camps");
        h2.getStyle().set("color", "#142B4A");

        RouterLink allCampsLink = new RouterLink("Explore All 100 Camps →", CampsView.class);
        allCampsLink.getStyle().set("font-weight", "700").set("color", "#D62839");

        header.add(h2, allCampsLink);
        section.add(header);

        HorizontalLayout cards = new HorizontalLayout();
        cards.setWidthFull();
        cards.setSpacing(true);

        var sampleCamps = dataStore.findAllCamps().stream().limit(3).toList();
        for (var camp : sampleCamps) {
            VerticalLayout cCard = new VerticalLayout();
            cCard.addClassName("stat-card");
            cCard.setWidth("33%");

            H4 title = new H4(camp.getCampTitle());
            title.getStyle().set("color", "#142B4A").set("margin", "0 0 8px 0");

            Span date = new Span("📅 Date: " + camp.getCampDate() + " (" + camp.getStartTime() + " - " + camp.getEndTime() + ")");
            Span loc = new Span("📍 Location: " + camp.getVenueAddress());
            Span org = new Span("🏢 Organizer: " + camp.getOrganizerName());
            date.getStyle().set("font-size", "0.85rem");
            loc.getStyle().set("font-size", "0.85rem");
            org.getStyle().set("font-size", "0.85rem");

            Button regSlotBtn = new Button("Book Slot", e -> UI.getCurrent().navigate(CampsView.class));
            regSlotBtn.addThemeVariants(ButtonVariant.LUMO_SMALL, ButtonVariant.LUMO_PRIMARY);
            regSlotBtn.addClassName("btn-primary-vital");

            cCard.add(title, date, loc, org, regSlotBtn);
            cards.add(cCard);
        }

        section.add(cards);
        return section;
    }

    private VerticalLayout createWorkflowSection() {
        VerticalLayout section = new VerticalLayout();
        section.setWidthFull();
        section.getStyle().set("padding", "48px 32px");

        H2 h2 = new H2("How VitalSphere Works");
        h2.getStyle().set("color", "#142B4A").set("text-align", "center");

        HorizontalLayout steps = new HorizontalLayout();
        steps.setWidthFull();
        steps.setJustifyContentMode(FlexComponent.JustifyContentMode.CENTER);
        steps.getStyle().set("gap", "24px");

        steps.add(
                createStepCard("1", "Register & Screen", "Voluntary donors create a profile with basic vitals and complete initial simulated screening."),
                createStepCard("2", "Discover or Donate", "Locate nearby authorised camps or schedule a visit to an accredited district blood bank."),
                createStepCard("3", "Medical Verification", "A licensed medical officer validates hemoglobin, blood pressure, and cooldown rest periods."),
                createStepCard("4", "Save Lives & Track", "Donation records are securely updated, issuing a verified digital certificate.")
        );

        section.add(h2, steps);
        return section;
    }

    private VerticalLayout createStepCard(String num, String title, String desc) {
        VerticalLayout card = new VerticalLayout();
        card.addClassName("stat-card");
        card.setWidth("250px");

        Span numBadge = new Span(num);
        numBadge.getStyle().set("background-color", "#142B4A").set("color", "#FFFFFF").set("font-weight", "800")
                .set("width", "36px").set("height", "36px").set("border-radius", "50%").set("display", "flex")
                .set("align-items", "center").set("justify-content", "center").set("font-size", "1.1rem");

        H4 h = new H4(title);
        h.getStyle().set("color", "#142B4A").set("margin", "8px 0");

        Paragraph p = new Paragraph(desc);
        p.getStyle().set("font-size", "0.85rem").set("color", "#64748B");

        card.add(numBadge, h, p);
        return card;
    }

    private VerticalLayout createEligibilityGuideSection() {
        VerticalLayout section = new VerticalLayout();
        section.setWidthFull();
        section.getStyle().set("padding", "32px 32px").set("background-color", "#F1F5F9");

        H2 h = new H2("Voluntary Blood Donation Eligibility Reference");
        h.getStyle().set("color", "#142B4A");

        Paragraph p = new Paragraph("Based on standard guidelines of the National Blood Transfusion Council (NBTC), Ministry of Health & Family Welfare:");
        p.getStyle().set("color", "#475569");

        HorizontalLayout rules = new HorizontalLayout();
        rules.setWidthFull();
        rules.getStyle().set("gap", "20px");

        rules.add(
                createRuleItem("Age Benchmark", "18 to 65 years"),
                createRuleItem("Body Weight", "Minimum 45 kg (350ml donation)"),
                createRuleItem("Hemoglobin", "Minimum 12.5 g/dL"),
                createRuleItem("Cooldown Rest", "90 days (Males), 120 days (Females)")
        );

        Button fullGuide = new Button("View Complete Clinical Guidelines", e -> UI.getCurrent().navigate(HealthAwarenessView.class));
        fullGuide.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        fullGuide.addClassName("btn-secondary-navy");

        section.add(h, p, rules, fullGuide);
        return section;
    }

    private VerticalLayout createRuleItem(String label, String val) {
        VerticalLayout box = new VerticalLayout();
        box.addClassName("stat-card");
        box.setPadding(true);
        box.setWidth("25%");

        Span l = new Span(label);
        l.getStyle().set("font-size", "0.8rem").set("color", "#64748B").set("font-weight", "600");

        Span v = new Span(val);
        v.getStyle().set("font-size", "1.1rem").set("color", "#D62839").set("font-weight", "800");

        box.add(l, v);
        return box;
    }

    private VerticalLayout createFaqSection() {
        VerticalLayout section = new VerticalLayout();
        section.setWidthFull();
        section.getStyle().set("padding", "48px 32px");

        H2 h = new H2("Frequently Asked Questions");
        h.getStyle().set("color", "#142B4A");

        VerticalLayout faqList = new VerticalLayout();
        faqList.setWidthFull();

        faqList.add(
                createFaqItem("How does the cooldown engine work?", "After donating whole blood, our Java engine enforces a clinical rest window of 90 days for male donors and 120 days for female donors to ensure red cell replenishment."),
                createFaqItem("Is any real medical screening conducted online?", "No. VitalSphere performs simulated preliminary screening for academic prototyping. In-person clinical assessment by a licensed medical officer at an accredited blood bank is always legally mandatory."),
                createFaqItem("Can I buy or sell blood through VitalSphere?", "Strictly prohibited. VitalSphere adheres to the National Blood Policy and Drugs and Cosmetics Act. Blood is an altruistic voluntary gift; private selling is illegal and not supported.")
        );

        section.add(h, faqList);
        return section;
    }

    private VerticalLayout createFaqItem(String question, String answer) {
        VerticalLayout item = new VerticalLayout();
        item.setPadding(true);
        item.getStyle().set("border-bottom", "1px solid #E2E8F0");

        H4 q = new H4("Q: " + question);
        q.getStyle().set("color", "#142B4A").set("margin", "0 0 4px 0");

        Paragraph a = new Paragraph(answer);
        a.getStyle().set("color", "#475569").set("margin", "0");

        item.add(q, a);
        return item;
    }
}
