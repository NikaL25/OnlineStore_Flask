### Flask E-commerce Application

# Flask E-commerce Application is a simple web-based online store built using Python and the Flask framework.

It includes core e-commerce features such as:

product listings,

user registration and authentication,

shopping cart functionality,

and order placement.

How to Run the Project Locally:
1. Make sure you have Python 3.6 or higher installed.

2. Clone the repository:
git clone https://github.com/NikaL25/OnlineStore_Flask.git

3. Navigate into the project directory:
cd OnlineStore_Flask

4. Create a virtual environment:
python -m venv venv

5. Activate the virtual environment:

On Linux/macOS: source venv/bin/activate

On Windows: venv\Scripts\activate

6. Install the required dependencies:
pip install -r requirements.txt


7. Start the application:
python app.py runserver

8. The app will be accessible at:
http://127.0.0.1:5000

## Project Structure:
The project includes standard Flask directories and files such as:

templates/ — for HTML templates

static/ — for CSS and JavaScript files

app.py, models.py, forms.py, routes.py — core application files

## Customization:
You can customize and extend the application by using the built-in admin dashboard, which allows you to:

Manage products (add, edit, delete)

Organize products into categories

Handle user accounts and orders

Additionally, you can extend the app with features like:

Payment gateway integration

Further customization of the admin interface

Ensure that the database is properly initialized on the first run.
