# RecycleUs - Hack to the Future Hackathon Project

## Project Overview

RecycleUs is a web application developed for the "Hack to the Future Hackathon". It aims to promote and simplify recycling habits by providing users with recycling guides, a recycling center locator, and personal recycling tracking features.

### Key Features

1. **Recycle Guide**: Comprehensive guides on how to recycle different materials.
2. **Recycle Tracker**: Personal recycling statistics and progress tracking.
3. **Recycle Center Locator**: Interactive map to find nearby recycling centers.
4. **Challenges & Achievements**: Gamified recycling goals and badges to encourage consistent recycling habits.

## Tech Stack

- **Frontend**: HTML, CSS, and minimal JavaScript
- **Backend**: Python with Flask
- **Database**: SQLite
- **APIs**: Google Maps API
- **Authentication**: Firebase

## Project Structure

- `/templates`: HTML templates for the web pages
- `/static`: 
  - `/css`: Stylesheets
  - `/js`: JavaScript files
- `app.py`: Main Flask application
- `database.py`: Database setup and migrations
- `firebase_config.py`: Firebase configuration and authentication functions
- `scheduled_tasks.py`: Background tasks for updating user streaks

## Setup and Installation

1. Clone the repository
2. Install required Python packages:
    ```
    pip install -r requirements.txt
    ```
3. Set up Firebase:
- Create a Firebase project
- Download the Firebase Admin SDK key and save it as `firebase_key.json` in the project root
- Update `firebase_config.py` with your Firebase project details
4. Set up Google Maps API:
- Obtain a Google Maps API key
- Create a `.env` file in the project root and add your API key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    FIREBASE_API_KEY=your_firebase_api_key_here
    ```
5. Initialize the database: 
    ```
    python database.py
    ```
6. Run the application:
    ```
    python app.py
    ```
## User Journey

1. Sign up and create a profile
2. Explore recycling guides
3. Use the map to find nearby recycling centers
4. Log recycling activities
5. Track habits, progress, and earn rewards

## Contributing

This project was developed as part of a hackathon. While it's not actively maintained, contributions, suggestions, and feedback are welcome. Please open an issue or submit a pull request if you'd like to contribute.

## Contributors

This project was developed by the team "We Can't Code" during the Hack to the Future Hackathon. The team members are:

- [cwnorhino](https://github.com/cwnorhino)
- [slyeet03](https://github.com/slyeet03)
- [rudracodess](https://github.com/rudracodess)
- [yashjswl](https://www.linkedin.com/in/yashjswl)

## Acknowledgements

- Hack to the Future Hackathon organizers
- Google Maps API
- Firebase
- All contributors and participants
