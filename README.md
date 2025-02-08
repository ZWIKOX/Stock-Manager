# Stock Management System

A simple stock management system built with Python, Tkinter, and MySQL. This application provides a modern, tabbed user interface for managing stock records with full CRUD (Create, Read, Update, Delete) functionality and CSV export support.

## Features

- **CRUD Operations:** Create, read, update, and delete stock records.
- **Random ID Generation:** Automatically generate valid stock item IDs in the format `XXXXX~X` (5 digits, a tilde, and 1 uppercase letter).
- **Tabbed Interface:** Manage stock details and view the stock list on separate tabs.
- **Menu Bar:** Includes options for exporting data to CSV and exiting the application.
- **CSV Export:** Export all stock records to a CSV file with a timestamped filename.

## Technologies Used

- **Python 3.x**
- **Tkinter** & **ttk** for building the GUI.
- **PyMySQL** for MySQL database connectivity.
- **MySQL** as the backend database.
- **csv** module for data export.
- **datetime** for managing timestamps.

### Prerequisites

- **Python 3.x** must be installed on your system.
- **MySQL** server must be installed and running.
- Install the required Python package using pip:

  ```bash
  pip install pymysql
