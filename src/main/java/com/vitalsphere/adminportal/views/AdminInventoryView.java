package com.vitalsphere.adminportal.views;

import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.PageTitle;
import com.vaadin.flow.router.Route;
import com.vitalsphere.adminportal.layouts.AdminLayout;
import com.vitalsphere.models.BloodComponent;
import com.vitalsphere.models.BloodGroup;
import com.vitalsphere.models.InventoryItem;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.services.SampleDataGeneratorService;
import jakarta.annotation.security.PermitAll;

import java.util.List;

/**
 * Section 9 & 13: Central Blood Inventory & Expiry Monitoring.
 */
@Route(value = "admin/inventory", layout = AdminLayout.class)
@PageTitle("Inventory Control — VitalSphere Admin")
@PermitAll
public class AdminInventoryView extends VerticalLayout {

    private final VitalSphereDataStore dataStore;
    private final Grid<InventoryItem> grid = new Grid<>(InventoryItem.class, false);
    private final ComboBox<BloodGroup> groupFilter = new ComboBox<>("Blood Group", BloodGroup.values());
    private final ComboBox<String> districtFilter = new ComboBox<>("District", SampleDataGeneratorService.AP_DISTRICTS);

    public AdminInventoryView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setWidthFull();
        setPadding(true);

        H2 heading = new H2("Central Blood Stock & Expiry Control (800 Sample Units)");
        heading.getStyle().set("color", "#142B4A").set("margin-bottom", "4px");

        Paragraph sub = new Paragraph("Monitor unit levels, component batches, and expiry warnings across district blood banks.");
        sub.getStyle().set("color", "#64748B");

        HorizontalLayout filters = new HorizontalLayout();
        filters.setWidthFull();
        filters.setAlignItems(FlexComponent.Alignment.END);

        groupFilter.setItemLabelGenerator(BloodGroup::getLabel);
        groupFilter.setPlaceholder("All Groups");
        groupFilter.setClearButtonVisible(true);
        groupFilter.addValueChangeListener(e -> refreshGrid());

        districtFilter.setPlaceholder("All Districts");
        districtFilter.setClearButtonVisible(true);
        districtFilter.addValueChangeListener(e -> refreshGrid());

        filters.add(groupFilter, districtFilter);

        configureGrid();
        refreshGrid();

        add(heading, sub, filters, grid);
    }

    private void configureGrid() {
        grid.setWidthFull();
        grid.getStyle().set("min-height", "550px");

        grid.addColumn(InventoryItem::getBatchNumber).setHeader("Batch No").setWidth("140px");
        grid.addColumn(i -> i.getBloodGroup().getCode()).setHeader("Blood Group").setWidth("110px");
        grid.addColumn(i -> i.getComponent().getDisplayName()).setHeader("Component").setWidth("200px");
        grid.addColumn(InventoryItem::getBloodBankName).setHeader("Blood Bank Center").setFlexGrow(2);
        grid.addColumn(InventoryItem::getDistrict).setHeader("District").setWidth("150px");
        grid.addColumn(i -> i.getUnitsAvailable() + " Units").setHeader("Available").setWidth("110px");
        grid.addColumn(InventoryItem::getCollectionDate).setHeader("Collected").setWidth("130px");
        grid.addColumn(InventoryItem::getExpiryDate).setHeader("Expiry Date").setWidth("130px");
    }

    private void refreshGrid() {
        List<InventoryItem> list = dataStore.findInventoryByFilters(groupFilter.getValue(), districtFilter.getValue(), null);
        grid.setItems(list);
    }
}
