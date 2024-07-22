
toy_response = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "JP101":{
                        "summary": "Transaction ID: 1502",
                        "value": {
                            "message": {
                                "toy_id": "JP101",
                                "owner_id": "super_mom492",
                                "coordinates": "18.458,77.235",
                                "name": "IntelliSkills Jungle Animals Stick Puzzle",
                                "description": "18-pc puzzles, 6 animals, suitable for 3+ kids",
                                "images": [],
                                "weight": "0.28kg",
                                "features": [],
                                "recommended_age": "3+",
                                "dimensions": "12X12X34",
                                "brand": "IntelliSkills",
                                "available": True,
                                "rating": 4.8,
                                "review_count": 1
                            }
                        }
                    }
                }
            }
        }
    },
    404: {
        "description": "Object Not Found",
        "content": {
            "application/json": {
                "examples": {
                    "JP109":{
                        "summary": "Not Found",
                        "value": {
                            "detail": "Toy JP109 not found"
                            
                        }
                    }
                }
            }
        }
        }
    }

