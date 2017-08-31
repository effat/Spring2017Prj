library('DMwR')

a<-read.csv("C:/Drive E/Spring 2017/PythonCodes/privacyArticles.csv",sep=",",header=T)

#create data frame
#Z = as.data.frame(a)
#f there are other columns you did not want to include as predictors, 
#you would have to remove them from X before using this trick, or using - in the model formula to exclude them. 
#For example, if you wanted to exclude the 67th predictor (that has the corresponding name x67), then you could write
#lm(Y ~ .-x67,data=Z)
#b<-a[,-1]
a$classLabel<-as.factor(a$classLabel)
smotedData <- SMOTE(classLabel ~ .-weblink, a, perc.over = 600,perc.under=100)

# Write CSV in R
write.csv(smotedData, file = "C:/Drive E/Spring 2017/PythonCodes/smotedPrivacyArticles.csv",row.names=FALSE)