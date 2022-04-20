WITH
sellers as
(SELECT DISTINCT Seller_Of.UserId
FROM Seller_Of),

buyers as
(SELECT DISTINCT Bidder_Of.UserId
FROM Bidder_Of)

SELECT DISTINCT COUNT(*)
FROM sellers, buyers
WHERE sellers.UserId = buyers.UserId







