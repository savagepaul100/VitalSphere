package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.html.H3;
import com.vaadin.flow.component.html.Paragraph;
import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.login.LoginForm;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.*;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;

/**
 * Section 6, Module 2: Citizen & Authority Authentication View.
 */
@Route(value = "login", layout = PublicLayout.class)
@PageTitle("Sign In — VitalSphere")
@AnonymousAllowed
public class LoginView extends VerticalLayout implements BeforeEnterObserver {

    private final LoginForm loginForm = new LoginForm();

    public LoginView() {
        setWidthFull();
        setPadding(false);

        VerticalLayout content = new VerticalLayout();
        content.setWidthFull();
        content.setAlignItems(FlexComponent.Alignment.CENTER);
        content.getStyle().set("padding", "48px 16px");

        H3 title = new H3("Sign In to VitalSphere");
        title.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Enter your registered credentials to access your donor dashboard or administrative command portal.");
        sub.getStyle().set("color", "#64748B").set("margin-bottom", "20px");

        loginForm.setAction("login");

        VerticalLayout demoCredentialsBox = new VerticalLayout();
        demoCredentialsBox.setWidth("380px");
        demoCredentialsBox.getStyle().set("background", "#F1F5F9").set("padding", "16px").set("border-radius", "8px").set("border", "1px solid #CBD5E1").set("margin-top", "16px");

        Span demoTitle = new Span("🔑 Prototype Demo Accounts");
        demoTitle.getStyle().set("font-weight", "700").set("color", "#142B4A").set("font-size", "0.85rem");

        Paragraph c1 = new Paragraph("• Super Admin: admin@vitalsphere.gov.in / Admin@VitalSphere2026\n" +
                "• Medical Officer: doctor.sharma@vitalsphere.gov.in / Doctor@2026\n" +
                "• Blood Bank Admin: bloodbank.vizag@vitalsphere.gov.in / Bank@2026\n" +
                "• Camp Organizer: organizer.ap@vitalsphere.gov.in / Camp@2026\n" +
                "• Voluntary Donor: donor@vitalsphere.demo / Donor@2026");
        c1.getStyle().set("font-size", "0.78rem").set("color", "#334155").set("line-height", "1.5").set("white-space", "pre-line");

        demoCredentialsBox.add(demoTitle, c1);

        content.add(title, sub, loginForm, demoCredentialsBox);
        add(content, new PublicFooterComponent());
    }

    @Override
    public void beforeEnter(BeforeEnterEvent beforeEnterEvent) {
        if (beforeEnterEvent.getLocation().getQueryParameters().getParameters().containsKey("error")) {
            loginForm.setError(true);
        }
    }
}
