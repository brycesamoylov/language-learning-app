SUPPORTED_LANGUAGES = {
    "el": {  # ISO 639-1 code for Greek
        "name": "Greek",
        "native_name": "Ελληνικά",
        "flag": "🇬🇷",
        "rtl": False,
        "levels": ["A1", "A2", "B1", "B2", "C1", "C2"],
        "initial_phrases": [
            {
                "text": "Γεια σας",
                "transliteration": "Yia sas",
                "translation": "Hello",
                "level": "A1",
                "category": "Greetings"
            },
            {
                "text": "Καλημέρα",
                "transliteration": "Kalimera",
                "translation": "Good morning",
                "level": "A1",
                "category": "Greetings"
            },
            {
                "text": "Πώς είστε;",
                "transliteration": "Pos iste?",
                "translation": "How are you?",
                "level": "A1",
                "category": "Greetings"
            },
            {
                "text": "Με λένε",
                "transliteration": "Me lene",
                "translation": "My name is",
                "level": "A1",
                "category": "Introductions"
            },
            {
                "text": "Ευχαριστώ",
                "transliteration": "Efharisto",
                "translation": "Thank you",
                "level": "A1",
                "category": "Common Phrases"
            }
        ],
        "initial_lessons": [
            {
                "title": "Greek Alphabet",
                "description": "Learn the Greek alphabet and pronunciation",
                "level": "A1",
                "category": "Fundamentals",
                "content": {
                    "alphabet": [
                        {"letter": "Α α", "name": "alpha", "pronunciation": "a"},
                        {"letter": "Β β", "name": "beta", "pronunciation": "v"},
                        {"letter": "Γ γ", "name": "gamma", "pronunciation": "gh/y"},
                        {"letter": "Δ δ", "name": "delta", "pronunciation": "th"},
                        {"letter": "Ε ε", "name": "epsilon", "pronunciation": "e"},
                        {"letter": "Ζ ζ", "name": "zeta", "pronunciation": "z"},
                        {"letter": "Η η", "name": "eta", "pronunciation": "i"},
                        {"letter": "Θ θ", "name": "theta", "pronunciation": "th"},
                        {"letter": "Ι ι", "name": "iota", "pronunciation": "i"},
                        {"letter": "Κ κ", "name": "kappa", "pronunciation": "k"},
                        {"letter": "Λ λ", "name": "lambda", "pronunciation": "l"},
                        {"letter": "Μ μ", "name": "mu", "pronunciation": "m"},
                        {"letter": "Ν ν", "name": "nu", "pronunciation": "n"},
                        {"letter": "Ξ ξ", "name": "xi", "pronunciation": "x"},
                        {"letter": "Ο ο", "name": "omicron", "pronunciation": "o"},
                        {"letter": "Π π", "name": "pi", "pronunciation": "p"},
                        {"letter": "Ρ ρ", "name": "rho", "pronunciation": "r"},
                        {"letter": "Σ σ/ς", "name": "sigma", "pronunciation": "s"},
                        {"letter": "Τ τ", "name": "tau", "pronunciation": "t"},
                        {"letter": "Υ υ", "name": "upsilon", "pronunciation": "i/y"},
                        {"letter": "Φ φ", "name": "phi", "pronunciation": "f"},
                        {"letter": "Χ χ", "name": "chi", "pronunciation": "ch/h"},
                        {"letter": "Ψ ψ", "name": "psi", "pronunciation": "ps"},
                        {"letter": "Ω ω", "name": "omega", "pronunciation": "o"}
                    ]
                }
            },
            {
                "title": "Basic Greetings",
                "description": "Learn common Greek greetings",
                "level": "A1",
                "category": "Conversation",
                "content": {
                    "phrases": [
                        {
                            "greek": "Γεια σας",
                            "transliteration": "Yia sas",
                            "translation": "Hello (formal)",
                            "audio_url": "greetings/yia_sas.mp3"
                        },
                        {
                            "greek": "Γεια σου",
                            "transliteration": "Yia sou",
                            "translation": "Hello (informal)",
                            "audio_url": "greetings/yia_sou.mp3"
                        },
                        {
                            "greek": "Καλημέρα",
                            "transliteration": "Kalimera",
                            "translation": "Good morning",
                            "audio_url": "greetings/kalimera.mp3"
                        },
                        {
                            "greek": "Καλησπέρα",
                            "transliteration": "Kalispera",
                            "translation": "Good evening",
                            "audio_url": "greetings/kalispera.mp3"
                        }
                    ]
                }
            }
        ]
    }
}
