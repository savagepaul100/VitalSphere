package com.vitalsphere.services;

import com.lowagie.text.*;
import com.lowagie.text.pdf.PdfWriter;
import com.vitalsphere.models.DonationRecord;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.awt.Color;

/**
 * Section 13, Feature F: Digital PDF Certificate generator written in Java.
 */
@Service
public class CertificateGeneratorService {

    public byte[] generateDonationCertificate(DonationRecord rec) {
        try {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            Document document = new Document(PageSize.A4.rotate(), 36, 36, 36, 36);
            PdfWriter.getInstance(document, out);
            document.open();

            // Fonts
            Font titleFont = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 24, new Color(20, 43, 74));
            Font subTitleFont = FontFactory.getFont(FontFactory.HELVETICA, 14, new Color(100, 116, 139));
            Font donorFont = FontFactory.getFont(FontFactory.HELVETICA_BOLD, 22, new Color(214, 40, 57));
            Font bodyFont = FontFactory.getFont(FontFactory.HELVETICA, 12, new Color(15, 23, 42));
            Font footerFont = FontFactory.getFont(FontFactory.HELVETICA_OBLIQUE, 9, new Color(100, 116, 139));

            // Header
            Paragraph title = new Paragraph("VITALSPHERE NATIONAL HEALTHCARE PLATFORM", titleFont);
            title.setAlignment(Element.ALIGN_CENTER);
            document.add(title);

            Paragraph subtitle = new Paragraph("CERTIFICATE OF VOLUNTARY BLOOD DONATION APPRECIATION", subTitleFont);
            subtitle.setAlignment(Element.ALIGN_CENTER);
            subtitle.setSpacingAfter(24);
            document.add(subtitle);

            // Body
            Paragraph presentedTo = new Paragraph("This is honorably presented to", bodyFont);
            presentedTo.setAlignment(Element.ALIGN_CENTER);
            document.add(presentedTo);

            Paragraph donorName = new Paragraph(rec.getDonorName(), donorFont);
            donorName.setAlignment(Element.ALIGN_CENTER);
            donorName.setSpacingAfter(16);
            document.add(donorName);

            String bodyText = String.format(
                    "In grateful recognition of the voluntary, non-remunerated donation of Whole Blood (%s) on %s at %s. " +
                    "Your selfless contribution brings life, vitality, and hope to patients across Andhra Pradesh.",
                    rec.getBloodGroup() != null ? rec.getBloodGroup().getCode() : "N/A",
                    rec.getDonationDate(),
                    rec.getBloodBankOrCamp()
            );

            Paragraph desc = new Paragraph(bodyText, bodyFont);
            desc.setAlignment(Element.ALIGN_CENTER);
            desc.setSpacingAfter(36);
            document.add(desc);

            // Certificate Details
            Paragraph meta = new Paragraph(String.format("Certificate ID: %s | Status: %s | DEMONSTRATION RECORD", rec.getId(), rec.getStatus()), footerFont);
            meta.setAlignment(Element.ALIGN_CENTER);
            document.add(meta);

            document.close();
            return out.toByteArray();
        } catch (Exception e) {
            throw new RuntimeException("Error generating PDF certificate: " + e.getMessage(), e);
        }
    }
}
