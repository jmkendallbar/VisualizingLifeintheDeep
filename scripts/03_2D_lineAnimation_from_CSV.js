//This is a script that can be run in After Effects to allow data in a CSV to drive 
//a vector graphic line animation. Follow the instructions in the Line Animation tutorial.

var numberOfPoints = thisComp.layer("03_Example_LineAnimation_COVIDdata.csv")("Data")("Number of Rows");
//Setting # of Point variable equal to the number of rows of data in CSV
var spacingForPoints = thisComp.width / numberOfPoints; //Spacing points
var startingPointX = 0; //Setting the first X value position
var thePath = content("Shape 1").content("Path 1").path; //Renaming path
var maximumYValue = 1200000; //Maximum Y value
var lineHeight = 0; //Initializing lineHeight variable
var arrayOfPoints = []; //Creating an empty array called arrayOfPoints

for(var i = 0; i < numberOfPoints; i++) { 
//Writing a for loop that loops through each row of data
  var data = thisComp.layer("03_Example_LineAnimation_COVIDdata.csv");
  var dailyCases = data.footage("03_Example_LineAnimation_COVIDdata.csv").dataValue([3,i])
  lineHeight = linear(dailyCases, 0, maximumYValue, content("Shape 1").content("Stroke 1").strokeWidth/2, thisComp.height)*-1;
//Function remaps data from the bottom of the composition to the top.
  arrayOfPoints[i] = [startingPointX, lineHeight];
//Store new x and y data into the array arrayOfPoints
  startingPointX += spacingForPoints;
//Update x value by adding the spacing between points
}

thePath.createPath(points=arrayOfPoints, inTangents=[], outTangents=[], is_closed=false);
