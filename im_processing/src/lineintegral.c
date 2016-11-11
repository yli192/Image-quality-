#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mip/image.h>

#define SWAP(a,b,t) t=a,a=b,b=t
int   verbose=0; /* print out more detailed information */
/*define a type struct*/
typedef struct {
  char   *name;
  int   slicedim;  /* dimension perpendicular to slice */
  int   slicedist; /*distance between slices*/
  int	avgdim;  /*dimension for averaging*/
  int	startavg, endavg; /* start and end values for averaging*/
  int 	do_average; /*true if profiles are to be averaged, 0 if summed */
  int	arb_prof; /*true for profile along arbitrary line */
  int	x0,y0,x1,y1; /* endpoints for arbitrary slicing*/
  int	sum_only; /* true if only the sum is to be printed */
  int   startslice, endslice;
  int   AllSlices; /* profile in all slices */
  int   bWithHeader;
  double	scalefac;
  double	normsum;
  double   normheight;
  double  start, increment;
} USEROPTS;
/* Prototypes */
void myMain(IMAGE *pImage, USEROPTS *pUserOpts, FILE *fpout);
int arbitraryProfile(int x1, int y1, int x0, int y0, int pixformat, int xdim, int ydim, int *x_ind, int *y_ind, char *ppix, double *distances, double *values);
int main(int argc, char **argv);
void usageterm(void);
void errorterm(void);
/* MyMain */
void myMain(IMAGE *pImage, USEROPTS *pUserOpts, FILE *fpout)
{
	double x;
	double sum,max,normfac;
	double avgfac; /* factor for computing average */
	double *pDistances, *pValues;
  int *px_ind, *py_ind;
	int	profdim; /*dimension for profiling*/
  int slice;
	int i, itmp, numpixels;
	int xdir, ydir, xdim,ydim, nvals;
	int x0, y0, x1, y1, profx0, profx1, profy0, profy1;
	int dimc, dimv[nDIMV]; //dimv =[dim(z),dim(y),dim(x)], dimc=3 if it's a 3d im
	int endpts[nDIMV][2], coarseness[nDIMV];
	int pixformat, pixsize, maxmin[2], pixcnt; //total number of pixels in im
	char *image;
	REALTYPE *rimage;

	imheader(pImage,&pixformat,&pixsize,&pixcnt,&dimc,dimv,maxmin);
  //printf("%i\t%i\n",dimv[2],dimc);
  if (pUserOpts->arb_prof){ //pUserOpts->arb_prof !=0 , =1 in fact
		if (verbose) fprintf(stderr,"arbitrary profile direction\n");
		/* (x0,y0) and (x1,y1) are the upper right and lower left corners of the region to be profiled */
		x0 = pUserOpts->x0;
		y0 = pUserOpts->y0;
		x1 = pUserOpts->x1;
		y1 = pUserOpts->y1;
		/* make sure the endpoints are ur and ll instead of lr and ul */
		if (x0 > x1) {
      printf("before swap (x0,x1): %i\t%i\n",x0,x1);
			SWAP(x0,x1,itmp);
      printf("after swap (x0,x1): %i\t%i\n",x0,x1); }
		if (y0 > y1) {
      printf("%i\t%i\n",y0,y1);
			SWAP(y0,y1,itmp);}
    printf("(x0,x1,y0,y1): %i\t%i%i\t%i\t\n",x0,x1,y0,y1);
    //  printf("%i\t%i\n",y0,y1);
		/* xdir and ydir are the indices into dimv for the directions
       in which the profiling is to occur. note that xdir must always be
       greater than ydir */
		xdim = x1 - x0+1;
		ydim = y1 - y0+1;
		/* the profiling coordinates are relative to the slice read in
       from the file which has a dift origin */
		profx0 = pUserOpts->x0 - x0;
  //  printf("%i\t%i\n",profx0,x0);
		profx1 = pUserOpts->x1 - x0;
		profy0 = pUserOpts->y0 - y0;
		profy1 = pUserOpts->y1 - y0;
		if (verbose) {
			fprintf(stderr,"profile coords in original image=(%d,%d) to (%d,%d)\n",
				pUserOpts->x0, pUserOpts->y0,  pUserOpts->x1, pUserOpts->y1);
			fprintf(stderr,"ur and ll of subimage=(%d,%d) to (%d,%d)\n",
				x0, y0,  x1, y1);
			fprintf(stderr, "in shifted image, profile from (%d,%d) to (%d,%d)\n",
				profx0, profy0, profx1, profy1);
		}
    numpixels = xdim*ydim;
		if (dimc == 3){
			if (pUserOpts->slicedim == 0)
				ydir = 1;
			else
				ydir = 0;
			xdir = ydir+1;
			if (xdir == pUserOpts->slicedim) xdir++;
		}else{
			ydir=0;
			xdir=1;
		}
		endpts[xdir][0] = x0;
		endpts[xdir][1] = x1;
		endpts[ydir][0] = y0;
		endpts[ydir][1] = y1;
		/* allocate memory for pixels in slice, arrays to store x (Distances)
       and y (Values) values */
		image = (char *)malloc(numpixels*pixsize);
		nvals = arbitraryProfile(profx0, profy0, profx1, profy1,
			pixsize, xdim, ydim, NULL, NULL, NULL, NULL, NULL);
		if (verbose) fprintf(stderr, "%d points in profile\n",nvals);
    px_ind = (int *)malloc(sizeof(int) * nvals);
    py_ind = (int *)malloc(sizeof(int) * nvals);
		pValues = (double *)malloc(sizeof(double) * nvals);
		pDistances = (double *)malloc(sizeof(double) * nvals);
		if (pValues == NULL || pDistances == NULL || image == NULL){
			if (verbose) fprintf(stderr, "allocation error\n");
			exit(1);
		}
  }

  else{
    fprintf(stderr,"improf : non-arbitary\n");
  }

  for (i = dimc - 1; i >= 0; --i)
  		coarseness[i] = 1;

  	if (pUserOpts->AllSlices && dimc == 3)
  		pUserOpts->endslice = dimv[pUserOpts->slicedim]-1; //if the slicedim =145, the last slice is 144
      //printf("%i\n",dimv[pUserOpts->slicedim]);
      //printf("%i\n",pUserOpts->endslice);
  	for (slice = pUserOpts->startslice;
         slice <= pUserOpts->endslice; slice += pUserOpts->slicedist){
  		if (dimc == 3)
  			endpts[pUserOpts->slicedim][0]=endpts[pUserOpts->slicedim][1] = slice;
  		if (imgetpix(pImage, endpts, coarseness, (GREYTYPE *)image)
        == INVALID){
  			fprintf(stderr,"improf : error reading pixels\n");
  			errorterm();
  		}
  		if (verbose && pixformat == REAL){
  			for(i=0,sum=0, rimage=(REALTYPE *)image; i < numpixels; ++i)
  				sum += rimage[i];
  			fprintf(stderr,"sum=%.3g\n",sum);
  		}
  		if (pUserOpts->arb_prof){
        nvals = arbitraryProfile(profx0, profy0, profx1, profy1,
  				pixsize, xdim, ydim, px_ind,py_ind,image, pDistances, pValues);
  			for(i=1; i<nvals; ++i)
  				pDistances[i] = pUserOpts->start +
            pDistances[i]*pUserOpts->increment;
  			avgfac=1.0;
      }else{
          fprintf(stderr,"non-arbitary\n");
      }
/*print part*/
      if (pUserOpts->sum_only)
			fprintf(fpout,"%s:%d\t%.8g\n",pUserOpts->name,slice,sum);
		else{
			if (pUserOpts->bWithHeader)
				//printf("\"%s:slice %d\n",pUserOpts->name,slice);
			for(i=0; i < nvals; ++i)
      fprintf(fpout,"%i\t%i\t%.5lg\t%.5g\n",px_ind[i],py_ind[i],pDistances[i],pValues[i]);
      fputc('\n',fpout); }
      if (px_ind[i] == 0 && py_ind[i] == 0)
          break;
    }
      free(image);
	    free(pValues);
	    free(pDistances);
      free(px_ind);
      free(py_ind);
}
int arbitraryProfile(int x1, int y1, int x0, int y0, int pixformat, int xdim, int ydim, int *x_ind, int *y_ind, char *ppix, double *distances, double *values)
     /* extracts pixels from the real, grey, or byte image who's pixels are
        stored in ppix along the line starting from (x1,y1) to (x0,y0). The
        line is traced using Bresenhams algorithm (i.e. integral steps along
        the axis with which the line has the larges change in distance. The
        size of the image is specified by xdim and ydim. The routine returns the
        number of points traced and, if ppix is nonnull, the array of distances
        from (x1,y1) and the values of pixels along the line are returned in the
        double precision arrays distances and values, respectively.
     */
{
	int	x, y, delta_x, delta_y, s1, s2,
    temp, interchange, epsilon, i;
	int	ipix, itmp;
	REALTYPE *pRpix=(REALTYPE *)ppix;
	GREYTYPE *pGpix=(GREYTYPE *)ppix;
	BYTETYPE *pBpix=(BYTETYPE *)ppix;

	//int	x_coord;
	//int	y_coord;
  double	x_coord_c;
	double	y_coord_c;
  /*calculate slope and intercept from the end and start pts*/
  printf("step1:start and end pts: %i\t%i\t%i\t%i\n",x1,y1,x0,y0);
 //make sure x1,y1 are always greater than x0, y0
  if (x0 > x1) {
    //printf("before swap (x0,x1): %i\t%i\n",x0,x1);
    SWAP(x0,x1,itmp); }
    //printf("after swap (x0,x1): %i\t%i\n",x0,x1); }
  if (y0 > y1) {
    //printf("%i\t%i\n",y0,y1);
    SWAP(y0,y1,itmp);}
  printf("(x0,x1,y0,y1): %i\t%i\t%i\t%i\t\n",x1,y1,x0,y0);
//calcualte the half points
  double x0_hp=x0+0.5;
  double y0_hp=y0+0.5;
  double x1_hp=x1+0.5;
  double y1_hp=y1+0.5;
  double slope,intercept;

  delta_x = abs(x0 - x1);
  delta_y = abs(y0 - y1);
  printf("delta_x and delta_y: %i\t%i\n",delta_x,delta_y);
  if (x0 < x1)
    s1 = -1;
  else if (x0 > x1)
    s1 = 1;
  else
    s1 = 0;

  if (y0 < y1)
    s2 = -1;
  else if (y0 > y1)
    s2 = 1;
  else
    s2 = 0;

  /* interchange delta_x and delta_y depending on the slope of the line */
  if (delta_y > delta_x) {
    temp = delta_x;
    delta_x = delta_y;
    delta_y = temp;
    interchange = 1;
  } else
    interchange = 0;

  x = x1;
  y = y1;
  printf("%i\n",delta_x);
  if (ppix == NULL) return (delta_x); //if ppix is null, returns the number of pts(nvals) in profile
  printf("delta_x returned in mem_allocation:%i\n",delta_x);

  slope = (y0_hp-y1_hp)/(x0_hp-x1_hp);
  intercept = y1_hp - slope*x1_hp;
  printf("step1:slope and intercept:%f\t%f\n",slope,intercept);

  double x_c,y_c; //the current x and y coordinate
  double x_coord_hp=x1+0.5; // half coordinate of the start point
  double y_coord_hp=y1+0.5;
  x_c = x_coord_hp;
  y_c = y_coord_hp;

  //printf("%f\t%f\t%f\t%f\n",x_coord_hp,y_coord_hp,x_c,y_c);
	for (i = 0; i <= delta_x+2; i++) { //if the number of iterations is equal to interceptions + 2

    printf("previous (x,y): %f\t%f\n",x_c,y_c);
    double x_hp=x1+0.5;
    double y_hp=y1+0.5;
    double dis_c_x,dis_c_y;

    //initialize x_current and y_current to be the starting pt

    //go y; calc x_coord
    double y_coord_c_y = y_c - 0.5;
    double x_coord_c_y =( y_coord_c_y - intercept)/slope;
    //printf("x_coord_c, y_coord_c: %f\t%f\n",x_coord_c_y,y_coord_c_y);
    //find distance for use x-coord_c,and y_coord_c
    dis_c_y = sqrt ( (x_c - x_coord_c_y) * (x_c - x_coord_c_y) + (y_c - y_coord_c_y) * (y_c - y_coord_c_y) );
    //printf("distance if choose x-direction: %f\n",dis_c_y);
    //go x; calc y_coord
    double x_coord_c_x = x_c - 0.5;
    double y_coord_c_x = x_coord_c_x *slope + intercept;
    //printf("x_coord_c, y_coord_c: %f\t%f\n",x_coord_c_x,y_coord_c_x);
    //find distance for use x-coord_c,and y_coord_c
    dis_c_x = sqrt ( (x_c - x_coord_c_x) * (x_c - x_coord_c_x) + (y_c - y_coord_c_x) * (y_c - y_coord_c_x) );
    //printf("distance if choose y-direction: %f\n",dis_c_x);
    //assign distance based on dis_c_y > dis_c_x
    //int x_ind,y_ind;
    if (dis_c_y < dis_c_x) {
        distances[i] = dis_c_y;
        x_ind[i]=floor((x_coord_c_y + x_c)/2.0);
        y_ind[i]=floor((y_coord_c_y + y_c)/2.0);
        printf("current(x,y): %f\t%f\n",x_coord_c_y,y_coord_c_y);
        x_c = x_coord_c_y;
        y_c = y_coord_c_y; }
    else {
        distances[i] = dis_c_x;
        x_ind[i]=floor((x_coord_c_x + x_c)/2.0);
        y_ind[i]=floor((y_coord_c_x + y_c)/2.0);
        printf("current(x,y): %f\t%f\n",x_coord_c_x,y_coord_c_x);
        x_c = x_coord_c_x;
        y_c = y_coord_c_x; }
    //update x_c and y_c
    printf("index i=%i\n",i);
    if (x_ind[i] == x_ind[i-1] && y_ind[i] == y_ind[i-1]){
      printf("can be merged,index i=%i\n",i);
      distances[i-1]=distances[i]+distances[i-1];
      i=i-1;
      printf("after merging i=%i\n",i);
    }

    //determin pixel coord
		ipix = xdim * y_ind[i] + x_ind[i];
		switch (pixformat) {
			case REAL:
				values[i] = (double)pRpix[ipix];
				break;
			case GREY:
				values[i] = (double)pGpix[ipix];
				break;
			case BYTE:
				values[i] = (double)pBpix[ipix];
				break;
			default:
				break;
		}
    if (x_c == x0+0.5 && y_c == y0+0.5) { //break if reaching endpoint of the line
      break;
    }
	}

	return (delta_x+1);
}

/* Main() */
int main(int argc, char **argv)
{
	IMAGE    *pImage;
	int   pixformat,
    dimc,
    dimv[nDIMV];
	int itmp;
	USEROPTS userOpts;

  /* initialize user options */
	userOpts.slicedim = 0;  /* dimension perpendicular to slice */
	userOpts.slicedist = 1;/*distance between slices*/
	userOpts.avgdim= -1;  /*dimension for averaging*/
	userOpts.do_average=1; /*true if profiles are to be averaged, 0 if summed */
	userOpts.arb_prof=0; /*true for arbitrary slicing */
	userOpts.sum_only=0; /* true if only the sum is to be printed */
	userOpts.startslice = 0;
	userOpts.endslice = 0;
	userOpts.AllSlices=1; /* profile in all slices */
	userOpts.scalefac=1.0;
	userOpts.normsum=0.0;
	userOpts.normheight=0.0;
	userOpts.start=0;
	userOpts.increment=1;
	userOpts.bWithHeader=TRUE;

	if (argc == 1) usageterm();

	while(argc > 1){
		/* Interpret options */
		while (--argc > 0 && (*++argv)[0] == '-') {
			char   *s;
			for (s = argv[0] + 1; *s; s++)
				switch (*s){
          case 'v':
          case 'D':
            verbose = 1;
            break;
          case 'a':
            userOpts.do_average=0;
            break;
          case 't':
            userOpts.sum_only=1;
            break;
          case 'H':
            userOpts.bWithHeader=FALSE;
            break;
          case 'd': /* direction and coordinates for sliceing */
            if (sscanf(*++argv, "%d", &userOpts.slicedim) == 0)
              usageterm();
            if (sscanf(*++argv, "%d", &userOpts.startslice) == 0)
              usageterm();
            if (sscanf(*++argv, "%d", &userOpts.endslice) == 0)
              usageterm();
            if (verbose)fprintf(stderr,"slice range=(%d,%d)\n",
              userOpts.startslice,userOpts.endslice);
            argc -= 3;
            userOpts.AllSlices=0;
            break;

          case 'p': /* direction for orthogonal profiling */
            userOpts.arb_prof=0; /* turn of arbitrary profiling */
            if (sscanf(*++argv, "%d", &userOpts.avgdim) == 0)
              usageterm();
            if (sscanf(*++argv, "%d", &userOpts.startavg) == 0)
              usageterm();
            if (sscanf(*++argv, "%d", &userOpts.endavg) == 0)
              usageterm();
            argc -= 3;
            break;

          case 'b': /* arbitrary profiling */
            userOpts.arb_prof=1; /* turn of arbitrary profiling */
            if (sscanf(*++argv, "%d", &userOpts.x0) == 0)
              usageterm();
            if (sscanf(*++argv, "%d", &userOpts.y0) == 0)
              usageterm();
            if (sscanf(*++argv, "%d", &userOpts.x1) == 0)
              usageterm();
            if (sscanf(*++argv, "%d", &userOpts.y1) == 0)
              usageterm();
            argc -= 4;
            break;

          case 'c':/*coarseness (distance between slices)*/
            if (sscanf(*++argv, "%d", &userOpts.slicedist) == 0)
              usageterm();
            argc--;
            break;

          case 's':/*scale factor for profiles*/
            userOpts.normheight=userOpts.normsum=0.0;
            if (sscanf(*++argv, "%lf", &userOpts.scalefac) == 0)
              usageterm();
            argc--;
            break;

          case 'h':/*scale factor for profiles*/
            userOpts.normsum=0.0;
            userOpts.scalefac=1.0;
            userOpts.do_average=0;
            if (sscanf(*++argv, "%lf", &userOpts.normheight) == 0)
              usageterm();
            argc--;
            break;

          case 'x':/*x-axis values*/
            if (sscanf(*++argv, "%lf", &userOpts.start) == 0)
              usageterm();
            if (sscanf(*++argv, "%lf", &userOpts.increment) == 0)
              usageterm();
            argc -= 2;
            break;

          case 'n':/*normalization sum for profiles*/
            userOpts.normheight=0.0;
            userOpts.scalefac=1.0;
            userOpts.do_average=0;
            if (sscanf(*++argv, "%lf", &userOpts.normsum) == 0)
              usageterm();
            argc--;
            break;

          default:
            break;
        }
		}

		/* Get image name from argument list */
		if (argc < 1) usageterm();
		if ((userOpts.name = *argv) == NULL) usageterm();
		/* Open image */
		if ((pImage = imopen(userOpts.name, READ)) == INVALID)
			errorterm();
		if (imdim(pImage, &pixformat, &dimc) == INVALID)
			errorterm();

		if (pixformat != REAL && pixformat != GREY){
			fprintf(stderr, "images must be REAL or GREY type\n");
			exit(1);
		}
		if (dimc != 2 && dimc != 3) {
			fprintf(stderr, "improf : image must be 2 or 3D\n");
			exit(-1);
		}

		/* Initialize image parameters */

		if (imbounds(pImage, dimv) == INVALID)
			errorterm();

		if (userOpts.avgdim == -1){
			/*avgdim wasn't specified using -p option*/
			userOpts.avgdim = dimc-1;
			userOpts.startavg = 0;
			userOpts.endavg = dimv[userOpts.avgdim];
		}
		/* check parameters */
		if (userOpts.slicedim < 0 || dimc - 1 < userOpts.slicedim ||
			(dimc == 2 && userOpts.slicedim != 0)) {
			fprintf(stderr, "improf : illegal slicing dimension\n");
			exit(-1);
		}
		if (dimc == 3){
			if (userOpts.startslice > userOpts.endslice)
				SWAP(userOpts.startslice,userOpts.endslice,itmp);
			/* check whether slices to be processed are legal */
			if (userOpts.startslice < 0 || userOpts.endslice
        >= dimv[userOpts.slicedim]){
				fprintf(stderr, "improf : illegal starting or ending slice\n");
				exit(-1);
			}
		}
		if (userOpts.slicedist < 0) {
			fprintf(stderr, "improf: distance between slices must be > 0\n");
			exit(-1);
		}

		if (!userOpts.arb_prof){
			if (userOpts.avgdim < 0 || dimc - 1 < userOpts.avgdim) {
				fprintf(stderr, "improf : illegal averaging dimension\n");
				exit(-1);
			}
			if (userOpts.startavg > userOpts.endavg)
				SWAP(userOpts.startavg,userOpts.endavg,itmp);
			if (userOpts.startavg < 0 || userOpts.endavg >= dimv[userOpts.avgdim]){
				fprintf(stderr,
					"improf : illegal start or end value for averaging\n");
				exit(-1);
			}
		}
		/* do the application work */
		myMain(pImage, &userOpts,stdout);
		imclose(pImage);
	}
  return 0;
}

void usageterm(void)
{
  /* This routine is intended to be called when the command line is */
  /* not appropriate. It should try to give the user an indication  */
  /* the error made.                    */

  fprintf(stderr, "Usage: improf [options] image.im [[options] image.im ...]\n");
	fprintf(stderr,
		"%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n",
		"   -a don't do averaging over number of lines in profile,",
		"     simply display sum",
    "   -d dim1 start end : profiling will be done in a plane of",
 		"     constant dim1 starting with planes start and ending with",
 		"     end. The default is dim1=0 (z), start=0, end=zdim. For",
 		"     2d images this option has no effect.",
		"   -b x0 y0 x1 y1: arbitrary profile from (x0,y0) to (x1,y1).",
 		"   -p dim2 start end: profiling will be done perpendicular to direction",
 		"     dim2. The points in the profile will be average of the points",
 		"     in the dim2 direction having a value of start through ",
 		"     end. Default is dim2=dimc-1, start=0, end=dimv[dim2]",
		"   -t prints only the sum of the profile",
    "   -s scalefac: scale profile by multiplying by scalefac",
    "   -n normsum: normalize profiles to a sum of normfac. If nonzero ",
 		"     then scalefac is ignored.",
 		"   -h height: scale profiles to have height equal to argument",
 		"   -x start increment: start and increment for labeling x-axis");
  exit(0);
}


void errorterm(void)
{
  /* Print out the error message found in the imaging */
  /* routines error buffer and terminate the program. */

  fprintf(stderr, "Error on imagelib routine:\n\t");


  fprintf(stderr, "%s\n", imerror());
  exit(1);
}
