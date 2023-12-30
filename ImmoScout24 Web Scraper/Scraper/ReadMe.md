# ImmoScout24 Web Scraper

## Project Overview
Building upon the successful demonstration in the Jupyter Notebook, this modular version of the ImmoScout24 Web Scraper offers enhanced scalability, easier deployment, and greater flexibility. This project continues to employ Selenium for effective data extraction from ImmoScout24, but with the added benefits of a modular, script-based approach.

## Key Advantages over Jupyter Notebook
- **Script-based Approach**: Easier integration into larger systems or workflows and more straightforward scheduling for regular scraping tasks.
- **Enhanced Scalability**: Better suited for scaling up, allowing for more extensive data extraction and handling.
- **Simplified Deployment**: The modular nature simplifies deployment on various environments, including servers or cloud platforms.
- **Improved Performance**: Optimized for better performance and efficiency, especially for longer scraping sessions.

## Features
- **Automated Browser Simulation**: Harnesses Selenium to automate browser interactions, capable of handling complex web elements and dynamic content.
- **Advanced Data Extraction**: Extracts detailed listing information (title, address, rent, etc.) and stores it in a SQLite database.
- **Duplication Check**: Employs unique identifiers for each listing to prevent duplicate data entries.
- **Modular Design**: Facilitates easy updates and maintenance of individual components of the project.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.7 or higher
- Google Chrome or Chromium browser
- ChromeDriver compatible with your Chrome version

## Installation and Setup

1. **Clone the Repository:**
   ```
   git clone https://github.com/markuskuehnle/ImmoScout24-Web-Scraper.git
   cd ImmoScout24-Web-Scraper
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**
   ```
   python -m venv venv
   .\venv\Scripts\activate  # For Windows
   source venv/bin/activate  # For Unix or MacOS
   ```

3. **Install Required Packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Configuration:**
   - Modify `config.xml` to set your desired search parameters and log file path.

## Usage
To run the scraper, execute the following command:
```
python scraper.py
```
Follow the on-screen instructions to solve the CAPTCHA manually in the opened browser window.

## Project Structure
- `scraper.py`: Main script that coordinates the scraping process.
- `database.py`: Handles all database-related operations.
- `utils.py`: Contains utility functions for data processing and handling.
- `config.xml`: Configuration file to set search parameters and paths.

## Data Schema
The scraped data is stored in an SQLite database with the following schema:
- `data_id`: Unique identifier for each listing
- `title`: Title of the listing
- `address`: Address of the property
- `kaltmiete`: Cold rent price
- `living_space`: Living space in square meters
- `rooms`: Number of rooms
- `secondary_criteria`: Additional attributes of the listing
- `date`: Date of data extraction

## Limitations and Ethical Considerations
- Still requires manual CAPTCHA solving.
- Dependent on the structure of the ImmoScout24 website; subject to changes.
- Must be used in compliance with ImmoScout24's terms of service and relevant legal guidelines.