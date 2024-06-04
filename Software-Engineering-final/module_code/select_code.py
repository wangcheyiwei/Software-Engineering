codes = [" "] * 7
size_codes=[" "]*7
codes[0] = """
SELECT 
    'Smelt' AS species,
    '<5' AS rang1,    
    SUM(CASE WHEN Weight < 5 THEN 1 ELSE 0 END) AS '<5',
    '5-10' AS rang2,
    SUM(CASE WHEN Weight BETWEEN 5 AND 10 THEN 1 ELSE 0 END) AS '5-10',
    '10-15' AS rang3,
    SUM(CASE WHEN Weight BETWEEN 10 AND 15 THEN 1 ELSE 0 END) AS '10-15',
    '15-20' AS rang4,
    SUM(CASE WHEN Weight BETWEEN 15 AND 20 THEN 1 ELSE 0 END) AS '15-20',
    '20-25' AS rang5,
    SUM(CASE WHEN Weight BETWEEN 20 AND 25 THEN 1 ELSE 0 END) AS '20-25',
    '>25' AS rang6,
    SUM(CASE WHEN Weight > 25 THEN 1 ELSE 0 END) AS '>25'
FROM 
    fish
WHERE 
    species = 'Smelt'
GROUP BY 
    species;
"""
codes[1] = """
SELECT 
    'Perch' AS species,
    '<5' AS rang1,
    SUM(CASE WHEN Weight < 5 THEN 1 ELSE 0 END) AS '<5',
    '5-250' AS rang2,
    SUM(CASE WHEN Weight BETWEEN 5 AND 250 THEN 1 ELSE 0 END) AS '5-250',
    '250-500' AS rang3,
    SUM(CASE WHEN Weight BETWEEN 250 AND 500 THEN 1 ELSE 0 END) AS '250-500',
    '500-750' AS rang4,
    SUM(CASE WHEN Weight BETWEEN 500 AND 750 THEN 1 ELSE 0 END) AS '500-750',
    '750-1000' AS rang5,
    SUM(CASE WHEN Weight BETWEEN 750 AND 1000 THEN 1 ELSE 0 END) AS '750-1000',
    '>1000' AS rang6,
    SUM(CASE WHEN Weight > 1000 THEN 1 ELSE 0 END) AS '>1000'
FROM
 fish
WHERE 
    species = 'Perch'
GROUP BY 
    species;
"""
codes[2] = """
SELECT 
    'Roach' AS species,
    '<5' AS rang1,
    SUM(CASE WHEN Weight < 5 THEN 1 ELSE 0 END) AS '<5',
    '5-75' AS rang2,
    SUM(CASE WHEN Weight BETWEEN 5 AND 75 THEN 1 ELSE 0 END) AS '5-75',
    '75-150' AS rang3,
    SUM(CASE WHEN Weight BETWEEN 75 AND 150 THEN 1 ELSE 0 END) AS '75-150',
    '150-225' AS rang4,
    SUM(CASE WHEN Weight BETWEEN 150 AND 225 THEN 1 ELSE 0 END) AS '150-225',
    '225-300' AS rang5,
    SUM(CASE WHEN Weight BETWEEN 225 AND 300 THEN 1 ELSE 0 END) AS '225-300',
    '>300' AS rang6,
    SUM(CASE WHEN Weight > 1000 THEN 1 ELSE 0 END) AS '>300'
FROM
 fish
WHERE 
    species = 'Roach'
GROUP BY 
    species;
"""
codes[3] = """
SELECT 
    'Parkki' AS species,
    '<5' AS rang1,
    SUM(CASE WHEN Weight < 5 THEN 1 ELSE 0 END) AS '<5',
    '5-50' AS rang2,
    SUM(CASE WHEN Weight BETWEEN 5 AND 75 THEN 1 ELSE 0 END) AS '5-50',
    '50-100' AS rang3,
    SUM(CASE WHEN Weight BETWEEN 75 AND 150 THEN 1 ELSE 0 END) AS '50-100',
    '100-150' AS rang4,
    SUM(CASE WHEN Weight BETWEEN 150 AND 225 THEN 1 ELSE 0 END) AS '100-150',
    '150-200' AS rang5,
    SUM(CASE WHEN Weight BETWEEN 225 AND 300 THEN 1 ELSE 0 END) AS '150-200',
    '>200' AS rang6,
    SUM(CASE WHEN Weight > 1000 THEN 1 ELSE 0 END) AS '>200'
FROM
 fish
WHERE 
    species = 'Parkki'
GROUP BY 
    species;
"""
codes[4] = """
SELECT 
    'Bream' AS species,
    '<200' AS rang1,
    SUM(CASE WHEN Weight < 5 THEN 1 ELSE 0 END) AS '<200',
    '200-250' AS rang2,
    SUM(CASE WHEN Weight BETWEEN 5 AND 75 THEN 1 ELSE 0 END) AS '200-250',
    '250-300' AS rang3,
    SUM(CASE WHEN Weight BETWEEN 75 AND 150 THEN 1 ELSE 0 END) AS '250-300',
    '300-350' AS rang4,
    SUM(CASE WHEN Weight BETWEEN 150 AND 225 THEN 1 ELSE 0 END) AS '300-350',
    '350-400' AS rang5,
    SUM(CASE WHEN Weight BETWEEN 225 AND 300 THEN 1 ELSE 0 END) AS '350-400',
    '>400' AS rang6,
    SUM(CASE WHEN Weight > 1000 THEN 1 ELSE 0 END) AS '>400'
FROM
 fish
WHERE 
    species = 'Bream'
GROUP BY 
    species;
"""

codes[5] = """
SELECT 
    'Whitefish' AS species,
   '<5' AS rang1,
    SUM(CASE WHEN Weight < 5 THEN 1 ELSE 0 END) AS '<5',
    '5-250' AS rang2,
    SUM(CASE WHEN Weight BETWEEN 5 AND 250 THEN 1 ELSE 0 END) AS '5-250',
    '250-500' AS rang3,
    SUM(CASE WHEN Weight BETWEEN 250 AND 500 THEN 1 ELSE 0 END) AS '250-500',
    '500-750' AS rang4,
    SUM(CASE WHEN Weight BETWEEN 500 AND 750 THEN 1 ELSE 0 END) AS '500-750',
    '750-1000' AS rang5,
    SUM(CASE WHEN Weight BETWEEN 750 AND 1000 THEN 1 ELSE 0 END) AS '750-1000',
    '>1000' AS rang6,
    SUM(CASE WHEN Weight > 1000 THEN 1 ELSE 0 END) AS '>1000'
FROM
 fish
WHERE 
    species = 'Whitefish'
GROUP BY 
    species;
"""

codes[6] = """
SELECT 
    'Pike' AS species,
   '<1000' AS rang1,
    SUM(CASE WHEN Weight < 5 THEN 1 ELSE 0 END) AS '<1000',
    '1000-1100' AS rang2,
    SUM(CASE WHEN Weight BETWEEN 5 AND 250 THEN 1 ELSE 0 END) AS '1000-1100',
    '1100-1200' AS rang3,
    SUM(CASE WHEN Weight BETWEEN 250 AND 500 THEN 1 ELSE 0 END) AS '1100-1200',
    '1200-1300' AS rang4,
    SUM(CASE WHEN Weight BETWEEN 500 AND 750 THEN 1 ELSE 0 END) AS '1200-1300',
    '1300-1400' AS rang5,
    SUM(CASE WHEN Weight BETWEEN 750 AND 1000 THEN 1 ELSE 0 END) AS '1300-1400',
    '>1400' AS rang6,
    SUM(CASE WHEN Weight > 1000 THEN 1 ELSE 0 END) AS '>1400'
FROM
 fish
WHERE 
    species = 'Pike'
GROUP BY 
    species;
"""
size_codes[0]="""
SELECT 
    'Smelt' AS species,
   '<5' AS rang1,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width < 5 THEN 1 ELSE 0 END) AS '<5',
    '5-25' AS rang2,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 5 AND 25 THEN 1 ELSE 0 END) AS '5-25',
    '25-50' AS rang3,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 25 AND 50 THEN 1 ELSE 0 END) AS '25-50',
    '50-75' AS rang4,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 50 AND 75 THEN 1 ELSE 0 END) AS '50-75',
    '75-100' AS rang5,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 75 AND 100 THEN 1 ELSE 0 END) AS '75-100',
    '>100' AS rang6,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width > 100 THEN 1 ELSE 0 END) AS '>100'
FROM
 fish
WHERE
    species = 'Smelt'
GROUP BY
    species;
"""
size_codes[1]="""
SELECT 
    'Perch' AS species,
   '<100' AS rang1,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width < 5 THEN 1 ELSE 0 END) AS '<100',
    '100-1800' AS rang2,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 100 AND 1800 THEN 1 ELSE 0 END) AS '100-1800',
    '1800-2500' AS rang3,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 1800 AND 2500 THEN 1 ELSE 0 END) AS '1800-2500',
    '2500-3200' AS rang4,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 2500 AND 3200 THEN 1 ELSE 0 END) AS '2500-3200',
    '3200-4000' AS rang5,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 3200 AND 4000 THEN 1 ELSE 0 END) AS '3200-4000',
    '>4000' AS rang6,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width > 4000 THEN 1 ELSE 0 END) AS '>4000'
FROM
 fish
WHERE
    species = 'Perch'
GROUP BY
    species;
"""

size_codes[2]="""
SELECT 
    'Roach' AS species,
   '<100' AS rang1,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width < 5 THEN 1 ELSE 0 END) AS '<100',
    '100-500' AS rang2,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 100 AND 500 THEN 1 ELSE 0 END) AS '100-500',
    '500-1000' AS rang3,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 500 AND 1000 THEN 1 ELSE 0 END) AS '500-1000',
    '1000-1500' AS rang4,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 1000 AND 1500 THEN 1 ELSE 0 END) AS '1000-1500',
    '1500-2000' AS rang5,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 1500 AND 2000 THEN 1 ELSE 0 END) AS '1500-2000',
    '>2000' AS rang6,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width > 2000 THEN 1 ELSE 0 END) AS '>2000'
FROM
 fish
WHERE
    species = 'Roach'
GROUP BY
    species;
"""

size_codes[3]="""
SELECT 
    'Parkki' AS species,
   '<300' AS rang1,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width < 300 THEN 1 ELSE 0 END) AS '<300',
    '300-600' AS rang2,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 300 AND 600 THEN 1 ELSE 0 END) AS '300-600',
    '600-900' AS rang3,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 600 AND 900 THEN 1 ELSE 0 END) AS '600-900',
    '900-1200' AS rang4,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 900 AND 1200 THEN 1 ELSE 0 END) AS '900-1200',
    '1200-1500' AS rang5,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 1200 AND 1500 THEN 1 ELSE 0 END) AS '1200-1500',
    '>1500' AS rang6,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width > 2000 THEN 1 ELSE 0 END) AS '>1500'
FROM
 fish
WHERE
    species = 'Parkki'
GROUP BY
    species;
"""

size_codes[4]="""
SELECT 
    'Bream' AS species,
   '<1000' AS rang1,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width < 1000 THEN 1 ELSE 0 END) AS '<1000',
    '1000-2000' AS rang2,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 1000 AND 2000 THEN 1 ELSE 0 END) AS '1000-2000',
    '2000-3000' AS rang3,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 2000 AND 3000 THEN 1 ELSE 0 END) AS '2000-3000',
    '3000-4000' AS rang4,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 3000 AND 4000 THEN 1 ELSE 0 END) AS '3000-4000',
    '4000-5000' AS rang5,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 4000 AND 5000 THEN 1 ELSE 0 END) AS '4000-5000',
    '>5000' AS rang6,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width > 5000 THEN 1 ELSE 0 END) AS '>5000'
FROM
 fish
WHERE
    species = 'Bream'
GROUP BY
    species;
"""

size_codes[5]="""
SELECT 
    'Whitefish' AS species,
   '<1000' AS rang1,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width < 1000 THEN 1 ELSE 0 END) AS '<1000',
    '1000-1500' AS rang2,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 1000 AND 2000 THEN 1 ELSE 0 END) AS '1000-1500',
    '1500-2000' AS rang3,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 1500 AND 2000 THEN 1 ELSE 0 END) AS '1500-2000',
    '2000-2500' AS rang4,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 2000 AND 2500 THEN 1 ELSE 0 END) AS '2000-2500',
    '2500-3000' AS rang5,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 2500 AND 3000 THEN 1 ELSE 0 END) AS '2500-3000',
    '>3000' AS rang6,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width > 3000 THEN 1 ELSE 0 END) AS '>3000'
FROM
 fish
WHERE
    species = 'Whitefish'
GROUP BY
    species;
"""

size_codes[6]="""
SELECT 
    'Pike' AS species,
   '<1000' AS rang1,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width < 1000 THEN 1 ELSE 0 END) AS '<1000',
    '1000-2000' AS rang2,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 1000 AND 2000 THEN 1 ELSE 0 END) AS '1000-2000',
    '2000-3000' AS rang3,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 2000 AND 3000 THEN 1 ELSE 0 END) AS '2000-3000',
    '3000-4000' AS rang4,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 3000 AND 4000 THEN 1 ELSE 0 END) AS '3000-4000',
    '4000-5000' AS rang5,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width BETWEEN 4000 AND 5000 THEN 1 ELSE 0 END) AS '4000-5000',
    '>5000' AS rang6,
    SUM(CASE WHEN (Length1+Length2+Length3)/3*Height*Width > 5000 THEN 1 ELSE 0 END) AS '>5000'
FROM
 fish
WHERE
    species = 'Pike'
GROUP BY
    species;
"""