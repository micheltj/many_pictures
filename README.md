# many_pictures

Please use this command to execute the Program: <br /> 
"py <Path to Repository>/many_pictures_python/index.py --dataset <Path to Repository>/videos/test.mp4 --index <Path to Repository>/index.csv --query <Path to Repository>/bilder/main.jpg --result-path <Path to Repository>/many_pictures_python --index_cut <Path to Repository>/index_target.csv"

  This Program will read an Input video found in the video folder and an Input Image found in the bilder folder.<br /> 
  The Input Image will be cut into multiple pieces.<br /> 
  Every piece will be replaced by an simmilar frame from the Input video.<br /> 
  We calculate the simmilarity with the chi2 distance of the colors.<br /> 
  At the End we save an Output Image into the bilder folder.<br /> 
