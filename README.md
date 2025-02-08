# Stock Management System

This is a desktop application for managing stock items. Built with Python, Tkinter, and MySQL, the application allows you to perform full CRUD (Create, Read, Update, Delete) operations, generate random stock item IDs, and export data to CSV.

## Features

- **CRUD Operations:**  
  Create, update, delete, and view stock items stored in a MySQL database.

- **Random ID Generation:**  
  Generate a valid stock item ID in the format `XXXXX~X` (five digits followed by a tilde and one uppercase letter).

- **CSV Export:**  
  Export stock data to a CSV file with a timestamped filename.

- **User-Friendly GUI:**  
  A simple and clean user interface built with Tkinter using frames, labels, entries, buttons, and a Treeview for displaying data.

## Technologies Used

- **Python 3.x**
- **Tkinter** for the GUI
- **pymysql** for MySQL database connectivity
- **MySQL** for data storage
- **csv** and **datetime** for CSV export functionality

## Prerequisites

- **Python 3.x** must be installed on your system.
- **MySQL** server must be installed and running.
- Install the required Python package by running:

  ```bash
  pip install pymysql
