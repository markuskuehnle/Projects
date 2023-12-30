# ImmoScout24 Data Extraction Project

## Overview
This project presents a simplified and effective approach to extract real estate listing data from ImmoScout24, one of the leading real estate platforms. Recognizing the challenges posed by traditional scraping methods, which are often blocked by modern websites, this project employs Selenium, a powerful browser automation tool, to simulate real user interactions for data extraction. 

## Features
- **Browser Simulation**: Utilizes Selenium to simulate a real browser, enabling it to bypass most common scraping blocks.
- **Manual CAPTCHA Solving**: Includes a step for manual CAPTCHA solving, ensuring compliance with website access rules while still automating the bulk of the data extraction process.
- **Data Extraction**: Efficiently extracts vital information about real estate listings, such as title, address, rent (Kaltmiete), living space, and number of rooms.
- **SQLite Database Integration**: Seamlessly stores the extracted data in a SQLite database, providing a structured and convenient way to handle the data.
- **Unique Identifier Handling**: Each listing is identified by its unique `data_id`, ensuring no duplicate entries are stored.

## How It Works
Upon execution, the script:
1. Opens the target webpage in a simulated browser window.
2. Waits for the user to solve the CAPTCHA manually (if prompted).
3. Navigates through the webpage, accessing and extracting data from each real estate listing.
4. Stores the extracted data in a SQLite database, with checks in place to avoid duplicate entries.

## Limitations and Considerations
- **Manual Intervention for CAPTCHA**: User intervention is required for CAPTCHA solving.
- **Dependence on Website Structure**: The script is dependent on the current structure of the ImmoScout24 website. Any changes in the website layout may require corresponding updates in the script.
- **Compliance with Legal and Ethical Standards**: Users are responsible for using this script in compliance with ImmoScout24's terms of service and relevant legal regulations.

