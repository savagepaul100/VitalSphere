# VitalSphere — Smart Blood Donation & Healthcare Coordination Platform

> **Connecting Lives. Empowering Hope.**  
> An academic, Java-first healthcare engineering prototype connecting voluntary donors, authorized blood banks, hospitals, and recipients with verified clinical eligibility standards.

---

## 1. Project Overview & Identity
- **Category:** Smart Blood Donation & Healthcare Coordination Platform
- **Focus Region:** Andhra Pradesh (26 districts referenced)
- **Primary Technology:** 100% Java (Java 21 LTS, Spring Boot 3.3.4, Vaadin Flow 24, Firebase Admin SDK)
- **Architecture:** Zero-JS UI framework overhead; Java views, event listeners, clinical evaluation engines, and reactive data synchronization.
- **Data Compliance:** Academic demonstration with realistic simulated records; strictly **no Aadhaar collection**, no private blood sales, and no automated diagnostic clearance.

---

## 2. Technology Stack
- **Language:** OpenJDK 21 LTS
- **Backend Framework:** Spring Boot 3.3.4, Spring Security 6
- **Frontend / UI:** Vaadin Flow 24.4 (Java-centric component hierarchy, responsive layouts, Lumo theme customization)
- **Cloud Backend:** Google Cloud Firebase Admin SDK for Firestore & Firebase Cloud Storage
- **Barcode & QR Engine:** ZXing 3.5.3 (camp attendance & pass verification)
- **Certificate Generator:** OpenPDF 2.0.2 (vector PDF certificates generated server-side in Java)
- **Build System:** Apache Maven 3.9.6

---

## 3. Architecture & User Portals

VitalSphere enforces complete architectural separation between citizen services and administrative authority tools:

### A. Public Website (`PublicLayout.java`)
- `/` — **Homepage:** Government-inspired top banner, hero headline, real-time counter metrics, Andhra Pradesh stock overview, emergency requirements, camp teasers, workflow steps, NBTC eligibility rules, and FAQ.
- `/find-blood` — **Search Engine:** Filter by blood group, district, and component (PRBC, FFP, Platelets, Whole Blood).
- `/donate` — **Donation & Screening:** Preliminary clinical self-evaluation (hemoglobin, weight, age, recent infection, and cooldown rest tracking).
- `/camps` — **Donation Camps:** Camp listing, venue, date/timings, slot availability, and instant slot registration.
- `/request-blood` — **Blood Request Form:** Inpatient hospital requirement submission with urgency grading (Critical / Urgent / Routine).
- `/awareness` — **Clinical Matrix:** Complete red cell transfusion compatibility table and pre/post-donation care guides.
- `/dashboard` — **Donor Dashboard:** Cooldown rest status countdown, previous donation logs, and digital appreciation certificates.
- `/login` & `/register` — **Authentication:** Citizen and administrative sign-in with simulated identity checks.

### B. Administration Portal (`AdminLayout.java`)
- `/admin/dashboard` — **Command Center:** Real-time metrics across 1,000 donors, 100 blood banks, 100 camps, and 800 inventory batches.
- `/admin/donors` — **Donor Management:** Directory search by name, email, blood group, and district.
- `/admin/medical-verification` — **Clinical Clearance:** Confidential Medical Officer review console for reviewing hemoglobin, BP, weight, and temporary/permanent deferrals.
- `/admin/blood-banks` — **Blood Bank Registry:** Accredited CDSCO license directory, contact helplines, and component unit status.
- `/admin/inventory` — **Inventory Control:** Batch numbers, expiry monitoring, and reserves per center.
- `/admin/requests` — **Blood Allocation:** Medical review and fulfillment of patient emergency requirements.
- `/admin/camps` — **Camp Management:** Schedule and monitor collection targets and attendance.
- `/admin/audit-logs` — **Audit Trail:** Immutable logging of administrative actions, medical clearances, and allocations.

---

## 4. Role-Based Access Control (RBAC)
VitalSphere implements 10 distinct RBAC roles defined in `UserRole.java`:
1. `SUPER_ADMIN`
2. `NATIONAL_AUTHORITY`
3. `STATE_AUTHORITY`
4. `DISTRICT_AUTHORITY`
5. `BLOOD_BANK_ADMIN`
6. `MEDICAL_OFFICER`
7. `CAMP_ORGANIZER`
8. `SUPPORT_STAFF`
9. `DONOR`
10. `RECIPIENT`

### Demo Credentials (Pre-seeded):
| Role | Email | Password |
| :--- | :--- | :--- |
| **Super Admin** | `admin@vitalsphere.gov.in` | `Admin@VitalSphere2026` |
| **Medical Officer** | `doctor.sharma@vitalsphere.gov.in` | `Doctor@2026` |
| **Blood Bank Admin** | `bloodbank.vizag@vitalsphere.gov.in` | `Bank@2026` |
| **Camp Organizer** | `organizer.ap@vitalsphere.gov.in` | `Camp@2026` |
| **Voluntary Donor** | `donor@vitalsphere.demo` | `Donor@2026` |

---

## 5. Clinical Reference Rules & Cooldown Engine
- **Whole Blood Cooldown:** 90 days for male donors, 120 days for female donors.
- **Statutory Age Benchmark:** 18 to 65 years.
- **Minimum Body Weight:** 45.0 kg.
- **Minimum Hemoglobin Standard:** 12.5 g/dL.
- **Status Classification:** `PENDING`, `UNDER_REVIEW`, `CLEARED_FOR_ASSESSMENT`, `REQUIRES_ADDITIONAL_REVIEW`, `TEMPORARILY_DEFERRED`, `PERMANENTLY_DEFERRED`.

---

## 6. Seed Data Scale (Section 12)
- **1,000 Donors:** Realistic Andhra Pradesh names, contact numbers, and district distributions.
- **100 Blood Banks:** Accredited government hospitals, Red Cross societies, and charitable centers.
- **100 Camps:** Mega camps across all AP districts with start/end timings and venue addresses.
- **800 Inventory Records:** Whole blood, PRBC, FFP, and platelets with batch numbers and shelf-life calculations.
- **250 Blood Requests:** Emergency and inpatient hospital transfusion cases.
- **500 Donations:** Historical records with certificate reference IDs.

---

## 7. How to Run & Build

### Running the Application:
```powershell
mvn spring-boot:run
```
Once started, navigate to:
- **Public Portal:** `http://localhost:8080`
- **Administration Command Center:** `http://localhost:8080/admin`

### Running the Test Suite:
```powershell
mvn test
```
All unit tests in `VitalSphereClinicalEngineTests.java` pass with 0 failures, validating ABO/Rh compatibility, cooldown rest intervals, underage permanent deferrals, and seed data initialization.
