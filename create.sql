drop table if exists Item;
drop table if exists User;
drop table if exists Category;
drop table if exists Bid;
drop table if exists Category_Of;
drop table if exists Bidder_Of;
drop table if exists Seller_Of;
drop table if exists Bid_Item;

CREATE TABLE Item(
    ItemID INTEGER PRIMARY KEY,
    Item_Name TEXT,
    Buy_Price REAL,
    Currently REAL,
    First_Bid REAL,
    Number_of_Bids INTEGER,
    Started_At TEXT,
    Ends_At TEXT,
    Item_Description TEXT
);

CREATE TABLE User(
    UserId TEXT PRIMARY KEY,
    Rating INTEGER,
    Country TEXT,
    User_Location TEXT
);

CREATE TABLE Category(
    Category TEXT PRIMARY KEY
);

CREATE TABLE Bid(
    BidId INTEGER PRIMARY KEY,
    Time_Of_Bid  TEXT,
    Amount REAL
);

CREATE TABLE Category_Of(
    ItemId INTEGER,
    Category TEXT
);

CREATE TABLE Seller_Of(
    ItemId INTEGER PRIMARY KEY,
    UserId TEXT
);

CREATE TABLE Bidder_Of(
    BidId INTEGER PRIMARY KEY,
    UserId TEXT
);

CREATE TABLE Bid_Item(
    BidId INTEGER PRIMARY KEY,
    ItemId INTEGER
);

