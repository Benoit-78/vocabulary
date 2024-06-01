--------------------------------
-- Data Manipulation Language --
--------------------------------
-- Working with data

-- Write
INSERT INTO `theme_perf` (`id_test`, `test_date`, `test`) VALUES (2, '2022-10-29', 83);

LOAD DATA INFILE '/path/data.txt' INTO TABLE your_table
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    (column1, column2, @percentage_variable)
    SET percentage = CAST(@percentage_variable AS SIGNED)
;
