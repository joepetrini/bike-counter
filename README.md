bike-counter
============

Web and mobile application to support the data collection and reporting for urban bike counting efforts.  

Built in conjunction with [Code for Philly](http://codeforphilly.org/projects/Philly_Bike_Coalition_Survey_App) and [Philly Bike Coalition](http://www.bicyclecoalition.org/).

## Requirements
* Python 2.7
* Pip


## Running the django web application

    # Clone the github repo
    git clone https://github.com/joepetrini/bike-counter.git bikecounts

    # Create a virutalenv using virtualenvwrapper
    # get https://virtualenvwrapper.readthedocs.org/en/latest/
    mkvirtualenv bikecounts
    cd webapp

    # Install project requirements
    pip install -r requirements.txt

    # Copy the local settings template
    # Update local.py with db settings, or leave as is for sqlite file
    cp bikecounter/settings/local_copyme.py bikecounter/settings/local.py

    # Run the database migration to update schema
    python manage.py migrate

    # Load initial data
    python manage.py loaddata init_data.json

    # Run it
    python manage.py runserver


## Running the mobile app

    cd mobilebapp/bikeapp/www
    sh server.sh

View it at http://localhost:1080
