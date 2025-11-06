# Gunicorn Options
Gunicorn offers a range of options to customize the server's behavior, including:

- Worker Processes: Adjust the number of worker processes to handle concurrent requests.
- Timeouts: Set custom timeouts for requests to avoid hanging processes.
- Logging: Configure detailed logging to monitor and debug application behavior.
- Daemon Mode: Run Gunicorn as a background service using daemon mode.


# Use Cases of GET Method
- Viewing a Webpage: When you type a URL in your browser, it sends a GET request to the server to fetch and display the webpage.
- Fetching Data: Many APIs use the GET method to fetch data, such as retrieving a list of users or fetching the details of a specific item.


# Common Use Cases for JSON Responses
- User Information: Providing user profiles or details for authenticated users.
- Product Data: Returning product details for e-commerce websites.
- Configuration Data: Sending configuration or settings data for software applications.


# Defining a Route with a Path Parameter
- Route Definition: The '/greet/<name>' defines a route that Flask will recognize. The <name> part in the URL is the path parameter.
- Route Function: The def greet(name): part defines a Python function that takes one argument (name) with the same name from the path.
- Return Statement: Finally, the function returns a JSON object that includes the value of the name parameter.


## Use Cases
Dynamic routes with path parameters are highly useful in web applications. Here are some common use cases:

- User Profiles: Create routes that capture user IDs to return profile information
/user/<user_id>.
- E-commerce: Define routes for product categories or specific products
/products/<category> or /products/<category>/<product_id>.


# Path vs Query Parameters
- Use path parameters for essential, hierarchical data that define the resource's identity.
- Query parameters are ideal for optional data that customizes the request, like filters and sorting.
- path parameters for required, resource-specific data and query parameters for optional, customizable data.


# Use Cases for URL Query Parameters
- Search Functionality: Implement search endpoints that take search terms as query parameters `/search?term=shoes`.
- Filtering Results: Filter results based on criteria like age, category, etc. `/users?age=25.`
- Customization: Customize responses based on user preferences `/dashboard?theme=dark.`

