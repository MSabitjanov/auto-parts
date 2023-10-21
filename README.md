# auto-parts
Backend for a e-commerce website, which sells auto parts and provides the services

# Auto Parts

## How to Run the Project Locally

To run this project on your local machine, follow these steps:

1. Clone the repository to your local machine. (clone from locale branch, since it use dbsqlite, no need to configure postgres)

2. Navigate to the project directory.

   ``` cd auto-parts```

4. Create a virtual environment and activate it.

     ``` python3 -m venv myenv ```
5. Activate it
  for ubuntu:
  ``` source myenv/bin/activate ```
  for windows:
  ``` myenv\Scripts\activate ```

7. Install the required dependencies.

    ``` pip install -r requirements.txt ```

9. Create a `.env` file in the root directory of the project and copy the content from `.env.example` file.

10. Update the necessary configurations in the `.env` file.

11. Go to project directory

    ``` cd auto-parts/ ```
    ex: ``` D:\PROJECTS\auto-parts\auto-parts ```

12. Run the migrations.

    ``` python manage.py migrate ```

13. Start the development server.

    ``` python manage.py runserver ```

14. Open your web browser and visit `http://127.0.0.1:8000` to see the project.




