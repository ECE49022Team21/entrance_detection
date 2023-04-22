# Initialize the detector parameters - picked a working combination from millions of random examples
parameters =  cv.aruco.DetectorParameters_create()
parameters.minDistanceToBorder =  7
parameters.cornerRefinementMaxIterations = 149
parameters.minOtsuStdDev= 4.0
parameters.adaptiveThreshWinSizeMin= 7
parameters.adaptiveThreshWinSizeStep= 49
parameters.minMarkerDistanceRate= 0.014971725679291437
parameters.maxMarkerPerimeterRate= 10.075976700411534 
parameters.minMarkerPerimeterRate= 0.2524866841549599 
parameters.polygonalApproxAccuracyRate= 0.05562707541937206
parameters.cornerRefinementWinSize= 9
parameters.adaptiveThreshConstant= 9.0
parameters.adaptiveThreshWinSizeMax= 369
parameters.minCornerDistanceRate= 0.09167132584946237
