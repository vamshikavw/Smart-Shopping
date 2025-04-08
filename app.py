from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

# --- Agents ---
class CustomerAgent:
    def __init__(self, customer_id):
        self.customer_id = customer_id.strip()  # Remove any extra spaces

    def get_customer_data(self):
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id=?", (self.customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return customer

class ProductAgent:
    def get_product_recommendations(self, customer_segment):
        conn = sqlite3.connect("ecommerce.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE category = ?", (customer_segment,))
        products = cursor.fetchall()
        conn.close()
        return products

# --- HTML Template ---
home_html = '''
<!DOCTYPE html>
<html>
<head><title>Smart Shopping</title></head>
<body>
    <h2>🎉 Welcome to the Smart Shopping Flask App!</h2>
    <form action="/recommend" method="get">
        <label>Enter Customer ID:</label>
        <input type="text" name="customer_id" required>
        <input type="submit" value="Get Recommendations">
    </form>
</body>
</html>
'''

@app.route('/')
def home():
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM customers")
    ids = cursor.fetchall()
    conn.close()

    print("Available IDs:", ids)  # Debug print

    return render_template_string(home_html)

@app.route('/recommend')
def recommend():
    customer_id = request.args.get('customer_id')

    if not customer_id:
        return "Please provide a customer ID."

    # 🔍 Get customer data
    agent = CustomerAgent(customer_id)
    customer_data = agent.get_customer_data()

    if not customer_data:
        return f"No customer found with ID '{customer_id}'."

    # 🔍 Simulate a segment (you can replace this with your ML segment logic)
    segment = "Electronics"  # Placeholder

    # 🛍 Get product recommendations
    product_agent = ProductAgent()
    products = product_agent.get_product_recommendations(segment)

    # 🖼️ HTML to display
    result_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Recommendations</title>
    </head>
    <body>
        <h2>🧑‍💼 Customer ID: {{ customer_id }}</h2>
        <h3>🛍️ Recommended Products:</h3>
        <table border="1" cellpadding="5">
            <tr>
                <th>Product ID</th>
                <th>Category</th>
                <th>Type</th>
                <th>Price</th>
                <th>Brand</th>
            </tr>
            {% for product in products %}
            <tr>
                <td>{{ product[0] }}</td>
                <td>{{ product[1] }}</td>
                <td>{{ product[2] }}</td>
                <td>{{ product[3] }}</td>
                <td>{{ product[4] }}</td>
            </tr>
            {% endfor %}
        </table>
        <br><a href="/">🔙 Go Back</a>
    </body>
    </html>
    '''

    return render_template_string(result_html, customer_id=customer_id, products=products)

if __name__ == '__main__':
    app.run(debug=True)
