package com.vitalsphere;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;

public class VitalSphereScreenshotter {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                // Set system look and feel
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());

                VitalSphereDesktopClient client = new VitalSphereDesktopClient();
                client.setSize(1280, 820);
                client.setLocationRelativeTo(null);
                client.setVisible(true);

                // Give it a moment to layout
                Thread.sleep(600);

                File dir = new File("target/screenshots");
                dir.mkdirs();

                // 1. Capture Main Window (Donors live roster)
                captureComponent(client, "target/screenshots/java_client_donors.png");

                // Find tabbed pane inside client
                JTabbedPane tabs = findTabbedPane(client);
                if (tabs != null) {
                    // 2. Capture Recipients tab
                    tabs.setSelectedIndex(1);
                    Thread.sleep(300);
                    captureComponent(client, "target/screenshots/java_client_recipients.png");

                    // 3. Capture Approvals / Clearance Desk tab
                    tabs.setSelectedIndex(2);
                    Thread.sleep(300);
                    captureComponent(client, "target/screenshots/java_client_clearance.png");

                    // 4. Capture Emergency Request Registration tab
                    tabs.setSelectedIndex(3);
                    Thread.sleep(300);
                    captureComponent(client, "target/screenshots/java_client_emergency_request.png");

                    // Reset to first tab
                    tabs.setSelectedIndex(0);
                }

                System.out.println("JAVA_SCREENSHOTS_CAPTURED_SUCCESSFULLY");
                client.dispose();
                System.exit(0);
            } catch (Exception e) {
                e.printStackTrace();
                System.exit(1);
            }
        });
    }

    private static JTabbedPane findTabbedPane(Container container) {
        for (Component c : container.getComponents()) {
            if (c instanceof JTabbedPane) {
                return (JTabbedPane) c;
            } else if (c instanceof Container) {
                JTabbedPane found = findTabbedPane((Container) c);
                if (found != null) return found;
            }
        }
        return null;
    }

    private static void captureComponent(Component comp, String path) throws Exception {
        BufferedImage img = new BufferedImage(comp.getWidth(), comp.getHeight(), BufferedImage.TYPE_INT_RGB);
        Graphics2D g2 = img.createGraphics();
        comp.paint(g2);
        g2.dispose();
        ImageIO.write(img, "png", new File(path));
        System.out.println("Captured: " + path);
    }
}
