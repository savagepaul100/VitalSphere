package com.vitalsphere.firebase;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.firestore.Firestore;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.cloud.FirestoreClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

/**
 * Firebase Configuration with resilient Cloud Firestore connection and graceful local mock fallback.
 */
@Configuration
public class FirebaseConfig {

    private static final Logger log = LoggerFactory.getLogger(FirebaseConfig.class);

    @Value("${vitalsphere.firebase.credentials-path:}")
    private String credentialsPath;

    @Value("${vitalsphere.firebase.project-id:vitalsphere-demo-db}")
    private String projectId;

    @Value("${vitalsphere.firebase.storage-bucket:vitalsphere-demo.appspot.com}")
    private String storageBucket;

    @Bean
    public FirebaseApp firebaseApp() {
        if (!FirebaseApp.getApps().isEmpty()) {
            return FirebaseApp.getInstance();
        }

        try {
            FirebaseOptions.Builder optionsBuilder = FirebaseOptions.builder()
                    .setProjectId(projectId)
                    .setStorageBucket(storageBucket);

            InputStream serviceAccount = null;
            if (credentialsPath != null && !credentialsPath.trim().isEmpty()) {
                File file = new File(credentialsPath.trim());
                if (file.exists()) {
                    serviceAccount = new FileInputStream(file);
                    log.info("VitalSphere: Loading Firebase credentials from file: {}", credentialsPath);
                }
            }

            if (serviceAccount == null) {
                // Try environment variable or classpath
                String googleAppCreds = System.getenv("GOOGLE_APPLICATION_CREDENTIALS");
                if (googleAppCreds != null && new File(googleAppCreds).exists()) {
                    serviceAccount = new FileInputStream(googleAppCreds);
                    log.info("VitalSphere: Loading Firebase credentials from GOOGLE_APPLICATION_CREDENTIALS");
                }
            }

            if (serviceAccount != null) {
                optionsBuilder.setCredentials(GoogleCredentials.fromStream(serviceAccount));
                FirebaseApp app = FirebaseApp.initializeApp(optionsBuilder.build());
                log.info("VitalSphere: FirebaseApp successfully connected to Project: {}", projectId);
                return app;
            } else {
                log.warn("VitalSphere: No external Firebase service account provided. Operating in safe In-Memory / Simulated Firestore Sync mode for academic demonstration.");
                return null;
            }
        } catch (IOException e) {
            log.warn("VitalSphere: Could not initialize live Firebase credentials ({}). Operating in Simulated Firestore Mode.", e.getMessage());
            return null;
        }
    }

    @Bean
    public Firestore firestore(FirebaseApp firebaseApp) {
        if (firebaseApp != null) {
            try {
                return FirestoreClient.getFirestore(firebaseApp);
            } catch (Exception e) {
                log.warn("VitalSphere: Unable to create live Firestore client. Using in-memory fallback. Reason: {}", e.getMessage());
            }
        }
        return null; // Repositories will gracefully fall back to synchronized thread-safe in-memory collections
    }
}
