import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Create and populate the SQLite database ---
try:
    # Connect to the database (this will create the file if it doesn't exist)
    conn = sqlite3.connect("sales_data.db")
    cursor = conn.cursor()

    # Create a 'sales' table
    # Using IF NOT EXISTS to prevent errors if the script is run multiple times
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')

    # Clear existing data to prevent duplicates on re-runs
    cursor.execute('DELETE FROM sales;')


    # Insert some sample data into the table
    sales_data = [
        ('Laptop', 10, 1200.00),
        ('Mouse', 50, 25.50),
        ('Keyboard', 30, 75.00),
        ('Monitor', 20, 300.75),
        ('Laptop', 5, 1150.00), # another laptop sale
        ('Mouse', 25, 24.00),   # another mouse sale
        ('Webcam', 15, 55.00)
    ]
    cursor.executemany('INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)', sales_data)

    # Commit the changes to the database
    conn.commit()
    print("Database 'sales_data.db' created and populated successfully.")

except sqlite3.Error as e:
    print(f"Database error: {e}")
finally:
    # Close the connection
    if conn:
        conn.close()


# --- 2. Connect to the database and run the SQL query ---
try:
    conn = sqlite3.connect("sales_data.db")

    # Define the SQL query to aggregate sales data
    query = """
        SELECT
            product,
            SUM(quantity) AS total_quantity,
            SUM(quantity * price) AS revenue
        FROM
            sales
        GROUP BY
            product
        ORDER BY
            revenue DESC
    """

    # Load the query results into a pandas DataFrame
    df = pd.read_sql_query(query, conn)

except sqlite3.Error as e:
    print(f"Database error: {e}")
    df = pd.DataFrame() # Create an empty DataFrame in case of an error
finally:
    if conn:
        conn.close()

# --- 3. Display the results ---

# Print the DataFrame to the console
print("\n--- Sales Data ---")
print(df)


# --- 4. Generate and save the bar chart ---
if not df.empty:
    # Plot a simple bar chart
    plt.figure(figsize=(10, 6)) # Set the figure size for better readability
    df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue', ax=plt.gca())

    # Add titles and labels for clarity
    plt.title('Total Revenue by Product')
    plt.xlabel('Product')
    plt.ylabel('Total Revenue ($)')
    plt.xticks(rotation=45, ha='right') # Rotate x-axis labels
    plt.tight_layout() # Adjust layout

    # Save the chart to a file
    chart_filename = "sales_revenue_chart.png"
    plt.savefig(chart_filename)

    print(f"\nBar chart saved as '{chart_filename}'")
else:
    print("\nCould not generate chart because no data was loaded.")
