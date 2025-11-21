# src/brand_config.py
# Master configuration for all supported brands (FINAL UPDATED VERSION)

BRANDS = {
    "phonepe": {
        "official_names": [
            "PhonePe",
            "PhonePe Business",
            "PhonePe Lite",
            "PhonePe Merchant"
        ],
        "official_publisher": "PhonePe Pvt Ltd",

        # MUST be named "keywords"
        "keywords": [
            "update", "pro", "secure", "latest",
            "cashback", "reward", "guide", "helper"
        ],

        "aliases": [
            "phone pay", "fonepe", "phone-pe",
            "phonepe app", "phonpay", "phonepay"
        ]
    },

    "paytm": {
        "official_names": [
            "Paytm",
            "Paytm Lite",
            "Paytm for Business"
        ],
        "official_publisher": "One97 Communications Ltd",

        # MUST be named "keywords"
        "keywords": [
            "update", "reward", "cashback", "lite",
            "guide", "earn", "wallet", "helper"
        ],

        "aliases": [
            "pay tm", "paytym", "paytmm",
            "paytm app", "paytm official", "pytm"
        ]
    },

    "gpay": {
        "official_names": [
            "Google Pay",
            "GPay",
            "GPay India"
        ],
        "official_publisher": "Google LLC",

        # MUST be named "keywords"
        "keywords": [
            "reward", "cashback", "update",
            "lite", "mod", "plus", "new"
        ],

        "aliases": [
            "g pay", "googlepay", "google pay india",
            "g-pay", "gpay official"
        ]
    }
}

