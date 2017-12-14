setwd("C:/Users/jabbari/Desktop/uwseds-group-transit-and-social-science")

library(rgeos)
library(rgdal)
library(SDMTools)
library(geosphere)
library(shapefiles)
library(maptools)
library(gmapsdistance)
library(plyr)
library(rgeos)
require(devtools)
install_github("RFigisGeo", "openfigis")
require(RFigisGeo)

# Read shapefile for USA zipcodes
shp <-
  readShapePoly(
    fn = "Data/zips/tl_2015_us_zcta510",
    proj4string = CRS("+proj=longlat"),
    repair = T
  )

# Extracting Seattle zipcodes
shp <-
  shp[which(as.numeric(as.character(shp$ZCTA5CE10)) >= 98101 &
              as.numeric(as.character(shp$ZCTA5CE10)) <= 98199),]
non_seattle_zips <-
  c(98137,
    98138,
    98140,
    98142,
    98143,
    98147,
    98148,
    98149,
    98150,
    98151,
    98152,
    98153,
    98155,
    98156,
    98157,
    98158,
    98159,
    98160,
    98162,
    98163,
    98166,
    98167,
    98168,
    98169,
    98171,
    98172,
    98173,
    98176,
    98179,
    98180,
    98182,
    98182,
    98183,
    98184,
    98186,
    98187,
    98188,
    98189,
    98192,
    98192,
    98193,
    98196,
    98197,
    98198
  )

shp <-
  shp[which(as.numeric(as.character(shp$ZCTA5CE10)) != 98110), ]
shp <-
  shp[which(as.numeric(as.character(shp$ZCTA5CE10)) != 98123), ]
shp <-
  shp[which(as.numeric(as.character(shp$ZCTA5CE10)) != 98128), ]
shp <-
  shp[which(as.numeric(as.character(shp$ZCTA5CE10)) != 98130), ]
shp <-
  shp[which(as.numeric(as.character(shp$ZCTA5CE10)) != 98135), ]
shp <-
  shp[which((as.numeric(as.character(shp$ZCTA5CE10)) %in% non_seattle_zips) == F), ]


# Ordering shapefile rows based on zip code
shp <- shp[order(shp$ZCTA5CE10),]

# Write generated Seattle Shapefile
writeOGR(
  obj = shp,
  dsn = "zips_sea",
  layer = "shp",
  driver = "ESRI Shapefile"
)

# Read the shapefile generated in previous step
shp <-
  readOGR(dsn = "Data/zips_sea/shp.shp")


# Read shapefile for bus routes
network <- readOGR(dsn = "TransitRoutes/Transit_Routes_for_King_County_Metro__transitroute_line.shp")
network <- network[-1, ] # Frist row of shapefile includes all the routes which need to be dropped

# Seattle boundries shapefile
city <- readOGR(dsn = "data/city-limits.geojson")

# Droping routes not passing Seattle
## Finding routes not passing Seattle
non_seattle_bus_routes <- c()
for (i in 1:dim(network)[1]) {
  if (is.null(gIntersection(network[i, ], city)) == T) {
    non_seattle_bus_routes <- rbind(non_seattle_bus_routes, i)
  }
}
##Dropping non seattle bus routes
network <- network[-non_seattle_bus_routes[, 1], ]
## Write the bus route shapefiles
writeOGR(
  obj = network,
  dsn = "bus_seattle",
  layer = "network",
  driver = "ESRI Shapefile"
)

## Limited the routes to the ones that are active
network <- network[which(network$CURRENT_NE == "CURRENT"), ]
network[-which(network$OBJECTID == "226"), ] ## This one had no data in it

shp <- shp[-30, ]  ## This zip code had no data


#Finding bus routes that passes each zipcode
routes_list <- c()
passing_bus_num <- c()
zipcode_counts <- matrix(nrow = 30, ncol = 2)
colnames(zipcode_counts) <- c('zip', 'count')
zipcode_counts <- data.frame(zipcode_counts)

for (i in 1:dim(shp)[1]) {
  for (j in 1:dim(network)[1]) {
    if (is.null(intersection(network[j, ], shp[i, ])) == F) {
      passing_bus_num <- c(passing_bus_num, as.character(network$OBJECTID[j]))
    }
  }
  routes_list[[i]] <- as.numeric(passing_bus_num)
  zipcode_counts$zip[i] <- as.character(shp$GEOID10[i])
  zipcode_counts$count[i] <- length(passing_bus_num)
  passing_bus_num <- c()
  
}

zipcode_counts <- data.frame(zipcode_counts)
write.csv(zipcode_counts, "zips_seattle.csv")


# Conver list of routes to csv file
lapply(routes_list, function(x)
  write.table(
    data.frame(x),
    'routes_zipcode.csv'  ,
    append = T,
    sep = ','
  ))


# Loading the household data to get the income
hh <- read.csv("hhsurvey-households.csv")

#Drop househoulds that didn't provide their income
hh <- hh[which(hh$hh_income_detailed != 98), ]

#Assign average of each bracket to households
hh$income <- NA

hh$income <- ifelse(hh$hh_income_detailed == 1, 5000, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 2, 17500, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 3, 30000, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 4, 42500, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 5, 62500, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 6, 87500, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 7, 125000, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 8, 175000, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 9 , 225000, hh$income)
hh$income <- ifelse(hh$hh_income_detailed == 10, 250000, hh$income)

#Create a dataframe of average income for each zipcode
df <- aggregate(hh$income ~ hh$h_zip, FUN = mean)
df <- data.frame(df)
colnames(df) <- c("zip", "income")

#Add income column to shapefile
shp$income <- NA

#Only keep zipcodes that we have in Seattle shapefile
df <-
  df[which((as.character(df$zip) %in% as.character(shp$GEOID10)) == T), ]

#Merging income data to Seattle shapefile
for (i in 1:dim(shp)[1]) {
  for (j in 1:dim(df)[1]) {
    shp$income[i] <-
      ifelse(as.character(shp$GEOID10[i]) == as.character(df$zip[j]),
             df$income[j],
             shp$income[i])
  }
}

# Save shapefile
writeOGR(
  obj = shp,
  dsn = "zips_sea",
  layer = "shp",
  driver = "ESRI Shapefile"
)
