package com.vitalsphere.adminportal.layouts;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.applayout.AppLayout;
import com.vaadin.flow.component.applayout.DrawerToggle;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.RouterLink;
import com.vitalsphere.adminportal.views.*;
import com.vitalsphere.publicportal.views.HomeView;
import com.vitalsphere.security.SecurityUtils;

/**
 * Section 9 & 10: Administration Portal Layout with high-density sidebar,
 * RBAC authorization badges, and audit command bar.
 */
public class AdminLayout extends AppLayout {

    public AdminLayout() {
        createHeader();
        createSidebar();
    }

    private void createHeader() {
        DrawerToggle toggle = new DrawerToggle();
        toggle.getStyle().set("color", "#142B4A");

        H3 portalTitle = new H3("VitalSphere National Healthcare Administration");
        portalTitle.getStyle().set("margin", "0").set("font-size", "1.1rem").set("font-weight", "700").set("color", "#142B4A");

        Span roleBadge = new Span("SUPER_ADMIN / STATE_AUTHORITY");
        roleBadge.getStyle().set("background", "#FEF3C7").set("color", "#92400E").set("padding", "3px 8px")
                .set("border-radius", "4px").set("font-size", "0.72rem").set("font-weight", "700");

        HorizontalLayout left = new HorizontalLayout(toggle, portalTitle, roleBadge);
        left.setAlignItems(FlexComponent.Alignment.CENTER);
        left.setSpacing(true);

        HorizontalLayout right = new HorizontalLayout();
        right.setAlignItems(FlexComponent.Alignment.CENTER);

        Button publicSiteBtn = new Button("Public Portal", VaadinIcon.EXTERNAL_LINK.create(), e -> UI.getCurrent().navigate(HomeView.class));
        publicSiteBtn.addThemeVariants(ButtonVariant.LUMO_TERTIARY);

        Button logoutBtn = new Button("Sign Out", VaadinIcon.SIGN_OUT.create(), e -> SecurityUtils.logout());
        logoutBtn.addThemeVariants(ButtonVariant.LUMO_ERROR, ButtonVariant.LUMO_TERTIARY);

        right.add(publicSiteBtn, logoutBtn);

        HorizontalLayout headerBar = new HorizontalLayout(left, right);
        headerBar.setWidthFull();
        headerBar.setJustifyContentMode(FlexComponent.JustifyContentMode.BETWEEN);
        headerBar.addClassName("admin-header");

        addToNavbar(headerBar);
    }

    private void createSidebar() {
        VerticalLayout navList = new VerticalLayout();
        navList.setPadding(true);
        navList.setSpacing(true);
        navList.addClassName("admin-sidebar");
        navList.setWidth("270px");

        Div brandDiv = new Div();
        brandDiv.getStyle().set("padding-bottom", "16px").set("border-bottom", "1px solid rgba(255,255,255,0.1)");
        H4 h = new H4("COMMAND CENTER");
        h.getStyle().set("color", "#FFFFFF").set("margin", "0 0 4px 0").set("letter-spacing", "1px");
        Span sub = new Span("Health & Blood Logistics Node");
        sub.getStyle().set("color", "#94A3B8").set("font-size", "0.75rem");
        brandDiv.add(h, sub);
        navList.add(brandDiv);

        navList.add(
                createNavItem("Dashboard", AdminDashboardView.class, VaadinIcon.DASHBOARD),
                createNavItem("Donor Directory", AdminDonorsView.class, VaadinIcon.USERS),
                createNavItem("Medical Screening", AdminMedicalVerificationView.class, VaadinIcon.DOCTOR),
                createNavItem("Blood Banks", AdminBloodBanksView.class, VaadinIcon.HOSPITAL),
                createNavItem("Inventory Control", AdminInventoryView.class, VaadinIcon.DATABASE),
                createNavItem("Blood Requests", AdminRequestsView.class, VaadinIcon.EXCLAMATION_CIRCLE_O),
                createNavItem("Donation Camps", AdminCampsView.class, VaadinIcon.CALENDAR),
                createNavItem("Audit Logs", AdminAuditLogsView.class, VaadinIcon.FILE_TEXT_O)
        );

        addToDrawer(navList);
    }

    private RouterLink createNavItem(String text, Class<? extends com.vaadin.flow.component.Component> target, VaadinIcon icon) {
        RouterLink link = new RouterLink();
        link.setRoute(target);

        Icon vaadinIcon = icon.create();
        vaadinIcon.setSize("18px");
        vaadinIcon.getStyle().set("color", "#94A3B8");

        Span label = new Span(text);
        label.getStyle().set("color", "#F8FAFC").set("font-size", "0.9rem").set("font-weight", "500");

        HorizontalLayout row = new HorizontalLayout(vaadinIcon, label);
        row.setAlignItems(FlexComponent.Alignment.CENTER);
        row.setSpacing(true);
        row.getStyle().set("padding", "8px 12px").set("border-radius", "6px").set("transition", "background 0.2s");

        link.add(row);
        return link;
    }
}
