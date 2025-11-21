# src/brand_config.py
# Master configuration for all supported brands

BRANDS = {
    "phonepe": {
        "official_names": ["PhonePe"],
        "official_publisher": "PhonePe Pvt Ltd",
        "keywords_suspicious": ["update", "pro", "secure", "latest", "cashback", "reward"],
        "aliases": ["phone pay", "fonepe", "phone-pe", "phonepe app"]
    },

    "paytm": {
        "official_names": ["Paytm"],
        "official_publisher": "One97 Communications Ltd",
        "keywords_suspicious": ["update", "cashback", "guide", "earn", "wallet", "helper"],
        "aliases": ["pay tm", "paytym", "paytmm", "paytm app"]
    },

    "gpay": {
        "official_names": ["Google Pay", "GPay"],
        "official_publisher": "Google LLC",
        "keywords_suspicious": ["reward", "lite", "update", "mod", "plus"],
        "aliases": ["g pay", "g-pay", "googlepay", "google pay india"]
    }
}
