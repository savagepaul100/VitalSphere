package com.vitalsphere.security;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.server.VaadinServletRequest;
import com.vaadin.flow.server.VaadinSession;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.logout.SecurityContextLogoutHandler;

/**
 * Helper utility for authenticated session verification, user identity, and RBAC authority checks.
 */
public class SecurityUtils {

    public static final String SESSION_USER_KEY = "CURRENT_AUTHENTICATED_USER";

    public static boolean isUserLoggedIn() {
        SecurityContext context = SecurityContextHolder.getContext();
        Authentication auth = context.getAuthentication();
        return auth != null
                && !(auth instanceof AnonymousAuthenticationToken)
                && auth.isAuthenticated();
    }

    public static String getCurrentUsername() {
        SecurityContext context = SecurityContextHolder.getContext();
        Authentication auth = context.getAuthentication();
        if (auth != null && auth.isAuthenticated()) {
            return auth.getName();
        }
        return null;
    }

    public static boolean hasRole(UserRole role) {
        SecurityContext context = SecurityContextHolder.getContext();
        Authentication auth = context.getAuthentication();
        if (auth == null || !auth.isAuthenticated()) {
            return false;
        }
        return auth.getAuthorities().stream()
                .anyMatch(a -> a.getAuthority().equals(role.getAuthority()));
    }

    public static boolean isStaffOrAdmin() {
        return hasRole(UserRole.SUPER_ADMIN)
                || hasRole(UserRole.NATIONAL_AUTHORITY)
                || hasRole(UserRole.STATE_AUTHORITY)
                || hasRole(UserRole.DISTRICT_AUTHORITY)
                || hasRole(UserRole.BLOOD_BANK_ADMIN)
                || hasRole(UserRole.MEDICAL_OFFICER)
                || hasRole(UserRole.CAMP_ORGANIZER)
                || hasRole(UserRole.SUPPORT_STAFF);
    }

    public static void logout() {
        SecurityContextLogoutHandler logoutHandler = new SecurityContextLogoutHandler();
        logoutHandler.logout(VaadinServletRequest.getCurrent().getHttpServletRequest(), null, null);
        if (VaadinSession.getCurrent() != null) {
            VaadinSession.getCurrent().getSession().invalidate();
        }
        UI.getCurrent().getPage().setLocation("/login");
    }
}
