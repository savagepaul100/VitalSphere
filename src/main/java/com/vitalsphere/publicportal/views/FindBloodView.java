package com.vitalsphere.publicportal.views;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.button.Button;
import com.vaadin.flow.component.button.ButtonVariant;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.html.*;
import com.vaadin.flow.component.orderedlayout.FlexComponent;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import com.vaadin.flow.router.*;
import com.vaadin.flow.server.auth.AnonymousAllowed;
import com.vitalsphere.models.BloodComponent;
import com.vitalsphere.models.BloodGroup;
import com.vitalsphere.models.InventoryItem;
import com.vitalsphere.publicportal.components.PublicFooterComponent;
import com.vitalsphere.publicportal.layouts.PublicLayout;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.services.SampleDataGeneratorService;

import java.util.List;

/**
 * Section 6, Module 4: Find Blood Availability search engine.
 */
@Route(value = "find-blood", layout = PublicLayout.class)
@PageTitle("Find Blood Availability — VitalSphere")
@AnonymousAllowed
public class FindBloodView extends VerticalLayout implements HasUrlParameter<String> {

    private final VitalSphereDataStore dataStore;
    private final Grid<InventoryItem> inventoryGrid = new Grid<>(InventoryItem.class, false);
    private final ComboBox<BloodGroup> bloodGroupCombo = new ComboBox<>("Blood Group");
    private final ComboBox<String> districtCombo = new ComboBox<>("District (Andhra Pradesh)");
    private final ComboBox<BloodComponent> componentCombo = new ComboBox<>("Blood Component");
    private final Span resultCountSpan = new Span();

    public FindBloodView(VitalSphereDataStore dataStore) {
        this.dataStore = dataStore;
        setWidthFull();
        setPadding(false);

        VerticalLayout content = new VerticalLayout();
        content.setWidthFull();
        content.getStyle().set("padding", "32px");

        H2 title = new H2("Find Blood Availability in Andhra Pradesh");
        title.getStyle().set("color", "#142B4A").set("margin-bottom", "6px");

        Paragraph subtitle = new Paragraph("Search verified sample stock reserves across authorized district blood banks and charitable centers. All stock figures are simulated for academic prototyping.");
        subtitle.getStyle().set("color", "#64748B");

        // Filter Bar
        HorizontalLayout filterBar = new HorizontalLayout();
        filterBar.setWidthFull();
        filterBar.setAlignItems(FlexComponent.Alignment.END);
        filterBar.getStyle().set("background-color", "#FFFFFF").set("padding", "20px").set("border-radius", "8px").set("border", "1px solid #E2E8F0");

        bloodGroupCombo.setItems(BloodGroup.values());
        bloodGroupCombo.setItemLabelGenerator(BloodGroup::getLabel);
        bloodGroupCombo.setPlaceholder("All Groups");
        bloodGroupCombo.setClearButtonVisible(true);

        districtCombo.setItems(SampleDataGeneratorService.AP_DISTRICTS);
        districtCombo.setPlaceholder("All Districts");
        districtCombo.setClearButtonVisible(true);

        componentCombo.setItems(BloodComponent.values());
        componentCombo.setItemLabelGenerator(BloodComponent::getDisplayName);
        componentCombo.setPlaceholder("All Components");
        componentCombo.setClearButtonVisible(true);

        Button searchBtn = new Button("Search Inventory", e -> performSearch());
        searchBtn.addThemeVariants(ButtonVariant.LUMO_PRIMARY);
        searchBtn.addClassName("btn-primary-vital");

        Button resetBtn = new Button("Reset", e -> {
            bloodGroupCombo.clear();
            districtCombo.clear();
            componentCombo.clear();
            performSearch();
        });

        filterBar.add(bloodGroupCombo, districtCombo, componentCombo, searchBtn, resetBtn);

        // Results Grid
        configureGrid();

        content.add(title, subtitle, filterBar, resultCountSpan, inventoryGrid);
        add(content, new PublicFooterComponent());

        performSearch();
    }

    private void configureGrid() {
        inventoryGrid.setWidthFull();
        inventoryGrid.getStyle().set("min-height", "450px");

        inventoryGrid.addColumn(item -> item.getBloodGroup().getCode())
                .setHeader("Blood Group")
                .setWidth("120px")
                .setFlexGrow(0);

        inventoryGrid.addColumn(item -> item.getComponent().getDisplayName())
                .setHeader("Component")
                .setWidth("220px");

        inventoryGrid.addColumn(InventoryItem::getBloodBankName)
                .setHeader("Blood Bank & Medical Center")
                .setFlexGrow(2);

        inventoryGrid.addColumn(InventoryItem::getDistrict)
                .setHeader("District")
                .setWidth("160px");

        inventoryGrid.addColumn(item -> item.getUnitsAvailable() + " Units")
                .setHeader("Stock Available")
                .setWidth("140px");

        inventoryGrid.addColumn(item -> item.getExpiryDate().toString())
                .setHeader("Expiry Benchmark")
                .setWidth("140px");

        inventoryGrid.addComponentColumn(item -> {
            Button reqBtn = new Button("Request", e -> UI.getCurrent().navigate("request-blood?bank=" + item.getBloodBankName()));
            reqBtn.addThemeVariants(ButtonVariant.LUMO_SMALL, ButtonVariant.LUMO_PRIMARY);
            reqBtn.addClassName("btn-primary-vital");
            return reqBtn;
        }).setHeader("Action").setWidth("120px");
    }

    private void performSearch() {
        BloodGroup selectedGroup = bloodGroupCombo.getValue();
        String selectedDistrict = districtCombo.getValue();
        BloodComponent selectedComponent = componentCombo.getValue();

        List<InventoryItem> items = dataStore.findInventoryByFilters(selectedGroup, selectedDistrict, selectedComponent);
        inventoryGrid.setItems(items);
        resultCountSpan.setText(String.format("Showing %d sample inventory units matching criteria in Andhra Pradesh.", items.size()));
        resultCountSpan.getStyle().set("font-weight", "600").set("color", "#142B4A").set("margin-top", "12px");
    }

    @Override
    public void setParameter(BeforeEvent event, @OptionalParameter String parameter) {
        Location location = event.getLocation();
        QueryParameters queryParameters = location.getQueryParameters();
        if (queryParameters.getParameters().containsKey("group")) {
            String groupCode = queryParameters.getParameters().get("group").get(0);
            BloodGroup group = BloodGroup.fromCode(groupCode);
            if (group != null) {
                bloodGroupCombo.setValue(group);
                performSearch();
            }
        }
    }
}
