
import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.chat import SchemeCard, SourceDocument, UserDemographics


# Comprehensive seed knowledge base of major Indian Government Schemes
INDIAN_SCHEMES_KNOWLEDGE: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "PM Kisan Samman Nidhi (PM-KISAN)",
        "title_hi": "प्रधानमंत्री किसान सम्मान निधि",
        "department": "Ministry of Agriculture & Farmers Welfare",
        "category": "Agriculture",
        "level": "Central",
        "state": "All India",
        "benefits": "₹6,000 per year paid in three equal installments of ₹2,000 directly transferred into bank accounts (DBT).",
        "eligibility_criteria": "Small and marginal landholder farmer families with cultivable land in their names. Institutional landholders, serving/retired government employees, and income tax payers are excluded.",
        "required_documents": "Aadhaar Card, Land ownership papers (Khatauni/Khasra), Active Bank Account linked with Aadhaar, Mobile Number.",
        "application_process": "1. Visit pmkisan.gov.in -> 'New Farmer Registration'. 2. Enter Aadhaar & Mobile OTP. 3. Enter Land Details & upload records. 4. eKYC completion.",
        "application_url": "https://pmkisan.gov.in",
        "helpline": "155261 / 011-24300606",
        "keywords": ["farmer", "kisan", "agriculture", "land", "crop", "farming", "6000", "kheti", "seed", "tractor"]
    },
    {
        "id": 2,
        "title": "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)",
        "title_hi": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना",
        "department": "National Health Authority (Ministry of Health and Family Welfare)",
        "category": "Healthcare",
        "level": "Central",
        "state": "All India",
        "benefits": "Cashless health cover up to ₹5,00,000 per family per year for secondary and tertiary care hospitalization across empanelled public & private hospitals.",
        "eligibility_criteria": "Households identified under rural & urban deprivations in SECC 2011 database, all senior citizens aged 70+ (under expanded PMJAY 2024+ regardless of income), and RSBY beneficiaries.",
        "required_documents": "Aadhaar Card, Ration Card / Parivar Pehchan Patra, Registered Mobile Number.",
        "application_process": "1. Check eligibility on beneficiary.nha.gov.in or Ayushman App. 2. Verify via Aadhaar eKYC. 3. Download Ayushman Golden Card.",
        "application_url": "https://beneficiary.nha.gov.in",
        "helpline": "14555",
        "keywords": ["health", "hospital", "ayushman", "insurance", "medical", "treatment", "doctor", "swasthya", "operation", "disease", "illness", "5 lakh"]
    },
    {
        "id": 3,
        "title": "Pradhan Mantri Awas Yojana - Gramin & Urban (PMAY)",
        "title_hi": "प्रधानमंत्री आवास योजना",
        "department": "Ministry of Housing and Urban Affairs / Ministry of Rural Development",
        "category": "Housing",
        "level": "Central",
        "state": "All India",
        "benefits": "Financial assistance of ₹1.20 Lakh (plains) to ₹1.30 Lakh (hilly areas) for rural construction, and interest subsidy up to 6.5% on home loans under Credit Linked Subsidy Scheme (CLSS) in urban areas.",
        "eligibility_criteria": "Families with no pucca house in their name anywhere in India. Economically Weaker Sections (EWS with income < ₹3 Lakh/yr) and Low Income Groups (LIG < ₹6 Lakh/yr).",
        "required_documents": "Aadhaar Card, Bank Passbook, Land/Property documents, Income Certificate, No-pucca house affidavit, MNREGA Job Card (for Gramin).",
        "application_process": "1. Urban: Apply via pmaymis.gov.in or CSC Center. 2. Rural: Contact Gram Panchayat / Block Development Officer (BDO) for Gramin survey list inclusion.",
        "application_url": "https://pmaymis.gov.in",
        "helpline": "011-23060484 / 1800-11-6163",
        "keywords": ["house", "housing", "pucca makan", "home loan", "subsidy", "flat", "makan", "ghar", "awas", "shelter"]
    },
    {
        "id": 4,
        "title": "Pradhan Mantri Mudra Yojana (PMMY)",
        "title_hi": "प्रधानमंत्री मुद्रा योजना",
        "department": "Department of Financial Services (Ministry of Finance)",
        "category": "Financial Services & Business",
        "level": "Central",
        "state": "All India",
        "benefits": "Collateral-free business loans up to ₹20 Lakh in 4 categories: Shishu (up to ₹50,000), Kishore (₹50,000 - ₹5 Lakh), Tarun (₹5 Lakh - ₹10 Lakh), and Tarun Plus (up to ₹20 Lakh).",
        "eligibility_criteria": "Any Indian citizen with a business plan for non-farm income-generating activities such as manufacturing, processing, trading, or service sector.",
        "required_documents": "Aadhaar Card, PAN Card, Business Address Proof, Project Report / Quotations for machinery, Bank Statements (last 6 months).",
        "application_process": "1. Prepare business proposal. 2. Apply via Udyamimitra portal (udyamimitra.in) or visit any commercial bank / RRB / NBFC branch.",
        "application_url": "https://www.mudra.org.in",
        "helpline": "1800-180-1111",
        "keywords": ["loan", "business", "startup", "shop", "mudra", "shishu", "kishore", "tarun", "dukan", "vyapar", "capital", "collateral free"]
    },
    {
        "id": 5,
        "title": "Sukanya Samriddhi Yojana (SSY)",
        "title_hi": "सुकन्या समृद्धि योजना",
        "department": "Ministry of Finance",
        "category": "Women & Child",
        "level": "Central",
        "state": "All India",
        "benefits": "High sovereign-guaranteed interest rate (currently ~8.2% p.a.), Section 80C tax deduction, and complete tax-free maturity amount for girl child education and marriage.",
        "eligibility_criteria": "Parents or legal guardians of a girl child aged up to 10 years. Maximum 2 accounts per family (or 3 in case of twins/triplets).",
        "required_documents": "Birth Certificate of girl child, Aadhaar & ID proof of parent/guardian, Address proof, Initial deposit amount (min ₹250).",
        "application_process": "1. Visit any Post Office or authorised Public/Private Bank branch. 2. Fill SSY Form-1. 3. Deposit initial minimum ₹250.",
        "application_url": "https://www.indiapost.gov.in",
        "helpline": "1800-266-6868",
        "keywords": ["girl", "daughter", "child", "sukanya", "beti", "bachat", "education", "marriage", "women", "post office", "interest"]
    },
    {
        "id": 6,
        "title": "PM Vishwakarma Yojana",
        "title_hi": "पीएम विश्वकर्मा योजना",
        "department": "Ministry of Micro, Small and Medium Enterprises (MSME)",
        "category": "Employment & Skill",
        "level": "Central",
        "state": "All India",
        "benefits": "Recognition as Vishwakarma with ID card, ₹500/day stipend during 5-7 days basic skill training, ₹15,000 toolkit incentive, and collateral-free enterprise loan up to ₹3 Lakh at 5% concessional interest.",
        "eligibility_criteria": "Traditional artisans and craftspeople working with hands and tools across 18 specified trades (Carpenter, Blacksmith, Potter, Tailor, Cobbler, Mason, etc.). Minimum age 18 years.",
        "required_documents": "Aadhaar Card, Mobile Number, Bank Account Details, Ration Card (for family verification).",
        "application_process": "1. Visit nearest CSC (Common Services Center). 2. Submit trade and Aadhaar biometric verification. 3. Complete Gram Panchayat / ULB verification.",
        "application_url": "https://pmvishwakarma.gov.in",
        "helpline": "1800-267-7777",
        "keywords": ["artisan", "carpenter", "tailor", "blacksmith", "craftsman", "darzi", "badhai", "lohar", "kumhar", "vishwakarma", "toolkit", "15000", "skill"]
    },
    {
        "id": 7,
        "title": "PM SVANidhi (Street Vendor's AtmaNirbhar Nidhi)",
        "title_hi": "पीएम स्वनिधि योजना",
        "department": "Ministry of Housing and Urban Affairs",
        "category": "Financial Services & Business",
        "level": "Central",
        "state": "All India",
        "benefits": "Micro-credit working capital loan: 1st tranche up to ₹10,000, 2nd tranche up to ₹20,000, and 3rd tranche up to ₹50,000 with 7% interest subsidy and cashback on digital transactions.",
        "eligibility_criteria": "Street vendors / hawkers vending in urban areas possessing Certificate of Vending / ID card issued by Urban Local Bodies (ULBs).",
        "required_documents": "Aadhaar Card, Vending Certificate / LOR (Letter of Recommendation from Municipality), Bank Account Details.",
        "application_process": "1. Register on pmsvanidhi.mohua.gov.in or via PM SVANidhi Mobile App. 2. Select preferred lending bank.",
        "application_url": "https://pmsvanidhi.mohua.gov.in",
        "helpline": "1800-11-1979",
        "keywords": ["street vendor", "hawker", "thela", "rehri", "patri", "svanidhi", "vendor loan", "10000", "working capital"]
    },
    {
        "id": 8,
        "title": "Atal Pension Yojana (APY)",
        "title_hi": "अटल पेंशन योजना",
        "department": "Pension Fund Regulatory and Development Authority (PFRDA)",
        "category": "Social Welfare & Pension",
        "level": "Central",
        "state": "All India",
        "benefits": "Guaranteed monthly pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000, or ₹5,000 per month starting at age 60 until lifetime.",
        "eligibility_criteria": "All Indian citizens between 18 to 40 years holding a savings bank account. Must not be an income tax payer as per latest guidelines.",
        "required_documents": "Aadhaar Card, Savings Bank / Post Office Account, Active Mobile Number.",
        "application_process": "1. Visit the bank where you hold your savings account. 2. Fill APY Registration Form. 3. Set auto-debit facility for monthly contribution.",
        "application_url": "https://www.npscra.nsdl.co.in",
        "helpline": "1800-110-069",
        "keywords": ["pension", "old age", "senior citizen", "retirement", "monthly pension", "atal pension", "apy", "60 years", "saving"]
    },
    {
        "id": 9,
        "title": "National Scholarship Portal (NSP) - Post-Matric & Pre-Matric",
        "title_hi": "राष्ट्रीय छात्रवृत्ति पोर्टल (छात्रवृत्ति योजनाएं)",
        "department": "Ministry of Social Justice, Tribal Affairs, Minority Affairs, and Education",
        "category": "Education",
        "level": "Central",
        "state": "All India",
        "benefits": "Direct financial assistance for school/college tuition fees, maintenance allowance, and study materials.",
        "eligibility_criteria": "Students from SC, ST, OBC, Minority, and EWS categories with family annual income typically below ₹2.5 Lakh/year (scheme specific) studying in recognized institutions.",
        "required_documents": "Student Aadhaar Card, Income Certificate, Caste/Category Certificate, Previous Year Marksheets, Fee Receipt, Bank Passbook, Institute Verification Form.",
        "application_process": "1. Register on scholarships.gov.in with One Time Registration (OTR). 2. Complete biometric authentication. 3. Select eligible scheme and submit institution verification.",
        "application_url": "https://scholarships.gov.in",
        "helpline": "0120-6619540",
        "keywords": ["scholarship", "student", "college", "school", "education", "fees", "chhatravritti", "sc", "st", "obc", "minority", "post matric"]
    },
    {
        "id": 10,
        "title": "e-Shram Portal (Unorganised Workers Welfare)",
        "title_hi": "ई-श्रम पोर्टल",
        "department": "Ministry of Labour & Employment",
        "category": "Employment & Social Welfare",
        "level": "Central",
        "state": "All India",
        "benefits": "Universal Account Number (UAN) card, ₹2,00,000 accidental death/permanent disability cover under PMSBY, and direct social security benefits during crises.",
        "eligibility_criteria": "Any unorganised worker between 16 to 59 years (e.g., construction workers, domestic workers, gig workers, rickshaw pullers, agricultural labourers). Not paying income tax and not an EPFO/ESIC member.",
        "required_documents": "Aadhaar Card linked with Mobile Number, Active Bank Account Details.",
        "application_process": "1. Visit eshram.gov.in -> 'Register on e-Shram'. 2. Complete Aadhaar OTP verification. 3. Fill occupation & skill details. 4. Download UAN e-Shram Card.",
        "application_url": "https://eshram.gov.in",
        "helpline": "14434",
        "keywords": ["eshram", "shramik", "labour", "worker", "unorganised", "construction", "driver", "domestic", "uan card", "majdoor"]
    }
]


class RAGService:
    """
    RAG Service for searching, filtering, and assembling Indian Government Scheme knowledge
    to enrich AI chatbot responses with accurate, verifiable civic information.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def search_schemes(
        self,
        query: str,
        demographics: Optional[UserDemographics] = None,
        category: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieves matching schemes from database or curated knowledge base using
        keyword relevance, demographic profiling, and category matching.
        """
        results: List[Dict[str, Any]] = []
        normalized_query = query.lower()
        query_words = set(re.findall(r'\w+', normalized_query))

        # 1. Fetch active schemes from DB if available
        db_schemes: List[Dict[str, Any]] = []
        if self.db:
            try:
                db_query = self.db.query(Service).filter(Service.is_active == True)
                if category:
                    db_query = db_query.filter(Service.category.ilike(f"%{category}%"))
                if state and state.lower() != "all india":
                    db_query = db_query.filter(
                        (Service.state == state) | (Service.state == "All India") | (Service.level == "Central")
                    )

                items = db_query.all()
                for s in items:
                    db_schemes.append({
                        "id": s.id,
                        "title": s.title,
                        "title_hi": s.title_hi,
                        "department": s.department,
                        "category": s.category,
                        "level": s.level,
                        "state": s.state or "All India",
                        "benefits": s.benefits or s.short_description,
                        "eligibility_criteria": s.eligibility_criteria or "",
                        "required_documents": s.required_documents or "",
                        "application_process": s.application_process or "",
                        "application_url": s.application_url or "",
                        "helpline": s.helpline or "",
                        "keywords": [w.lower() for w in re.findall(r'\w+', f"{s.title} {s.category} {s.department} {s.benefits or ''}")]
                    })
            except Exception:
                db_schemes = []

        pool = db_schemes if db_schemes else INDIAN_SCHEMES_KNOWLEDGE

        # 2. Score each scheme against query and citizen demographic profile
        for item in pool:
            score = 0.0
            search_text = f"{item.get('title', '')} {item.get('title_hi', '')} {item.get('category', '')} {item.get('department', '')} {item.get('benefits', '')} {item.get('eligibility_criteria', '')}".lower()
            keywords = [k.lower() for k in item.get("keywords", [])]

            # Direct keyword hits
            for kw in keywords:
                if kw in normalized_query:
                    score += 4.0
            
            # Word token overlap
            for qw in query_words:
                if len(qw) > 2 and qw in search_text:
                    score += 1.5

            # Exact title substring match
            if item.get("title", "").lower() in normalized_query:
                score += 8.0

            # Demographic boosts
            if demographics:
                # Occupation matching
                if demographics.occupation:
                    occ = demographics.occupation.lower()
                    if ("farmer" in occ or "kisan" in occ) and item.get("category") == "Agriculture":
                        score += 3.5
                    elif ("student" in occ) and item.get("category") == "Education":
                        score += 3.5
                    elif ("business" in occ or "shop" in occ or "self" in occ) and "Business" in item.get("category", ""):
                        score += 3.5
                    elif ("artisan" in occ or "carpenter" in occ or "tailor" in occ) and "Vishwakarma" in item.get("title", ""):
                        score += 5.0
                    elif ("vendor" in occ or "hawker" in occ) and "SVANidhi" in item.get("title", ""):
                        score += 5.0
                    elif ("labour" in occ or "worker" in occ) and "e-Shram" in item.get("title", ""):
                        score += 4.0

                # Age matching
                if demographics.age is not None:
                    if demographics.age >= 60 and ("Old Age" in item.get("title", "") or "Atal Pension" in item.get("title", "") or "Ayushman" in item.get("title", "")):
                        score += 3.0
                    elif demographics.age <= 10 and "Sukanya" in item.get("title", ""):
                        score += 3.0

                # Gender matching
                if demographics.gender and demographics.gender.lower() in ["female", "woman", "girl"]:
                    if "Sukanya" in item.get("title", "") or "Women" in item.get("category", ""):
                        score += 3.0

                # Income matching (low income / EWS benefits)
                if demographics.annual_income is not None and demographics.annual_income <= 300000:
                    if item.get("category") in ["Housing", "Healthcare", "Social Welfare", "Education"]:
                        score += 2.0

            if score > 0 or not query_words:
                scored_item = dict(item)
                scored_item["score"] = score
                results.append(scored_item)

        # Sort by relevance score
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results[:limit]

    def build_rag_prompt_context(self, schemes: List[Dict[str, Any]]) -> str:
        """
        Builds clear markdown context of retrieved schemes for LLM system prompt.
        """
        if not schemes:
            return "No specific scheme documents were matched in the database."

        context_sections = []
        for i, s in enumerate(schemes, 1):
            sec = (
                f"### Scheme [{i}]: {s.get('title')} ({s.get('title_hi', '')})\n"
                f"- **Department**: {s.get('department')}\n"
                f"- **Category**: {s.get('category')} | **Level**: {s.get('level', 'Central')}\n"
                f"- **Benefits**: {s.get('benefits')}\n"
                f"- **Eligibility**: {s.get('eligibility_criteria')}\n"
                f"- **Required Documents**: {s.get('required_documents')}\n"
                f"- **Application Process**: {s.get('application_process')}\n"
                f"- **Official Portal**: {s.get('application_url')}\n"
                f"- **Helpline**: {s.get('helpline', 'N/A')}"
            )
            context_sections.append(sec)

        return "\n\n".join(context_sections)

    def extract_cards_and_sources(
        self, schemes: List[Dict[str, Any]]
    ) -> tuple[List[SchemeCard], List[SourceDocument]]:
        """
        Formats raw scheme dictionaries into API response cards and citations.
        """
        cards: List[SchemeCard] = []
        sources: List[SourceDocument] = []

        for s in schemes:
            cards.append(
                SchemeCard(
                    id=s.get("id"),
                    title=s.get("title", ""),
                    title_hi=s.get("title_hi"),
                    department=s.get("department"),
                    category=s.get("category"),
                    level=s.get("level", "Central"),
                    state=s.get("state"),
                    benefits=s.get("benefits"),
                    eligibility_summary=s.get("eligibility_criteria"),
                    application_url=s.get("application_url"),
                    helpline=s.get("helpline"),
                    match_score=round(s.get("score", 1.0), 2)
                )
            )

            sources.append(
                SourceDocument(
                    title=s.get("title", ""),
                    url=s.get("application_url"),
                    snippet=f"{s.get('department', '')} | Benefits: {s.get('benefits', '')[:120]}...",
                    relevance_score=round(s.get("score", 1.0), 2)
                )
            )

        return cards, sources