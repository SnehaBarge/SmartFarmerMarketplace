# Smart Farmer Marketplace

A Streamlit web application that provides a marketplace for farmers to list and rent out their tools and sell their crops. The application also features AI-powered recommendations using the Google Gemini API.

## About the Project

This project is a prototype for a smart marketplace that aims to connect farmers and empower them with data-driven insights. It is built with Python and Streamlit, and it uses a SQLite database to store the data.

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

You will need to have Python and pip installed on your system.

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/your_username_/SmartFarmerMarketplace.git
    ```
2.  Install the required packages
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a `.env` file in the root of the project.
2.  Add your Google Gemini API key to the `.env` file:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

## Usage

To run the application, use the following command:

```sh
streamlit run app.py
```

## Database

The application uses a SQLite database named `farmermarket.db`. The database has the following tables:

-   **tools**: Stores information about the tools available for rent.
    -   `Farmer` (TEXT)
    -   `Location` (TEXT)
    -   `Tool` (TEXT)
    -   `Rate` (REAL)
    -   `Contact` (TEXT)
    -   `Notes` (TEXT)
-   **crops**: Stores information about the crops available for sale.
    -   `Farmer` (TEXT)
    -   `Location` (TEXT)
    -   `Crop` (TEXT)
    -   `Quantity` (TEXT)
    -   `Expected_Price` (REAL)
    -   `Contact` (TEXT)
    -   `Listing_Date` (TEXT)
-   **farmers**: Stores information about the farmers.
    -   `name` (TEXT)
    -   `location` (TEXT)
    -   `farm_size` (REAL)
    -   `farm_unit` (TEXT)
    -   `contact` (TEXT)

## Features

-   **User Roles:** The application has two user roles: "Farmer" and "Admin".
-   **Farmer View:** Farmers can log in, add new tool and crop listings, and view all listings.
-   **Admin View:** Admins can do everything a farmer can do, plus they can view the database tables and add new farmer profiles.
-   **AI Recommendations:** The application provides AI-powered recommendations to farmers when they add a new listing.
-   **Profile Integration:** The application pre-fills the listing forms with the farmer's information if they have a profile in the database.
