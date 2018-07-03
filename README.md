# Location Filter for InYourArea.co.uk

Simple machine learning powered filter for location tags on articles 
displayed on the inyourarea.co.uk platform.

Notebooks for modelling details and exploration are available in 
[notebooks](./notebooks).

The scraper used to collect input data is in [article_scraper](./article_scraper)

A Flask [app](./app.py) provide a REST api to the filters prediction.

Once data are collected, to refit the models, run [main.py](./main.py)

### API

* POST /location-filters/predictions
    
    predict the relevancy of a location tag for a given article.
    The publisher of this article must be amongst the available publishers.
    
    example request: 
    ```json 
    {
	    "article_id": "4bc46aab-aee3-408f-9b93-3973bdad5816",
	    "location_ids": [
		        "2e1d9ff5-cbde-4eae-a311-ec4def1ec76e",
		        "fbe7bb85-5ee9-4172-955c-ec2f9b9ac3b4"
	    ]
    }
    
    
    ```
    example response:
    ```
    {
        "article_id": "4bc46aab-aee3-408f-9b93-3973bdad5816",
        "predictions": [
            {
                "confidence": 0.13035546997650807,
                "id": "2e1d9ff5-cbde-4eae-a311-ec4def1ec76e",
                "name": "Finsbury Park",
                "relevant": false
            },
            {
                "confidence": 0.9641445963269318,
                "id": "fbe7bb85-5ee9-4172-955c-ec2f9b9ac3b4",
                "name": "Birmingham",
                "relevant": true
            }
        ],
        "publisher": "birminghammail",
        "title": "Can you answer these extremely difficult pub quiz questions? Find out if you're a true champion here"
    }
    ```
        
    
    
* GET /location-filters/models
    
    Lists the models available on the API.