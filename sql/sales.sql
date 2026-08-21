
SELECT * FROM `sales dataset`

-- بيانات الكل
SELECT `Gender`, ROUND( AVG(`Quantity`),2) as `Quantity_avg` ,  ROUND( AVG(`Total Amount`) ,2) as `Total Amount_avg` FROM `sales dataset` GROUP BY `Gender`

SELECT
    CASE
        WHEN MONTH(`Date`) = 1 THEN 'January'
        WHEN MONTH(`Date`) = 2 THEN 'February'
        WHEN MONTH(`Date`) = 3 THEN 'March'
        WHEN MONTH(`Date`) = 4 THEN 'April'
        WHEN MONTH(`Date`) = 5 THEN 'May'
        WHEN MONTH(`Date`) = 6 THEN 'June'
        WHEN MONTH(`Date`) = 7 THEN 'July'
        WHEN MONTH(`Date`) = 8 THEN 'August'
        WHEN MONTH(`Date`) = 9 THEN 'September'
        WHEN MONTH(`Date`) = 10 THEN 'October'
        WHEN MONTH(`Date`) = 11 THEN 'November'
        WHEN MONTH(`Date`) = 12 THEN 'December'
    END AS MONTH_name,
    ROUND(AVG(`Quantity`), 2) AS Quantity_avg,
    ROUND(AVG(`Total Amount`), 2) AS Total_Amount_avg
FROM `sales dataset`
GROUP BY MONTH(`Date`);




SELECT CASE 
    WHEN `Age` BETWEEN 18 and 24 THEN '18-24' 
    WHEN `Age` BETWEEN 25 and 34 THEN '25-34' 
    WHEN `Age` BETWEEN 34 and 44 THEN '35-44' 
    WHEN `Age` BETWEEN 45 and 54 THEN '45-54'
    WHEN `Age` BETWEEN 55 and 64 THEN '55-64' 
END as range_age ,ROUND( AVG(`Total Amount`),2) as `Total Amount_avg` ,ROUND( AVG(`Quantity`),2) as `Quantity_avg` FROM `sales dataset` GROUP BY range_age



SELECT `Product Category` , SUM(`Quantity`) as `Quantity_total` FROM `sales dataset` GROUP BY `Product Category` ORDER BY  `Quantity_total` DESC



-- بيانات النساء
SELECT
    CASE
        WHEN MONTH(`Date`) = 1 THEN 'January'
        WHEN MONTH(`Date`) = 2 THEN 'February'
        WHEN MONTH(`Date`) = 3 THEN 'March'
        WHEN MONTH(`Date`) = 4 THEN 'April'
        WHEN MONTH(`Date`) = 5 THEN 'May'
        WHEN MONTH(`Date`) = 6 THEN 'June'
        WHEN MONTH(`Date`) = 7 THEN 'July'
        WHEN MONTH(`Date`) = 8 THEN 'August'
        WHEN MONTH(`Date`) = 9 THEN 'September'
        WHEN MONTH(`Date`) = 10 THEN 'October'
        WHEN MONTH(`Date`) = 11 THEN 'November'
        WHEN MONTH(`Date`) = 12 THEN 'December'
    END AS MONTH_name,
    ROUND(AVG(`Quantity`), 2) AS Quantity_avg,
    ROUND(AVG(`Total Amount`), 2) AS Total_Amount_avg
FROM `sales dataset`
WHERE `Gender`='Female'
GROUP BY MONTH(`Date`);




SELECT CASE 
    WHEN `Age` BETWEEN 18 and 24 THEN '18-24' 
    WHEN `Age` BETWEEN 25 and 34 THEN '25-34' 
    WHEN `Age` BETWEEN 34 and 44 THEN '35-44' 
    WHEN `Age` BETWEEN 45 and 54 THEN '45-54'
    WHEN `Age` BETWEEN 55 and 64 THEN '55-64' 
END as range_age ,ROUND( AVG(`Total Amount`),2) as `Total Amount_avg` ,ROUND( AVG(`Quantity`),2) as `Quantity_avg` FROM `sales dataset` 
 WHERE `Gender`='Female'
GROUP BY range_age

SELECT `Product Category` , SUM(`Quantity`) FROM `sales dataset`WHERE `Gender`='Female' GROUP BY `Product Category` 

-- بيانات الرجال

SELECT
    CASE
        WHEN MONTH(`Date`) = 1 THEN 'January'
        WHEN MONTH(`Date`) = 2 THEN 'February'
        WHEN MONTH(`Date`) = 3 THEN 'March'
        WHEN MONTH(`Date`) = 4 THEN 'April'
        WHEN MONTH(`Date`) = 5 THEN 'May'
        WHEN MONTH(`Date`) = 6 THEN 'June'
        WHEN MONTH(`Date`) = 7 THEN 'July'
        WHEN MONTH(`Date`) = 8 THEN 'August'
        WHEN MONTH(`Date`) = 9 THEN 'September'
        WHEN MONTH(`Date`) = 10 THEN 'October'
        WHEN MONTH(`Date`) = 11 THEN 'November'
        WHEN MONTH(`Date`) = 12 THEN 'December'
    END AS MONTH_name,
    ROUND(AVG(`Quantity`), 2) AS Quantity_avg,
    ROUND(AVG(`Total Amount`), 2) AS Total_Amount_avg
FROM `sales dataset`
WHERE `Gender`='Male'
GROUP BY MONTH(`Date`);




SELECT CASE 
    WHEN `Age` BETWEEN 18 and 24 THEN '18-24' 
    WHEN `Age` BETWEEN 25 and 34 THEN '25-34' 
    WHEN `Age` BETWEEN 35 and 44 THEN '35-44' 
    WHEN `Age` BETWEEN 45 and 54 THEN '45-54'
    WHEN `Age` BETWEEN 55 and 64 THEN '55-64' 
END as range_age ,ROUND( AVG(`Total Amount`),2) as `Total Amount_avg` ,ROUND( AVG(`Quantity`),2) as `Quantity_avg` FROM `sales dataset` 
 WHERE `Gender`='Male'
GROUP BY range_age

SELECT `Product Category` , SUM(`Quantity`) FROM `sales dataset`WHERE `Gender`='male' GROUP BY `Product Category` 
