package com.vitalsphere.publicportal.layouts;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.applayout.AppLayout;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.RouterLink;
import com.vitalsphere.publicportal.views.*;
import com.vitalsphere.security.SecurityUtils;

/**
 * Public portal responsive layout with government-inspired top notice,
 * navigation bar, citizen links, login/register triggers, and full footer.
 */
public class PublicLayout extends AppLayout {

    public PublicLayout() {
        createHeader();
        createFooter();
    }

    private void createHeader() {
        // 1. Government-inspired disclaimer top bar
        Div govTopBar = new Div();
        govTopBar.addClassName("gov-top-bar");

        HorizontalLayout leftGov = new HorizontalLayout();
        leftGov.setAlignItems(FlexComponent.Alignment.CENTER);
        leftGov.setSpacing(true);

        Span flagIcon = new Span("🇮🇳");
        Span govTitle = new Span("VITALSPHERE NATIONAL DIGITAL BLOOD COORDINATION ECOSYSTEM");
        govTitle.getStyle().set("font-weight", "600");
        leftGov.add(flagIcon, govTitle);

        HorizontalLayout rightGov = new HorizontalLayout();
        rightGov.setAlignItems(FlexComponent.Alignment.CENTER);
        rightGov.setSpacing(true);

        Span demoBadge = new Span("ACADEMIC PROTOTYPE • SIMULATED MEDICAL RECORDS");
        demoBadge.addClassName("demo-badge");

        RouterLink adminLink = new RouterLink("Official Portal", AdminDashboardRedirectView.class);
        adminLink.getStyle().set("color", "#94A3B8").set("font-size", "0.75rem").set("text-decoration", "underline");

        rightGov.add(demoBadge, adminLink);
        govTopBar.add(leftGov, rightGov);

        // 2. Main Public Navbar
        HorizontalLayout mainNav = new HorizontalLayout();
        mainNav.addClassName("public-header");
        mainNav.setWidthFull();
        mainNav.setJustifyContentMode(FlexComponent.JustifyContentMode.BETWEEN);
        mainNav.setAlignItems(FlexComponent.Alignment.CENTER);

        // Brand
        VerticalLayout brandBox = new VerticalLayout();
        brandBox.setPadding(false);
        brandBox.setSpacing(false);
        brandBox.setMargin(false);

        Anchor brandLink = new Anchor("/", "");
        HorizontalLayout brandRow = new HorizontalLayout();
        brandRow.setAlignItems(FlexComponent.Alignment.CENTER);
        brandRow.setSpacing(true);

        Icon dropIcon = VaadinIcon.DROP.create();
        dropIcon.setColor("#D62839");
        dropIcon.setSize("28px");

        H2 brandText = new H2("VitalSphere");
        brandText.getStyle().set("margin", "0").set("font-size", "1.6rem").set("font-weight", "800").set("color", "#142B4A");

        brandRow.add(dropIcon, brandText);
        brandLink.add(brandRow);

        Span tagline = new Span("Connecting Lives. Empowering Hope.");
        tagline.addClassName("brand-tagline");

        brandBox.add(brandLink, tagline);

        // Nav Links
        HorizontalLayout navLinks = new HorizontalLayout();
        navLinks.setAlignItems(FlexComponent.Alignment.CENTER);
        navLinks.setSpacing(true);

        RouterLink homeLink = new RouterLink("Home", HomeView.class);
        RouterLink findBloodLink = new RouterLink("Find Blood", FindBloodView.class);
        RouterLink donateLink = new RouterLink("Donate Blood", DonateView.class);
        RouterLink campsLink = new RouterLink("Camps", CampsView.class);
        RouterLink requestLink = new RouterLink("Request Blood", BloodRequestView.class);
        RouterLink awarenessLink = new RouterLink("Health Awareness", HealthAwarenessView.class);

        navLinks.add(homeLink, findBloodLink, donateLink, campsLink, requestLink, awarenessLink);

        // Action Buttons
        HorizontalLayout authActions = new HorizontalLayout();
        authActions.setAlignItems(FlexComponent.Alignment.CENTER);

        if (SecurityUtils.isUserLoggedIn()) {
            Button dashboardBtn = new Button("My Dashboard", VaadinIcon.USER.create(), e -> UI.getCurrent().navigate(DonorDashboardView.class));
            dashboardBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
            dashboardBtn.addClassName("btn-primary-vital");

            Button logoutBtn = new Button("Logout", VaadinIcon.SIGN_OUT.create(), e -> SecurityUtils.logout());
            logoutBtn.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

            authActions.add(dashboardBtn, logoutBtn);
        } else {
            Button loginBtn = new Button("Sign In", VaadinIcon.SIGN_IN.create(), e -> UI.getCurrent().navigate(LoginView.class));
            loginBtn.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

            Button registerBtn = new Button("Register as Donor", VaadinIcon.PLUS_CIRCLE.create(), e -> UI.getCurrent().navigate(RegisterView.class));
            registerBtn.addClassName("btn-primary-vital");

            authActions.add(loginBtn, registerBtn);
        }

        mainNav.add(brandBox, navLinks, authActions);

        VerticalLayout headerWrapper = new VerticalLayout(govTopBar, mainNav);
        headerWrapper.setPadding(false);
        headerWrapper.setSpacing(false);
        headerWrapper.setWidthFull();

        addToNavbar(true, headerWrapper);
    }

    private void createFooter() {
        // AppLayout child views will render in content, footer can be attached to views or page base
    }
}
