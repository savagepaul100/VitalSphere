package com.vitalsphere;

import com.vaadin.flow.component.page.AppShellConfigurator;
import com.vaadin.flow.component.page.Push;
import com.vaadin.flow.theme.Theme;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * VitalSphere - Smart Blood Donation & Healthcare Coordination Platform
 * Central Spring Boot entry point and Vaadin AppShell configuration.
 */
@SpringBootApplication
@EnableScheduling
@Theme(value = "vitalsphere")
@Push
public class VitalSphereApplication implements AppShellConfigurator {

    public static void main(String[] args) {
        SpringApplication.run(VitalSphereApplication.class, args);
    }
}
