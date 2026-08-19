from typing import Dict, Any, List


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
