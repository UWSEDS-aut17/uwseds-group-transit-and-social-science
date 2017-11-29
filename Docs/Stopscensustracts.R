library(SDMTools)


setwd("C:/Users/jabbari/Desktop/uwseds-group-transit-and-social-science/Data/1_gtfs")
df<-read.csv("stops.csv")
setwd("C:/Users/jabbari/Desktop/uwseds-group-transit-and-social-science/Data")
tract<-readShapePoly(fn = "tract2010/tract2010",proj4string = CRS("+init=esri:102748"),repair = T)
tract<-spTransform(tract,CRS("+init=epsg:4326"))
tract_king<-tract[which(tract$COUNTYFP10=='033'),]

polys <- slot(tract_king,"polygons")

zones<- vector(mode = "list", length = 398)
for (i in 1:398) {
  
  zones[[i]]<-slot(slot(polys[[i]],"Polygons")[[1]],"coords"  )
}

df$census_tract_id<-NA
x1<-df
coordinates(x1) <-  ~stop_lon+stop_lat

for (i in 1:398){
  q<-pnt.in.poly(data.frame(coordinates(x1)),data.frame(zones[[i]])) 
  x1$census_tract_id<-ifelse(q$pip == 0, x1$census_tract_id,i )
  q<-NA
}

b=matrix(nrow = 398,ncol=1)
b[,1]<-as.numeric(as.character(tract_king$NAME10))
rownames(b)<-1:398
x1$census_tract_id2<-NA

for (i in 1:dim(x1)[1]){
  for (j in 1:398){
    x1$census_tract_id2[i]<-ifelse(x1$census_tract_id[i]== j, b[j,1],x1$census_tract_id2[i] )
  }
}

df$census_tract_id<-x1$census_tract_id2

write.csv(df,"stops-censustracts.csv")