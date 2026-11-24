// Pan-India States and Districts / Major Cities
export const INDIA_STATES_DATA = {
  "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Kurnool", "Kakinada", "Nellore", "Kadapa", "Anantapur", "Eluru", "Rajahmundry", "Vizianagaram", "Ongole", "Chittoor", "Machilipatnam"],
  "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Ramagundam", "Mahabubnagar", "Nalgonda", "Adilabad", "Suryapet"],
  "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", "Amravati", "Navi Mumbai", "Kolhapur", "Akola", "Latur"],
  "Karnataka": ["Bengaluru", "Mysuru", "Hubballi-Dharwad", "Mangaluru", "Belagavi", "Kalaburagi", "Davanagere", "Ballari", "Vijayapura", "Shivamogga"],
  "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Tiruppur", "Vellore", "Erode", "Thoothukudi", "Dindigul"],
  "Delhi NCR": ["New Delhi", "North Delhi", "South Delhi", "West Delhi", "East Delhi", "Noida", "Gurugram", "Faridabad", "Ghaziabad"],
  "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Gandhinagar", "Junagadh", "Anand", "Navsari", "Morbi"],
  "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj", "Meerut", "Bareilly", "Aligarh", "Moradabad", "Saharanpur", "Gorakhpur", "Noida"],
  "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman", "Malda", "Kharagpur", "Haldia"],
  "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Kollam", "Thrissur", "Kannur", "Alappuzha", "Kottayam", "Palakkad"],
  "Rajasthan": ["Jaipur", "Jodhpur", "Kota", "Bikaner", "Ajmer", "Udaipur", "Bhilwara", "Alwar", "Bharatpur", "Sikar"],
  "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Dewas", "Satna", "Ratlam"],
  "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Bihar Sharif", "Arrah"],
  "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Hoshiarpur"],
  "Haryana": ["Faridabad", "Gurugram", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal"],
  "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore"],
  "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur"],
  "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh"],
  "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur", "Rishikesh"],
  "Goa": ["North Goa (Panaji)", "South Goa (Margao)", "Vasco da Gama", "Mapusa", "Ponda"]
};

const FIRST_NAMES = [
  "Aarav", "Aditi", "Akhil", "Ananya", "Bhavani", "Chaitanya", "Deepika", "Dinesh",
  "Gowri", "Harish", "Ishaan", "Kavya", "Krishna", "Lakshmi", "Madhav", "Manish",
  "Naveen", "Pallavi", "Praneeth", "Priya", "Rahul", "Rajesh", "Ramana", "Sai",
  "Sandeep", "Sneha", "Srinivas", "Suresh", "Surya", "Swapna", "Tarun", "Varun",
  "Venkatesh", "Vidya", "Vijay", "Vikram", "Yashwant", "Rohan", "Tanvi", "Arjun"
];

const LAST_NAMES = [
  "Reddy", "Rao", "Chowdary", "Varma", "Naidu", "Sharma", "Murthy", "Sastry",
  "Raju", "Prasad", "Babu", "Kumar", "Gupta", "Pillai", "Patnaik", "Devi",
  "Deshmukh", "Patil", "Iyer", "Banerjee", "Singh", "Verma", "Mehta", "Joshi"
];

const BLOOD_GROUPS = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"];
const ALL_STATES = Object.keys(INDIA_STATES_DATA);

// Generate 256 realistic Pan-India donors
export const fullDonorsList = [];
for (let i = 1; i <= 256; i++) {
  const fn = FIRST_NAMES[i % FIRST_NAMES.length];
  const ln = LAST_NAMES[(i * 3) % LAST_NAMES.length];
  const bg = BLOOD_GROUPS[i % BLOOD_GROUPS.length];
  const st = ALL_STATES[i % ALL_STATES.length];
  const cities = INDIA_STATES_DATA[st];
  const city = cities[i % cities.length];
  const daysRest = 90 + ((i * 7) % 65);
  const hb = (12.6 + ((i % 25) * 0.12)).toFixed(1);
  const aadhaarLast4 = String(1000 + ((i * 37) % 8999));
  const isDonated = (i % 3 === 0);
  const isFit = hb >= 12.5;

  fullDonorsList.push({
    id: `DNR-${String(i).padStart(3, '0')}`,
    name: `${fn} ${ln}`,
    aadhaar: `XXXX-XXXX-${aadhaarLast4}`,
    bloodGroup: bg,
    state: st,
    city: city,
    district: `${city}, ${st}`,
    healthStatus: isFit ? `FIT (Hb: ${hb} g/dL, Rest: ${daysRest}d)` : `BORDERLINE (Hb: ${hb} g/dL)`,
    fitClass: isFit ? "status-fit" : "status-borderline",
    medicalProof: i % 2 === 0 ? "Registered Physician Medical Certificate" : "Hospital Blood Test Card",
    groupProof: i % 3 === 0 ? "Clinical Pathology Lab Certificate" : "Official Red Cross Donor Card",
    mobile: `+91 98${String(10000000 + (i * 33333)).slice(0, 8)}`,
    verification: "APPROVED_BY_MEDICAL_OFFICER",
    donationState: isDonated ? "Already Donated (Verified History)" : "Ready to Donate (Eligible Now)"
  });
}

// Generate 32 recipients across India who want blood
export const fullRecipientsList = [];
const HOSPITALS = [
  "Apollo Speciality Hospital", "Government General Hospital", "Fortis Healthcare",
  "Manipal Hospital", "AIIMS Hospital", "Care Hospitals", "Narayana Health",
  "Lilavati Hospital", "Max Super Speciality Hospital", "Red Cross Transfusion Center"
];

const URGENCIES = ["CRITICAL", "URGENT", "ROUTINE"];

for (let j = 1; j <= 32; j++) {
  const pfn = FIRST_NAMES[(j * 2) % FIRST_NAMES.length];
  const pln = LAST_NAMES[(j * 5) % LAST_NAMES.length];
  const bg = BLOOD_GROUPS[(j * 2) % BLOOD_GROUPS.length];
  const st = ALL_STATES[(j * 2) % ALL_STATES.length];
  const cities = INDIA_STATES_DATA[st];
  const city = cities[(j * 3) % cities.length];
  const hosp = `${HOSPITALS[j % HOSPITALS.length]}, ${city}`;
  const units = (j % 4) + 1;
  const ml = units * 350;
  const urg = URGENCIES[j % URGENCIES.length];
  const aadhaarLast4 = String(2000 + ((j * 43) % 7999));

  fullRecipientsList.push({
    id: `REQ-${String(8000 + j)}`,
    patientName: `${pfn} ${pln}`,
    aadhaar: `XXXX-XXXX-${aadhaarLast4}`,
    bloodGroup: bg,
    units: `${units} Unit${units > 1 ? 's' : ''} (${ml} ml)`,
    hospital: hosp,
    state: st,
    city: city,
    district: `${city}, ${st}`,
    urgency: urg,
    urgencyClass: urg === 'CRITICAL' ? 'status-critical' : (urg === 'URGENT' ? 'status-urgent' : 'status-routine'),
    contact: `+91 97${String(20000000 + (j * 44444)).slice(0, 8)}`,
    status: j % 3 === 0 ? "ALLOCATED" : "LOOKING_FOR_DONORS"
  });
}
