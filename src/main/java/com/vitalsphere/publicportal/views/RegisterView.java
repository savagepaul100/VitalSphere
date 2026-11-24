package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.datepicker.DatePicker;
import com.vaadin.flow.component.formlayout.FormLayout;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.component.textfield.TextField;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.models.BloodGroup;
import com.vitalsphere.models.User;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.security.UserRole;
import com.vitalsphere.services.SampleDataGeneratorService;

import java.time.LocalDate;
import java.util.UUID;

/**
 * Section 6, Module 2: Voluntary Donor Registration.
 * Does NOT collect Aadhaar number or biometric data (strictly adhering to Section 2 & 14 guidelines).
 */
@Route(value = "register", layout = PublicLayout.class)
@PageTitle("Register as Voluntary Donor — VitalSphere")
@AnonymousAllowed
public class RegisterView extends VerticalLayout {

    private final VitalSphereDataStore dataStore;

    public RegisterView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setWidthFull();
        setPadding(false);

        VerticalLayout content = new VerticalLayout();
        content.setWidthFull();
        content.setAlignItems(FlexComponent.Alignment.CENTER);
        content.getStyle().set("padding", "32px");

        H2 title = new H2("Voluntary Blood Donor Registration");
        title.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Join the Andhra Pradesh voluntary donation network. Identity verification is simulated for academic demonstration.");
        sub.getStyle().set("color", "#64748B");

        FormLayout form = new FormLayout();
        form.setWidth("750px");
        form.getStyle().set("background", "#FFFFFF").set("padding", "28px").set("border-radius", "8px").set("border", "1px solid #E2E8F0");

        TextField fullName = new TextField("Full Name");
        TextField email = new TextField("Email Address");
        TextField mobile = new TextField("Mobile Number");
        DatePicker dob = new DatePicker("Date of Birth");
        dob.setMax(LocalDate.now().minusYears(18));
        dob.setValue(LocalDate.now().minusYears(22));

        ComboBox<String> gender = new ComboBox<>("Gender", "MALE", "FEMALE", "OTHER");
        gender.setValue("MALE");

        ComboBox<BloodGroup> bloodGroup = new ComboBox<>("Blood Group (If Known)", BloodGroup.values());
        bloodGroup.setItemLabelGenerator(BloodGroup::getLabel);

        ComboBox<String> district = new ComboBox<>("District (Andhra Pradesh)", SampleDataGeneratorService.AP_DISTRICTS);
        district.setValue("Visakhapatnam");

        TextField city = new TextField("City / Town");
        TextField address = new TextField("Residential Address");
        TextField pincode = new TextField("Pincode");

        form.add(fullName, email, mobile, dob, gender, bloodGroup, district, city, address, pincode);

        Button registerBtn = new Button("Submit Registration", e -> {
            if (fullName.isEmpty() || email.isEmpty() || mobile.isEmpty() || bloodGroup.isEmpty() || district.isEmpty()) {
                Notification.show("Please complete required profile fields.", 3000, Notification.Position.MIDDLE)
                        .addThemeVariants(NotificationVariant.LUMO_ERROR);
                return;
            }

            User user = new User(
                    "DONOR-" + UUID.randomUUID().toString().substring(0, 8),
                    fullName.getValue(), email.getValue(), mobile.getValue(),
                    dob.getValue(), gender.getValue(), "Andhra Pradesh",
                    district.getValue(), city.getValue(), bloodGroup.getValue(), UserRole.DONOR
            );
            user.setAddress(address.getValue());
            user.setPincode(pincode.getValue());

            dataStore.saveUser(user);

            Notification.show("Registration Successful! Please proceed to login.", 4000, Notification.Position.MIDDLE)
                    .addThemeVariants(NotificationVariant.LUMO_SUCCESS);

            UI.getCurrent().navigate(LoginView.class);
        });
        registerBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY, ButtonVariant.LUMO_LARGE);
        registerBtn.addClassName("btn-primary-vital");

        content.add(title, sub, form, registerBtn);
        add(content, new PublicFooterComponent());
    }
}
