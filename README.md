# Library Management System (Python)

## Overview

This project is a fully object-oriented Library Management System developed in Python. It enables users to manage books, perform advanced searches, compare sorting algorithms, and maintain persistent storage using CSV files.

The system demonstrates practical implementation of data structures, classical algorithms, recursion, and software design principles within a modular architecture.

---

## Key Features

### Book Management
- Add, update, and remove books from inventory  
- Track lending and return history  
- Manage multiple book copies with automatic availability updates  
- Persistent data storage using CSV files  

### Advanced Search Capabilities
- Recursive search by title  
- Custom binary search combining rating and publication year criteria  
- Truth-table based filtering (genre, student-friendly criteria, borrowing type)  

### Sorting and Algorithm Implementation
- Bubble Sort (by rating)  
- Merge Sort (by title and publication year)  
- Strategy Design Pattern for flexible sorting selection  
- Performance benchmarking to compare sorting efficiency  

### Data Persistence
- CSV-based storage system  
- Automatic loading and saving of data  
- Data handling using pandas  

### Software Design Principles Applied
- Object-Oriented Programming (OOP)  
- Abstract Base Classes (ABC)  
- Strategy Pattern  
- Encapsulation and modular separation (Inventory, Analytics, UI)  
- Input validation and structured error handling  

---

## Technologies Used

- Python 3  
- pandas  
- datetime  
- abc (Abstract Base Classes)  
- Object-Oriented Design Principles  

---

## Project Structure

- `Book` – Represents individual book entities  
- `BookInventory` – Handles storage and database operations  
- `BookAnalytics` – Manages sorting and performance comparison  
- `BookUI` – Handles user interaction and system flow  
- Sorting strategies – Bubble Sort and Merge Sort implementations  

---

## How to Run

1. Install Python 3  
2. Install required dependency:

```bash
pip install pandas
```

3. Run the program:

```bash
python library_management_system.py
```

---

## Learning Outcomes

This project demonstrates:

- Implementation of classical sorting algorithms (Bubble Sort and Merge Sort)  
- Custom binary search logic with multiple evaluation criteria  
- Recursive search implementation  
- Application of software design patterns  
- Modular system architecture  
- Performance comparison and benchmarking  
- File-based data persistence  
