WITH
expensiveItems as 
(SELECT Item.ItemId, Currently
FROM Item
WHERE Currently > 100 AND Number_of_Bids > 0),

joined as
(SELECT DISTINCT Category_Of.Category
FROM Category_Of, expensiveItems
WHERE Category_Of.ItemId = expensiveItems.ItemId)

SELECT COUNT(*)
FROM joined

