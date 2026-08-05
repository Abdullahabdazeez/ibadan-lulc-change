/************************************************************
 IBADAN LULC 2013–2023 — FINAL GEE WORKFLOW
 Author: Abdullah Abdazeez Ayomide
 Classes: 1 Built-up, 2 Vegetation, 3 Water, 4 Bare soil
************************************************************/

var gaul = ee.FeatureCollection('FAO/GAUL/2015/level2');
var oyoLGAs = gaul.filter(ee.Filter.eq('ADM0_NAME','Nigeria'))
  .filter(ee.Filter.eq('ADM1_NAME','Oyo'));
var ibadanLGAs = oyoLGAs.filter(ee.Filter.or(
  ee.Filter.stringContains('ADM2_NAME','Ibadan'),
  ee.Filter.eq('ADM2_NAME','Akinyele'), ee.Filter.eq('ADM2_NAME','Egbeda'),
  ee.Filter.eq('ADM2_NAME','Ido'), ee.Filter.eq('ADM2_NAME','Lagelu'),
  ee.Filter.eq('ADM2_NAME','Oluyole'), ee.Filter.eq('ADM2_NAME','Ona-Ara'),
  ee.Filter.eq('ADM2_NAME','Ona Ara')
));
var studyArea = ibadanLGAs.geometry();
Map.centerObject(studyArea,9);

function prepareLandsat8(image){
  var qa=image.select('QA_PIXEL');
  var clearMask=qa.bitwiseAnd(1<<0).eq(0)
    .and(qa.bitwiseAnd(1<<1).eq(0)).and(qa.bitwiseAnd(1<<2).eq(0))
    .and(qa.bitwiseAnd(1<<3).eq(0)).and(qa.bitwiseAnd(1<<4).eq(0));
  var saturationMask=image.select('QA_RADSAT').eq(0);
  var optical=image.select(['SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7'],
    ['Blue','Green','Red','NIR','SWIR1','SWIR2']).multiply(0.0000275).add(-0.2);
  return optical.updateMask(clearMask).updateMask(saturationMask)
    .copyProperties(image,['system:time_start']);
}
function addIndices(image){
  var ndvi=image.normalizedDifference(['NIR','Red']).rename('NDVI');
  var ndbi=image.normalizedDifference(['SWIR1','NIR']).rename('NDBI');
  var mndwi=image.normalizedDifference(['Green','SWIR1']).rename('MNDWI');
  var bsi=image.expression('((S+R)-(N+B))/((S+R)+(N+B))',{S:image.select('SWIR1'),R:image.select('Red'),N:image.select('NIR'),B:image.select('Blue')}).rename('BSI');
  var evi=image.expression('2.5*((N-R)/(N+6*R-7.5*B+1))',{N:image.select('NIR'),R:image.select('Red'),B:image.select('Blue')}).rename('EVI');
  return image.addBands([ndvi,ndbi,mndwi,bsi,evi]);
}
function makeComposite(startDate,endDate,label){
  var collection=ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(studyArea)
    .filterDate(startDate,endDate).filter(ee.Filter.lt('CLOUD_COVER',60)).map(prepareLandsat8);
  print(label+' Landsat image count:',collection.size());
  return addIndices(collection.median().clip(studyArea));
}
var landsat2013=makeComposite('2013-04-01','2013-12-31','2013');
var landsat2023=makeComposite('2023-01-01','2023-12-31','2023');
var predictorBands=['Blue','Green','Red','NIR','SWIR1','SWIR2','NDVI','NDBI','MNDWI','BSI','EVI'];

var dynamicWorld=ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1').filterBounds(studyArea);
var dwBands=['water','trees','grass','flooded_vegetation','crops','shrub_and_scrub','built','bare','snow_and_ice'];
function makeDWComposite(startDate,endDate){return dynamicWorld.filterDate(startDate,endDate).select(dwBands).median().clip(studyArea);}
function makeFourClassDW(dwImage,threshold){
  var built=dwImage.select('built');
  var vegetation=dwImage.select(['trees','grass','flooded_vegetation','crops','shrub_and_scrub']).reduce(ee.Reducer.max());
  var probabilities=ee.Image.cat([built,vegetation,dwImage.select('water'),dwImage.select('bare')])
    .rename(['built_prob','vegetation_prob','water_prob','bare_prob']);
  var maxProbability=probabilities.reduce(ee.Reducer.max());
  return probabilities.toArray().arrayArgmax().arrayGet([0]).add(1).rename('class').toByte()
    .updateMask(maxProbability.gte(threshold));
}
var recentDWClass=makeFourClassDW(makeDWComposite('2022-01-01','2023-12-31'),0.65);
var earlyDWClass=makeFourClassDW(makeDWComposite('2016-01-01','2017-12-31'),0.60);
var stableDWClass=recentDWClass.updateMask(recentDWClass.eq(earlyDWClass)).rename('class').toByte();
var recentBuiltBuffer=recentDWClass.eq(1).unmask(0).focalMax({radius:1500,units:'meters'});
function spectralCandidates(image){
  return {
    water:image.select('MNDWI').gt(0.15).and(image.select('NDVI').lt(0.25)).selfMask().multiply(3).rename('class').toByte(),
    vegetation:image.select('NDVI').gt(0.50).and(image.select('MNDWI').lt(0.25)).selfMask().multiply(2).rename('class').toByte(),
    bare:image.select('BSI').gt(0.12).and(image.select('NDVI').lt(0.30)).and(image.select('MNDWI').lt(0.05)).and(recentBuiltBuffer.eq(0)).selfMask().multiply(4).rename('class').toByte(),
    built:image.select('NDBI').gt(0.05).and(image.select('NDVI').lt(0.40)).and(image.select('MNDWI').lt(0.05)).and(image.select('BSI').lt(0.30)).and(recentBuiltBuffer.eq(1)).selfMask().multiply(1).rename('class').toByte()
  };
}
var s13=spectralCandidates(landsat2013), s23=spectralCandidates(landsat2023);
var reference2013=stableDWClass.unmask(s13.water).unmask(s13.vegetation).unmask(s13.bare).unmask(s13.built).rename('class').toByte();
var reference2023=recentDWClass.unmask(s23.water).unmask(s23.vegetation).unmask(s23.bare).unmask(s23.built).rename('class').toByte();
reference2013=reference2013.updateMask(reference2013.gte(1).and(reference2013.lte(4)));
reference2023=reference2023.updateMask(reference2023.gte(1).and(reference2023.lte(4)));

function createSamples(predictors,reference,seedValue){
  return predictors.select(predictorBands).addBands(reference).stratifiedSample({
    numPoints:500,classBand:'class',classValues:[1,2,3,4],classPoints:[500,500,500,500],
    region:studyArea,scale:30,seed:seedValue,geometries:true,dropNulls:true,tileScale:4
  }).randomColumn('random',seedValue);
}
var samples2013=createSamples(landsat2013,reference2013,2013);
var samples2023=createSamples(landsat2023,reference2023,2023);
var training2013=samples2013.filter(ee.Filter.lt('random',0.70));
var validation2013=samples2013.filter(ee.Filter.gte('random',0.70));
var training2023=samples2023.filter(ee.Filter.lt('random',0.70));
var validation2023=samples2023.filter(ee.Filter.gte('random',0.70));
function trainRF(trainingFeatures,seedValue){
  return ee.Classifier.smileRandomForest({numberOfTrees:300,minLeafPopulation:2,bagFraction:0.70,seed:seedValue})
    .train({features:trainingFeatures,classProperty:'class',inputProperties:predictorBands});
}
var classifier2013=trainRF(training2013,2013), classifier2023=trainRF(training2023,2023);
var lulc2013=landsat2013.select(predictorBands).classify(classifier2013).rename('LULC').toByte().clip(studyArea)
  .focalMode({radius:1,units:'pixels',kernelType:'square'}).rename('LULC').toByte();
var lulc2023=landsat2023.select(predictorBands).classify(classifier2023).rename('LULC').toByte().clip(studyArea)
  .focalMode({radius:1,units:'pixels',kernelType:'square'}).rename('LULC').toByte();
function assessAccuracy(validationFeatures,classifier,yearLabel){
  var matrix=validationFeatures.classify(classifier).errorMatrix('class','classification',[1,2,3,4]);
  print(yearLabel+' confusion matrix:',matrix); print(yearLabel+' overall accuracy:',matrix.accuracy());
  print(yearLabel+' kappa coefficient:',matrix.kappa()); print(yearLabel+' producers accuracy:',matrix.producersAccuracy());
  print(yearLabel+' consumers accuracy:',matrix.consumersAccuracy());
}
assessAccuracy(validation2013,classifier2013,'2013'); assessAccuracy(validation2023,classifier2023,'2023');
var lulcPalette=['d7191c','1a9641','2c7bb6','fdae61'];
Map.addLayer(lulc2013,{min:1,max:4,palette:lulcPalette},'FINAL LULC 2013',true);
Map.addLayer(lulc2023,{min:1,max:4,palette:lulcPalette},'FINAL LULC 2023',false);

var classNames=ee.Dictionary({'1':'Built-up','2':'Vegetation','3':'Water','4':'Bare soil'});
function classAreas(classifiedImage,yearValue){
  var grouped=ee.Image.pixelArea().divide(1000000).rename('area_sqkm').addBands(classifiedImage.rename('class'))
    .reduceRegion({reducer:ee.Reducer.sum().group({groupField:1,groupName:'class'}),geometry:studyArea,scale:30,maxPixels:1e13,tileScale:4});
  return ee.FeatureCollection(ee.List(grouped.get('groups')).map(function(item){
    item=ee.Dictionary(item); var code=ee.Number(item.get('class')).toInt(); var area=ee.Number(item.get('sum'));
    return ee.Feature(null,{year:yearValue,class_code:code,class_name:classNames.get(code.format()),area_sqkm:area,area_ha:area.multiply(100)});
  }));
}
var areaTable2013=classAreas(lulc2013,2013), areaTable2023=classAreas(lulc2023,2023);
var transitionImage=lulc2013.multiply(10).add(lulc2023).rename('transition').toByte();
var builtUpGain=lulc2013.neq(1).and(lulc2023.eq(1)).selfMask().rename('built_up_gain');
var exportFolder='Ibadan_Final_LULC_2013_2023';
function exportImage(image,name){Export.image.toDrive({image:image,description:name,folder:exportFolder,fileNamePrefix:name,region:studyArea,scale:30,crs:'EPSG:32631',maxPixels:1e13,fileFormat:'GeoTIFF'});}
exportImage(lulc2013,'Ibadan_Final_LULC_2013'); exportImage(lulc2023,'Ibadan_Final_LULC_2023');
exportImage(transitionImage,'Ibadan_Final_Transition_2013_2023'); exportImage(builtUpGain.toByte(),'Ibadan_BuiltUp_Gain_2013_2023');
Export.table.toDrive({collection:areaTable2013,description:'Ibadan_Final_Area_Table_2013',folder:exportFolder,fileNamePrefix:'Ibadan_Final_Area_Table_2013',fileFormat:'CSV'});
Export.table.toDrive({collection:areaTable2023,description:'Ibadan_Final_Area_Table_2023',folder:exportFolder,fileNamePrefix:'Ibadan_Final_Area_Table_2023',fileFormat:'CSV'});
Export.table.toDrive({collection:ibadanLGAs,description:'Ibadan_Metropolitan_Boundary',folder:exportFolder,fileNamePrefix:'Ibadan_Metropolitan_Boundary',fileFormat:'SHP'});
