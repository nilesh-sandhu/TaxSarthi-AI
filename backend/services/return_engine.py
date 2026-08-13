def get_returns(registration_type: str):

    registration_type = registration_type.lower()

    if registration_type == "regular":

        return {
            "registration_type": "Regular",

            "returns": [

                {
                    "return_name": "GSTR-1",
                    "frequency": "Monthly / Quarterly",
                    "due_date": "11th of next month",
                    "late_fee": "₹50/day"
                },

                {
                    "return_name": "GSTR-3B",
                    "frequency": "Monthly",
                    "due_date": "20th of next month",
                    "late_fee": "₹50/day"
                },

                {
                    "return_name": "GSTR-9",
                    "frequency": "Yearly",
                    "due_date": "31 December",
                    "late_fee": "As per GST Rules"
                }

            ],

            "recommendation":
            "File GSTR-1 before GSTR-3B every month."
        }

    elif registration_type == "composition":

        return {

            "registration_type": "Composition",

            "returns": [

                {
                    "return_name": "CMP-08",
                    "frequency": "Quarterly",
                    "due_date": "18th of next month",
                    "late_fee": "₹50/day"
                },

                {
                    "return_name": "GSTR-4",
                    "frequency": "Yearly",
                    "due_date": "30 April",
                    "late_fee": "As per GST Rules"
                }

            ],

            "recommendation":
            "File CMP-08 every quarter and GSTR-4 annually."
        }

    else:

        return {

            "registration_type": registration_type,

            "returns": [],

            "recommendation":
            "Registration type not recognized."
        }
    