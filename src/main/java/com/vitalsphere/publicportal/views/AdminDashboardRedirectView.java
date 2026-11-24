package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.html.Div;
import com.vaadin.flow.router.BeforeEnterEvent;
import com.vaadin.flow.router.BeforeEnterObserver;
import com.vaadin.flow.router.Route;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.adminportal.views.AdminDashboardView;

/**
 * Convenient redirect to Administration command dashboard.
 */
@Route("admin")
@AnonymousAllowed
public class AdminDashboardRedirectView extends Div implements BeforeEnterObserver {

    @Override
    public void beforeEnter(BeforeEnterEvent event) {
        event.forwardTo(AdminDashboardView.class);
    }
}
