#include <cstdlib>
#include <cstdio>
#include <mip/imgio.h>
#include <mip/miputil.h>
int main(int argc, char *argv[])
{
	if(argc!=4)
	{
		printf("Usage: hard_thresholding inim threshold outim_name\n"
               "Description: if the pixel value is above threshold, it's changed"
                "to 10, otherwise it stays unchanged\n");
		return -1;
	}
  int dimX,dimY,dimZ;
	//float *readimage3d(char *fp, int *piXdim, int *piYdim, int *piZdim);
	float *im=readimage3d(argv[1],&dimX,&dimY,&dimZ);
	float t = atof(argv[2]);
	printf("Input image dimension X, Y, Z, and threshold: %i,%i,%i,%f\n",dimX,dimY,dimZ,t);
	int counter =0;
	for(int i=0;i<dimX*dimY*dimZ;i++)
	{
		if(im[i]>t)
		{
			im[i]=10;
			counter +=1;
		}
		else
			im[i]=0;
	}
	writeimage(argv[3],dimX,dimY,dimZ,im);
	printf("counter number of voxels greater than threshold: %d\n",counter);
	free_vector(im);
	return 0;
}
