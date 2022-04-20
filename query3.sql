WITH
temp as (SELECT ItemId, COUNT(*) as num
FROM Category_Of
GROUP BY ItemId)

SELECT COUNT(*)
FROM temp
WHERE num = 4
