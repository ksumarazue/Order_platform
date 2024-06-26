# Order platform

This is a simple online ordering platform built using Flask, a lightweight web framework in Python, along with SQLite for the database.

## Features

- User registration and authentication
- Different user roles: admin, client, and employee
- Creating, viewing, updating, and deleting orders
- Order status tracking

## Project Structure
```
Order_platform-master/
│
├── controllers/
│ ├── order/
│ ├── product/
│ └── user/
│
├── instance/
│ └── models/
│ ├── order/
│ ├── product/
│ └── user/
│
├── static/
│
├── templates/
│
├── venv/
│
├── .gitignore
├── app.py
├── create_admin.py
├── README.md
└── requirements.txt
```

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ksumarazue/CodeMe_Fin_Project.git
    ```

2. Navigate to the project directory:
    ```sh
    cd Order_platform-master
    ```

3. Create virtual environment
   ```sh
   python -m venv venv
   ```
   
4. Activate virtual environment
   ```
   venv\Scripts\Activate
   ```
   
5. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

6. Before starting the application for the first time, you must create an admin account. To do this, first run:
    ```sh
    python create_admin.py
    ```
    This operation will create the user 'admin' with the password 'admin_password'.

7. Run the application:
    ```sh
    python app.py
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000/`.

2. You can log in with the admin account you created.

## Contributing

If you would like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Flask: [Flask Documentation](https://flask.palletsprojects.com/)
- SQLite: [SQLite Documentation](https://www.sqlite.org/docs.html)

## Contact

For any questions or comments, please contact the project maintainers.

## Placeholder Sections

- **Testing**: (Details about how to run tests)
- **API Documentation**: (Details about the API endpoints)