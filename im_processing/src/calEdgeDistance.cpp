#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <cmath>
#include <mip/imgio.h>
#include <mip/miputil.h>

int main(int argc, char *argv[])
{
    if(argc!=8)
    {
        printf("Usage: calcEdgeDistance inim x0 y0 x1 y1 slicenum outim\n"
               "Description: calculates the distance from (x0,y0) to the object's boundary along"
                "the direction of the line formed by (x0,y0) and (x1,y1)\n");
        return -1;
    }
  int dimX,dimY,dimZ;
  //float *readimage3d(char *fp, int *piXdim, int *piYdim, int *piZdim);
  float *im=readimage3d(argv[1],&dimX,&dimY,&dimZ);
  int x0 = atoi(argv[2]);
  int y0 = atoi(argv[3]);
  int x1 = atoi(argv[4]);
  int y1 = atoi(argv[5]);
  int slicenum=atoi(argv[6]);
  int y,x;
  //slicenum = 33; //actaully we are accessing the 34th slice, skipping the first 33
  const bool y_long = (fabs(y1-y0) > fabs(x1-x0)); // if y_long is true, x becomes the given direction (every step increases one, starting from the start to the end point), y is then computed based on x.
  //Bresenham's method
   if  (y_long) {
   std::cout << "y_long" << std::endl ;
   for (int y = y0; y < y1 ;y++) {
   x=(y-y0)*(x0-x1)/(y0-y1)+x0;
   int i=dimX*dimY*slicenum+dimX*y+x;
   //std::cout << x << y << im[i] <<std::endl;
   std::cout << "("<< x << " " << y << " " << slicenum << ") " << im[i] <<std::endl;
   //for (int y = y0; y > y1 ;y--) {
  // x=(y-y0)*(x0-x1)/(y0-y1)+x0;
  // std::cout << "("<< x << " " << y << " " << slicenum << ") " << im[i] <<std::endl;
   

   if ( im[i] < 0.05 ) { //pixel value is less than a threshold; can make it a relative one 
       std::cout << "point to edge distance:" << y-y0 << std::endl;
       break;
   }
   else 
   {
   im[i] = 1;
   }
    }
   
  for (int y = y0; y > y1 ;y--) {
   x=(y-y0)*(x0-x1)/(y0-y1)+x0;
   int i=dimX*dimY*slicenum+dimX*y+x;
   //std::cout << x << y << im[i] <<std::endl;
   std::cout << "("<< x << " " << y << " " << slicenum << ") " << im[i] <<std::endl;


   if ( im[i] < 0.05 ) { //pixel value is less than a threshold; can make it a relative one 
       std::cout << "point to edge distance:" << fabs(y-y0) << std::endl;
       break;
   }
   else
   {
   im[i] = 1;
   }
    }

  
   }
   else {
   for (int x = x0; x < x1 ;x++) {
   y=(x-x0)*(y0-y1)/(x0-x1)+y0;
   int i=dimX*dimY*slicenum+dimX*y+x;
   std::cout << "("<< x << " " << y << " " << slicenum << ") " << im[i] <<std::endl;
   

   if ( im[i] < 0.05 ) { //pixel value is less than a threshold; can make it a relative one 
       std::cout << "point to edge distance:" << fabs(x-x0) << std::endl;
       break;
   }
   else
   {
   im[i] = 1;
   }

   }
 
   for (int x = x0; x > x1 ;x--) {
   y=(x-x0)*(y0-y1)/(x0-x1)+y0;
   int i=dimX*dimY*slicenum+dimX*y+x;
   std::cout << "("<< x << " " << y << " " << slicenum << ") " << im[i] <<std::endl;


   if ( im[i] < 0.05 ) { //pixel value is less than a threshold; can make it a relative one 
       std::cout << "point to edge distance:" << fabs(x-x0) << std::endl;
       break;
   }
   else
   {
   im[i] = 1;
   }

   }

   }

  writeimage(argv[7],dimX,dimY,dimZ,im);
  free_vector(im);
  return 0;
}
