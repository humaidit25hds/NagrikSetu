from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.chat import UserDemographics, EligibilityResult, EligibilityCriteriaItem, SchemeCard
from app.services.rag import INDIAN_SCHEMES_KNOWLEDGE


def check_eligibility(
    user_data: Dict[str, Any],
    scheme: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Check whether a user is eligible for a government scheme.

    user_data example:
    {
        "age": 25,
        "gender": "female",
        "income": 150000,
        "state": "Maharashtra",
        "occupation": "student"
    }

    scheme example:
    {
        "name": "Student Scholarship",
        "min_age": 18,
        "max_age": 30,
        "max_income": 250000,
        "gender": "all",
        "states": ["Maharashtra", "Gujarat"]
    }
    """

    reasons: List[str] = []
    eligible = True

    # -------------------------
    # Age Check
    # -------------------------

    age = user_data.get("age")

    if age is not None:

        min_age = scheme.get("min_age")
        max_age = scheme.get("max_age")

        if min_age is not None and age < min_age:
            eligible = False
            reasons.append(
                f"Minimum age required is {min_age} years."
            )

        if max_age is not None and age > max_age:
            eligible = False
            reasons.append(
                f"Maximum age allowed is {max_age} years."
            )

    # -------------------------
    # Income Check
    # -------------------------

    income = user_data.get("income")

    if income is not None:

        min_income = scheme.get("min_income")
        max_income = scheme.get("max_income")

        if min_income is not None and income < min_income:
            eligible = False
            reasons.append(
                f"Minimum annual income required is ₹{min_income}."
            )

        if max_income is not None and income > max_income:
            eligible = False
            reasons.append(
                f"Maximum annual income allowed is ₹{max_income}."
            )

    # -------------------------
    # Gender Check
    # -------------------------

    user_gender = user_data.get("gender")
    scheme_gender = scheme.get("gender", "all")

    if (
        user_gender
        and scheme_gender != "all"
        and user_gender.lower() != scheme_gender.lower()
    ):
        eligible = False
        reasons.append(
            f"This scheme is available for {scheme_gender} applicants."
        )

    # -------------------------
    # State Check
    # -------------------------

    user_state = user_data.get("state")
    allowed_states = scheme.get("states")

    if user_state and allowed_states:

        normalized_states = [
            state.lower() for state in allowed_states
        ]

        if user_state.lower() not in normalized_states:
            eligible = False
            reasons.append(
                f"This scheme is not currently available in {user_state}."
            )

    # -------------------------
    # Occupation Check
    # -------------------------

    user_occupation = user_data.get("occupation")
    allowed_occupations = scheme.get("occupations")

    if user_occupation and allowed_occupations:

        normalized_occupations = [
            occupation.lower()
            for occupation in allowed_occupations
        ]

        if user_occupation.lower() not in normalized_occupations:
            eligible = False
            reasons.append(
                f"The scheme is available only for "
                f"{', '.join(allowed_occupations)}."
            )

    # -------------------------
    # Result
    # -------------------------

    if eligible:
        message = "The applicant appears to be eligible for this scheme."
    else:
        message = "The applicant does not meet all eligibility criteria."

    return {
        "eligible": eligible,
        "message": message,
        "reasons": reasons
    }


class EligibilityService:
    """
    Service for evaluating citizen eligibility against government schemes
    based on demographic profile and scheme requirements.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def evaluate(
        self,
        scheme_id: Optional[int] = None,
        scheme_name: Optional[str] = None,
        demographics: UserDemographics = None
    ) -> EligibilityResult:
        """
        Evaluates a citizen's eligibility for a specific scheme.
        Returns detailed result with matched/unmet criteria and next steps.
        """
        if not demographics:
            return EligibilityResult(
                scheme_title=scheme_name or f"Scheme #{scheme_id}",
                status="NEED_MORE_INFO",
                match_score_percent=0,
                matched_criteria=[],
                unmet_criteria=[
                    EligibilityCriteriaItem(
                        criterion="Citizen Profile",
                        met=False,
                        reason="Please provide demographic information for eligibility assessment."
                    )
                ],
                next_steps=["Please share your age, income, state, and occupation to get personalized eligibility."],
                application_url=None
            )

        # Find scheme
        scheme = self._get_scheme(scheme_id, scheme_name)
        if not scheme:
            return EligibilityResult(
                scheme_title=scheme_name or f"Scheme #{scheme_id}",
                status="INELIGIBLE",
                match_score_percent=0,
                matched_criteria=[],
                unmet_criteria=[
                    EligibilityCriteriaItem(
                        criterion="Scheme Details",
                        met=False,
                        reason="Scheme not found in knowledge base."
                    )
                ]
            )

        # Evaluate eligibility
        matched = []
        unmet = []
        match_count = 0
        total_criteria = 0

        # Check each eligibility criterion
        criteria_checks = self._evaluate_criteria(demographics, scheme)
        for criterion, is_met, reason in criteria_checks:
            total_criteria += 1
            if is_met:
                matched.append(EligibilityCriteriaItem(criterion=criterion, met=True, reason=reason))
                match_count += 1
            else:
                unmet.append(EligibilityCriteriaItem(criterion=criterion, met=False, reason=reason))

        # Determine overall status
        if not unmet:
            status = "ELIGIBLE"
        elif match_count >= total_criteria * 0.7:
            status = "LIKELY_ELIGIBLE"
        else:
            status = "INELIGIBLE"

        match_score = int((match_count / max(total_criteria, 1)) * 100)

        # Generate next steps
        next_steps = self._generate_next_steps(status, unmet, scheme)

        return EligibilityResult(
            scheme_id=scheme.get("id"),
            scheme_title=scheme.get("title", scheme_name or "Unknown Scheme"),
            status=status,
            match_score_percent=match_score,
            matched_criteria=matched,
            unmet_criteria=unmet,
            required_documents=self._extract_documents(scheme),
            next_steps=next_steps,
            application_url=scheme.get("application_url")
        )

    def get_eligible_schemes(
        self,
        user_profile: UserDemographics,
        limit: int = 5
    ) -> List[SchemeCard]:
        """
        Finds and returns schemes a user is likely eligible for based on profile.
        """
        from app.services.rag import RAGService
        
        rag_service = RAGService(db=self.db)
        
        # Create search query from demographics
        query_parts = []
        if user_profile.occupation:
            query_parts.append(user_profile.occupation)
        if user_profile.age is not None:
            if user_profile.age <= 10:
                query_parts.append("girl child education")
            elif user_profile.age >= 60:
                query_parts.append("old age pension")
        if user_profile.gender and user_profile.gender.lower() == "female":
            query_parts.append("women schemes")
        if user_profile.annual_income is not None and user_profile.annual_income <= 300000:
            query_parts.append("low income welfare")

        query = " ".join(query_parts) if query_parts else "government schemes"

        # Retrieve schemes
        schemes = rag_service.search_schemes(
            query=query,
            demographics=user_profile,
            state=user_profile.state,
            limit=limit
        )

        # Convert to SchemeCards
        cards = []
        for s in schemes:
            cards.append(
                SchemeCard(
                    id=s.get("id"),
                    title=s.get("title"),
                    title_hi=s.get("title_hi"),
                    department=s.get("department"),
                    category=s.get("category"),
                    level=s.get("level", "Central"),
                    state=s.get("state"),
                    benefits=s.get("benefits"),
                    eligibility_summary=s.get("eligibility_criteria"),
                    application_url=s.get("application_url"),
                    helpline=s.get("helpline"),
                    match_score=round(s.get("score", 0), 2)
                )
            )

        return cards

    def _get_scheme(self, scheme_id: Optional[int], scheme_name: Optional[str]) -> Optional[Dict[str, Any]]:
        """Retrieve scheme from DB or knowledge base."""
        # Try DB first
        if self.db and scheme_id:
            try:
                service = self.db.query(Service).filter(Service.id == scheme_id).first()
                if service:
                    return {
                        "id": service.id,
                        "title": service.title,
                        "title_hi": service.title_hi,
                        "department": service.department,
                        "category": service.category,
                        "eligibility_criteria": service.eligibility_criteria,
                        "required_documents": service.required_documents,
                        "application_url": service.application_url,
                        "benefits": service.benefits
                    }
            except Exception:
                pass

        # Fall back to knowledge base
        if scheme_id:
            for s in INDIAN_SCHEMES_KNOWLEDGE:
                if s.get("id") == scheme_id:
                    return s
        
        if scheme_name:
            scheme_name_lower = scheme_name.lower()
            for s in INDIAN_SCHEMES_KNOWLEDGE:
                if scheme_name_lower in s.get("title", "").lower() or scheme_name_lower in s.get("title_hi", "").lower():
                    return s

        return None

    def _evaluate_criteria(
        self,
        demographics: UserDemographics,
        scheme: Dict[str, Any]
    ) -> List[tuple[str, bool, str]]:
        """Evaluate each eligibility criterion."""
        criteria = []

        # Age criterion
        age = demographics.age
        if age is not None:
            criteria.append((
                "Age",
                age >= 18 if age else False,
                f"Age {age} years" if age else "Age not provided"
            ))

        # Income criterion
        income = demographics.annual_income
        if income is not None:
            is_eligible = income <= 1000000  # Generally for most schemes
            criteria.append((
                "Income Limit",
                is_eligible,
                f"Annual income ₹{income}" if income else "Income not provided"
            ))

        # Category/Caste criterion
        category = demographics.category
        if category:
            criteria.append((
                "Category/Caste",
                True,
                f"Category: {category}"
            ))

        # State criterion
        state = demographics.state
        if state:
            scheme_states = scheme.get("state", "All India")
            is_eligible = "All India" in scheme_states or state in scheme_states
            criteria.append((
                "State Availability",
                is_eligible,
                f"Applicable in {state}" if is_eligible else f"Not available in {state}"
            ))

        # Occupation match
        occupation = demographics.occupation
        if occupation:
            criteria.append((
                "Occupation/Type",
                True,
                f"Occupation: {occupation}"
            ))

        # Differently abled status
        if demographics.is_differently_abled and demographics.is_differently_abled.lower() == "yes":
            criteria.append((
                "Differently Abled",
                True,
                "Person with disability - may qualify for special schemes"
            ))

        return criteria

    def _extract_documents(self, scheme: Dict[str, Any]) -> List[str]:
        """Extract required documents from scheme details."""
        doc_text = scheme.get("required_documents", "")
        if not doc_text:
            return ["Aadhaar Card", "Proof of Residence", "Bank Account Details"]
        
        # Simple parsing of comma-separated documents
        docs = [d.strip() for d in doc_text.split(",")]
        return docs[:5]  # Limit to 5

    def _generate_next_steps(
        self,
        status: str,
        unmet: List[EligibilityCriteriaItem],
        scheme: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable next steps based on eligibility status."""
        steps = []

        if status == "ELIGIBLE":
            steps.append(f"You are eligible! Visit {scheme.get('application_url', 'the official portal')} to apply.")
            steps.append("Prepare all required documents before applying.")
            steps.append("Call helpline for any clarifications.")
        elif status == "LIKELY_ELIGIBLE":
            steps.append("You likely meet most criteria. Review the unmet criteria above.")
            if unmet:
                steps.append(f"Address: {unmet[0].reason}")
            steps.append(f"Visit {scheme.get('application_url', 'the official portal')} for detailed guidelines.")
        else:  # INELIGIBLE
            steps.append("Unfortunately, you don't appear to meet the current eligibility criteria.")
            if unmet:
                steps.append(f"Review issue: {unmet[0].reason}")
            steps.append("Check if there are other schemes you might be eligible for.")
            steps.append("Contact the helpline for alternate options.")

        return steps


def get_missing_information(
    user_data: Dict[str, Any],
    required_fields: List[str]
) -> List[str]:
    """
    Find information that is required but missing.
    """

    missing_fields = []

    for field in required_fields:

        value = user_data.get(field)

        if value is None or value == "":
            missing_fields.append(field)

    return missing_fields
