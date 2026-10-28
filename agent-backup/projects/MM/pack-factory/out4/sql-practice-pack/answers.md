# Answers

One valid answer per exercise; yours may differ if it returns the same rows.

## 1. List all customers from Austin.
```sql
select * from customers where city = 'Austin' order by id;
```
Returns 11 row(s).

## 2. Count customers per city, largest first.
```sql
select city, count(*) n from customers group by city order by n desc, city;
```
Returns 5 row(s).

## 3. List products over $40, most expensive first.
```sql
select name, price from products where price > 40 order by price desc;
```
Returns 4 row(s).

## 4. What is the average product price per category?
```sql
select category, round(avg(price), 2) avg_price from products group by category order by category;
```
Returns 3 row(s).

## 5. How many orders are in each status?
```sql
select status, count(*) n from orders group by status order by status;
```
Returns 3 row(s).

## 6. Show each order with the customer's name (join).
```sql
select o.id, c.name from orders o join customers c on c.id = o.customer_id order by o.id;
```
Returns 120 row(s).

## 7. Total quantity sold per product name.
```sql
select p.name, sum(oi.qty) qty from order_items oi join products p on p.id = oi.product_id group by p.name order by qty desc, p.name;
```
Returns 15 row(s).

## 8. Revenue per order for paid orders (qty x price).
```sql
select o.id, round(sum(oi.qty * p.price), 2) revenue from orders o join order_items oi on oi.order_id = o.id join products p on p.id = oi.product_id where o.status = 'paid' group by o.id order by o.id;
```
Returns 64 row(s).

## 9. Top 5 customers by number of orders.
```sql
select c.name, count(*) n from orders o join customers c on c.id = o.customer_id group by c.id order by n desc, c.name limit 5;
```
Returns 5 row(s).

## 10. Customers who never ordered.
```sql
select c.name from customers c left join orders o on o.customer_id = c.id where o.id is null order by c.id;
```
Returns 1 row(s).

## 11. Orders per month.
```sql
select substr(order_date, 1, 7) month, count(*) n from orders group by month order by month;
```
Returns 9 row(s).

## 12. Categories with more than 4 products.
```sql
select category, count(*) n from products group by category having n > 4 order by category;
```
Returns 2 row(s).

## 13. Most expensive product in each category.
```sql
select p.category, p.name, p.price from products p where p.price = (select max(price) from products where category = p.category) order by p.category;
```
Returns 3 row(s).

## 14. Customers who bought a Tools product.
```sql
select distinct c.name from customers c join orders o on o.customer_id = c.id join order_items oi on oi.order_id = o.id join products p on p.id = oi.product_id where p.category = 'Tools' order by c.name;
```
Returns 23 row(s).

## 15. Running total of orders by month.
```sql
select month, n, sum(n) over (order by month) running from (select substr(order_date, 1, 7) month, count(*) n from orders group by month) order by month;
```
Returns 9 row(s).

## 16. Rank products by units sold (window function).
```sql
select name, qty, rank() over (order by qty desc) rnk from (select p.name, sum(oi.qty) qty from order_items oi join products p on p.id = oi.product_id group by p.name) order by rnk, name;
```
Returns 15 row(s).

## 17. Refund rate: share of orders that are refunded.
```sql
select round(100.0 * sum(status = 'refunded') / count(*), 1) pct from orders;
```
Returns 1 row(s).

## 18. Customers whose first order was in the first quarter of the year.
```sql
select c.name from customers c join (select customer_id, min(order_date) first_order from orders group by customer_id) f on f.customer_id = c.id where f.first_order < '2026-04-01' order by c.name;
```
Returns 26 row(s).

## 19. Average order value (paid orders only).
```sql
select round(avg(rev), 2) aov from (select o.id, sum(oi.qty * p.price) rev from orders o join order_items oi on oi.order_id = o.id join products p on p.id = oi.product_id where o.status = 'paid' group by o.id);
```
Returns 1 row(s).

## 20. Orders containing more than one distinct product.
```sql
select order_id, count(distinct product_id) n from order_items group by order_id having n > 1 order by order_id;
```
Returns 85 row(s).
