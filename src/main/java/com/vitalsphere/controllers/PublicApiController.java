package com.vitalsphere.controllers;

import com.vitalsphere.models.DonationRecord;
import com.vitalsphere.repositories.VitalSphereDataStore;
import com.vitalsphere.services.CertificateGeneratorService;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Public REST Controller for simulated digital certificate downloads and stats.
 */
@RestController
@RequestMapping("/api/public")
public class PublicApiController {

    private final VitalSphereDataStore dataStore;
    private final CertificateGeneratorService certificateService;

    public PublicApiController(VitalSphereDataStore dataStore, CertificateGeneratorService certificateService) {
        this.dataStore = dataStore;
        this.certificateService = certificateService;
    }

    @GetMapping("/certificates/{id}")
    public ResponseEntity<byte[]> downloadCertificate(@PathVariable String id) {
        var opt = dataStore.findAllDonations().stream().filter(d -> d.getId().equals(id)).findFirst();
        DonationRecord rec = opt.orElseGet(() -> {
            var all = dataStore.findAllDonations();
            return all.isEmpty() ? null : all.get(0);
        });

        if (rec == null) {
            return ResponseEntity.notFound().build();
        }

        byte[] pdfBytes = certificateService.generateDonationCertificate(rec);
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"VitalSphere-Certificate-" + rec.getId() + ".pdf\"")
                .contentType(MediaType.APPLICATION_PDF)
                .body(pdfBytes);
    }
}
