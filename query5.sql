WITH
temp as
(SELECT DISTINCT Seller_Of.UserId, User.rating
FROM Seller_Of, User
WHERE Seller_Of.UserId = User.UserId)

SELECT COUNT(*)
FROM temp
WHERE rating > 1000


