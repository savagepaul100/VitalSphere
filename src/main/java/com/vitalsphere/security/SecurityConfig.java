package com.vitalsphere.security;

import com.vaadin.flow.spring.security.VaadinWebSecurity;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;

import java.util.ArrayList;
import java.util.List;

/**
 * Spring Security configuration seamlessly integrated with Vaadin Flow.
 * Guarantees public access to citizen modules while protecting administration routes.
 */
@EnableWebSecurity
@Configuration
public class SecurityConfig extends VaadinWebSecurity {

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        // Public endpoints allowed without authentication
        http.authorizeHttpRequests(auth -> auth
                .requestMatchers(
                        new AntPathRequestMatcher("/"),
                        new AntPathRequestMatcher("/find-blood/**"),
                        new AntPathRequestMatcher("/donate/**"),
                        new AntPathRequestMatcher("/camps/**"),
                        new AntPathRequestMatcher("/awareness/**"),
                        new AntPathRequestMatcher("/request-blood/**"),
                        new AntPathRequestMatcher("/register/**"),
                        new AntPathRequestMatcher("/login/**"),
                        new AntPathRequestMatcher("/api/public/**"),
                        new AntPathRequestMatcher("/images/**"),
                        new AntPathRequestMatcher("/icons/**"),
                        new AntPathRequestMatcher("/themes/**")
                ).permitAll()
                .requestMatchers(new AntPathRequestMatcher("/admin/**")).authenticated()
        );

        super.configure(http);
        setLoginView(http, "/login");
    }

    @Bean
    public UserDetailsService userDetailsService(PasswordEncoder passwordEncoder) {
        List<UserDetails> users = new ArrayList<>();

        // 1. Super Admin
        users.add(User.withUsername("admin@vitalsphere.gov.in")
                .password(passwordEncoder.encode("Admin@VitalSphere2026"))
                .roles("SUPER_ADMIN", "NATIONAL_AUTHORITY")
                .build());

        // 2. Medical Officer
        users.add(User.withUsername("doctor.sharma@vitalsphere.gov.in")
                .password(passwordEncoder.encode("Doctor@2026"))
                .roles("MEDICAL_OFFICER")
                .build());

        // 3. Blood Bank Admin (Visakhapatnam District Hospital)
        users.add(User.withUsername("bloodbank.vizag@vitalsphere.gov.in")
                .password(passwordEncoder.encode("Bank@2026"))
                .roles("BLOOD_BANK_ADMIN")
                .build());

        // 4. Camp Organizer
        users.add(User.withUsername("organizer.ap@vitalsphere.gov.in")
                .password(passwordEncoder.encode("Camp@2026"))
                .roles("CAMP_ORGANIZER")
                .build());

        // 5. Test Voluntary Donor
        users.add(User.withUsername("donor@vitalsphere.demo")
                .password(passwordEncoder.encode("Donor@2026"))
                .roles("DONOR")
                .build());

        return new InMemoryUserDetailsManager(users);
    }
}
