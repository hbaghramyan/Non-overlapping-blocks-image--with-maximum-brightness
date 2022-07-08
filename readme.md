### An algorithm to find not intersecting blocks in an image with maximum brightness.

#### Task 3.1

Extract, summarise and export information from CSV files to a list

Your task is to prepare a function that will return a list of aggregated data from provided CSV files located in the "data" folder. The CSV files contains historical prices of traded shares of fictional companies. The filename of each file reflects the name of a fictional company. All data sets have the same structure and consist of six columns:

• date - a specific trading date in the format 'YYYY-MM-DD';

• open, max, min, close – the opening, maximum, minimum and closing prices, respectively;

• vol - volume (number of shares traded during a given day).

Task details

Create a function named solution that takes as an argument a list of paths to one or more of the provided files. The function should return a list of several nested lists. The length of the returned list equals the length of the list of paths passed to the function. Each nested list consists of two data frames with aggregated data for the individual company:

• first data frame: highest trading volume values in individual years o contains two columns: date - the date of the day with the highest trading volume in a year (parsed as a datetime, in the format 'YYYY-MM-DD'), and vol - the actual volume of shares traded in that day, o the number of rows of the data frame should be equal to the number of years in the history of the given company;

• second data frame: days of highest closing prices in individual years o contains two columns: date - the date of the day with the highest closing prices in a year (parsed as a datetime, in the format "YYYY-MM-DD'), and close - the actual closing price; if the same closing price occurred on more than one day in a given year, you should include them all with their full dates, o the number of rows of the data frame might be greater than the equivalent dimension for the first data frame.

#### Task 3.2

John likes to travel. He has visited a lot of cities over many years. Whenever he visits a city, he takes a few photos and saves them on his computer. Each photo has a name with an extension (jpg", "png' or "jpeg") and there is a record of the name of the city where the photo was taken and the time and date the photo; for example: "photo.jpg, Warsaw, 2013-09-05 14:08:15". Note that, in some rare cases, photos from different locations may share the time and date, due to timezone differences. John notices that his way of filing photos on his computer has become a mess. He wants to reorganize the photos. First he decides to group the photos by city, then, within each such group, sort the photos by the time they were taken and finally assign consecutive natural numbers to the photos, starting from 1. Afterwards he intends to rename all the photos. The new name of each photo should begin with the name of the city followed by the number already assigned to that photo. The number of every photo in each group should have the same length (equal to the length of the largest number in this group); thus, John needs to add some leading zeros to the numbers. The new name of the photo should end with the extension, which should remain the same. Your task is to help John by finding the new name of each photo. Each of John's photos has the format: '<>. <>, <>, yyyy-mm-dd, hh:mm:ss", where '<>', '<>' and", <>' consist only of letters of the English alphabet and supply the name of the photo, the file name extension and the city name, respectively. Be aware that the names of the photos may not be unique. 

Write a function that, given a string representing the list of M photos, returns the string representing the list of the new names of all photos (the order of photos should stay the same).

For example, given a string: "photo.jpg, Warsaw, 2013-09-05 14:08:15 john.png, London, 2015-06-20 15:13:22 myFriends.png, Warsaw, 2013-09-05 14:07:13 Eiffel.jpg, Paris, 2015-07-23 08:03:02 pisatower.jpg, Paris, 2015-07-22 23:59:59 BOB.jpg, London, 2015-08-05 00:02:03 notredame.png, Paris, 2015-09-01 12:00:00 me.jpg, Warsaw, 2013-09-06 15:40:22 a.png, Warsaw, 2016-02-13 13:33:50 b.jpg, Warsaw, 2016-01-02 15:12:22 c.jpg, Warsaw, 2016-01-02 14:34:30 d.jpg, Warsaw, 2016-01-02 15:15:01 e.png, Warsaw, 2016-01-02 09:49:09 f.png, Warsaw, 2016-01-02 10:55:32 g.jpg, Warsaw, 2016-02-29 22:13:11" 

your function should return:

Warsaw02.jpg Londoni.png Warsaw01.png Paris2.jpg Paris1.jpg London2.jpg Paris3.png Warsaw03.jpg Warsaw09.png Warsaw07.jpg Warsaw06.jpg Warsaw08.jpg Warsaw04.png Warsaw05.png Warsaw10.jpg as there are ten photos taken in Warsaw (numbered from 01 to 10). two photos in London (numbered from 1 to 2) and three photos in Paris (numbered from 1 to 3). The new names of the photos are returned in the same order as in the given string. 
· Each extension is "jpg", "png" or "jpeg. In your solution, focus on correctness.
