LEVELS = {
    "level0": {
        "criteria": 0,
        "screens": [
            "general1",
            "general2",
            "general3",
            "final",
        ],
        "file": "level0.csv"
    },
    "level1": {
        "criteria": 9,
        "screens": [
            "general1",
            "general2",
            "general3",
            "img1",
            "final",
        ],
        "file": "level1.csv"
    },
    "level2": {
        "criteria": 5,
        "screens": [
            "general1",
            "general2",
            "general3",
            "img2",
            "final",
        ],
        "file": "level2.csv"
    },
    "level3": {
        "criteria": 13,
        "screens": [
            "general1",
            "general2",
            "general3",
            "img1",
            "img2",
            "final",
        ],
        "file": "level3.csv"
    },
    "level4": {
        "criteria": 3,
        "screens": [
            "general1",
            "general2",
            "general3",
            "img3",
            "final",
        ],
        "file": "level4.csv"
    },
    "level5": {
        "criteria": 11,
        "screens": [
            "general1",
            "general2",
            "general3",
            "img3",
            "img1",
            "final",
        ],
        "file": "level5.csv"
    },
    "level6": {
        "criteria": 7,
        "screens": [
            "general1",
            "general2",
            "general3",
            "img3",
            "img2",
            "final",
        ],
        "file": "level6.csv"
    },
    "level7": {
        "criteria": 15,
        "screens": [
            "general1",
            "general2",
            "general3",
            "img1",
            "img2",
            "img3",
            "final",
        ],
        "file": "level7.csv"
    },
    "level8": {
        "criteria": 15,
        "screens": [
            "general1",
            "general2",
            "general3",
            "img1",
            "img2",
            "img3",
            "final",
        ],
        "file": "level8.csv"
    },

    # Niveles de prueba
    "sin_cuando": {
        "criteria": 14,
        "screens": [
            "general1",
            "general2",
            "general3",
            "final",
        ],
        "file": "test.csv",
    },
}

GROUPS = {
    "Aislado": [
        "level0",
        "level1",
        "level2",
        "level4",
        "level8",
    ],
    "Aditivo": [
        "level0",
        "level2",
        "level3",
        "level7",
        "level8",
    ],
    "Integral": [
        "level0",
        "level7",
        "level7",
        "level7",
        "level8",
    ]
}
