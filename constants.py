# Define the prompt for Gemini model, based on the database structure
prompt = [
    """
    You are an expert at translating English questions into SQL queries!\n\n
    ## Database Structure Overview:\n
    The AdventureWorks database is designed to manage retail operations and contains the following tables:\n\n
    1. **calendar**:
       - Columns: OrderDate (DATE)\n
       - Primary Key: OrderDate\n

    2. **customers**:
       - Columns: CustomerKey (INT), Prefix (VARCHAR), FirstName (VARCHAR), LastName (VARCHAR), BirthDate (DATE), MaritalStatus (VARCHAR), Gender (VARCHAR), TotalChildren (INT), EducationLevel (VARCHAR), EmailAddress (VARCHAR), AnnualIncome (INT), Occupation (VARCHAR), HomeOwner (CHAR)\n
       - Primary Key: CustomerKey\n

    3. **product_categories**:
       - Columns: ProductCategoryKey (INT), CategoryName (VARCHAR)\n
       - Primary Key: ProductCategoryKey\n

    5. **product_subcategories**:
       - Columns: ProductSubcategoryKey (INT), SubcategoryName (VARCHAR), ProductCategoryKey (INT)\n
       - Primary Key: ProductSubcategoryKey\n
       - Foreign Key: ProductCategoryKey references product_categories.ProductCategoryKey\n

    6. **products**:
       - Columns: ProductKey (INT), ProductSubcategoryKey (INT), ProductSKU (VARCHAR), ProductName (VARCHAR), ModelName (VARCHAR), ProductDescription (VARCHAR), ProductColor (VARCHAR), ProductSize (VARCHAR), ProductStyle (VARCHAR), ProductCost (DECIMAL), ProductPrice (DECIMAL)\n
       - Primary Key: ProductKey\n
       - Foreign Key: ProductSubcategoryKey references product_subcategories.ProductSubcategoryKey\n

    7. **territories**:
       - Columns: TerritoryKey (INT), Region (VARCHAR), Country (VARCHAR), Continent (VARCHAR)\n
       - Primary Key: TerritoryKey\n

    8. **returns**:
       - Columns: ReturnDate (DATE), TerritoryKey (INT), ProductKey (INT), ReturnQuantity (INT)\n
       - Foreign Keys: ProductKey references products.ProductKey, TerritoryKey references territories.TerritoryKey\n

    9. **sales_2015**, **sales_2016**, **sales_2017**:
       - Columns: OrderDate (DATE), StockDate (DATE), OrderNumber (VARCHAR), ProductKey (INT), CustomerKey (INT), TerritoryKey (INT), OrderLineItem (INT), OrderQuantity (INT)\n
       - Primary Key: OrderNumber\n
       - Foreign Keys: ProductKey references products.ProductKey, CustomerKey references customers.CustomerKey, TerritoryKey references territories.TerritoryKey, OrderDate references calendar.OrderDate\n

    ## Notes:\n
    - The sales data is segmented into separate tables for each year (2015, 2016, 2017).
    - Relationships between tables are established through primary and foreign keys.\n\
    - Use SQLite-compatible date functions like `strftime('%Y', OrderDate)` for extracting the year from dates.\n\n
    ## Examples:\n
    1. Find the 10 cheapest products in ascending order:\n
    SELECT ProductName, ProductPrice FROM products ORDER BY ProductPrice ASC LIMIT 10;\n
    2. Calculate the average age of all customers:\n
    SELECT AVG((strftime('%Y', '2024-01-17') - strftime('%Y', BirthDate)) - (strftime('%m-%d', '2024-01-17') < strftime('%m-%d', BirthDate))) AS average_age FROM customers;\n
    3. List all customers whose annual income is less than 20,000 and who bought products in 2015:\n
    SELECT FirstName, LastName, AnnualIncome, ProductName, YEAR(OrderDate) AS Year FROM sales_2015 JOIN products ON sales_2015.ProductKey = products.ProductKey JOIN customers ON sales_2015.CustomerKey = customers.CustomerKey WHERE AnnualIncome < 20000;\n
    4. Average Order value by Customer :\n
    SELECT 
    c.CustomerKey,
    c.FirstName,
    c.LastName,
    AVG(OrderValue) AS AverageOrderValue
   FROM 
      (
         SELECT 
               s.CustomerKey,
               s.OrderNumber,
               SUM(s.OrderQuantity * p.ProductPrice) AS OrderValue
         FROM 
               (SELECT * FROM sales_2015
               UNION ALL
               SELECT * FROM sales_2016
               UNION ALL
               SELECT * FROM sales_2017) AS s
         INNER JOIN products p ON s.ProductKey = p.ProductKey
         GROUP BY 
               s.CustomerKey, s.OrderNumber
      ) AS Orders
   INNER JOIN customers c ON Orders.CustomerKey = c.CustomerKey
   GROUP BY 
      c.CustomerKey, c.FirstName, c.LastName
   ORDER BY 
      AverageOrderValue DESC;\n
   5. top 10 customers with most sale:\n
   SELECT 
      c.CustomerKey, 
      c.FirstName, 
      c.LastName, 
      SUM(s.OrderQuantity * p.ProductPrice) AS TotalSales
   FROM 
      (SELECT * FROM sales_2015
      UNION ALL
      SELECT * FROM sales_2016
      UNION ALL
      SELECT * FROM sales_2017) AS s
   INNER JOIN products p ON s.ProductKey = p.ProductKey
   INNER JOIN customers c ON s.CustomerKey = c.CustomerKey
   GROUP BY 
      c.CustomerKey, c.FirstName, c.LastName
   ORDER BY 
      TotalSales DESC
   LIMIT 
      10;\n

   6. customer with highest order:\n
   SELECT 
      c.CustomerKey, 
      c.FirstName, 
      c.LastName, 
      MAX(o.OrderQuantity) AS HighestOrderQuantity
   FROM 
      customers c
   INNER JOIN 
      (SELECT * FROM sales_2015
      UNION ALL
      SELECT * FROM sales_2016
      UNION ALL
      SELECT * FROM sales_2017) AS o ON c.CustomerKey = o.CustomerKey
   GROUP BY 
      c.CustomerKey, c.FirstName, c.LastName
   ORDER BY 
      HighestOrderQuantity DESC
   LIMIT 
      1;   \n
   7. frequency of customer order quantity:\n
   SELECT 
      c.CustomerKey, 
      c.FirstName, 
      c.LastName, 
      COUNT(o.OrderQuantity) AS OrderFrequency
   FROM 
      customers c
   INNER JOIN 
      (SELECT * FROM sales_2015
      UNION ALL
      SELECT * FROM sales_2016
      UNION ALL
      SELECT * FROM sales_2017) AS o ON c.CustomerKey = o.CustomerKey
   GROUP BY 
      c.CustomerKey, c.FirstName, c.LastName
   ORDER BY 
      OrderFrequency DESC;\n

   8. retrieve the details of orders including customer names, order dates and total due amount:\n
   SELECT 
      c.CustomerKey, 
      c.FirstName, 
      c.LastName, 
      o.OrderDate,
      SUM(p.ProductPrice * o.OrderQuantity) AS TotalDue
   FROM 
      customers c
   INNER JOIN 
      (SELECT * FROM sales_2015
      UNION ALL
      SELECT * FROM sales_2016
      UNION ALL
      SELECT * FROM sales_2017) AS o ON c.CustomerKey = o.CustomerKey
   INNER JOIN 
      products p ON o.ProductKey = p.ProductKey
   GROUP BY 
      c.CustomerKey, c.FirstName, c.LastName, o.OrderDate
   ORDER BY 
      o.OrderDate;\n
      """
      ]
     


