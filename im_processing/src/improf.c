/*
 * Filename: improf
 * Routines:
 * Includes:
 * Dependencies:
 * Author:  Eric Frey
 * Date:  May 1990
 * Latest Revision:
 * 	27 March 1991: added flag AllSlices instead of checking for both start
 *                   and end slices == 0 as the condition for profiling all
 *							slices. This avoids the problem of wanting to get a
 *							profile of only the 1st slice. ecf.
 *
 *		9 December 1993: cleaned up code, added -b (profiles along arbitrary lines
 *				in a plane), -t (print sum of profile) and -x (set start and
 *				increment for labeling x axis) options. ecf.
 $Log: improf.c,v $
 * Revision 1.8  1995/01/03  15:11:21  frey
 * added code to print version number
 *
 * Revision 1.7  1995/01/03  15:08:55  frey
 * Fixed bug in arbitrary profiling when profile point was in lower left corner of bounding rectangle.
 *
 *
 * Program Name: improf
 *
 * Usage: prof [options] image.im
 * this routine generates a series of profiles suitable for piping into
 * graph or xgraph. Works for 2d and 3d images
 *
 *      options:
 *				-a don't do averaging over number of lines in profile, simple
 *					display sum
 *				-b x0 y0 x1 y1: does an arbitrary profile using bresenham algorithm
 *					from (x0,y0) to (x1,y1). This cancels any -p option already in
 *					effect the option. Since the distance between points on the
 *					profile is not 1, this effects the way sums are computed using
 *					the -s and -b options
 *				-d dim1 start end : profiling will be done in a plane of
 *					constant dim1 starting with planes start and ending with
 *					end. The default is dim1=0 (z), start=0, end=zdim. For
 *					2d images this option has no effect.
 *				-p dim2 start end: profiling will be done perpendicular to direction
 *					dim2. The points in the profile will be average of the points
 *					in the dim2 direction having a value of start through
 *					end. Default is dim2=dimc-1, start=0, end=dimv[dim2]
 *          -s scalefac: scale profile by multiplying by scalefac
 *          -t prints only the sum of the profile (in the case of -b it prints
 *					the integral performed using a trapezoidal rule
 *			   -n normsum: normalize profiles to a sum of normfac. If nonzero
 *					then scalefac is ignored. In the case of -b profiling the sum
 *					used is the integral performed using a trapezoidal rule.
 *				-h height: scale profiles to have height equal to argument
 *				-H: turn off printing of xgraph-style header
 *				-x start increment: start and increment for labeling x-axis
 *
 *
 *			Examples:
 *				profile all slices in z direction in x direction
 *					(for a 3d image) with y=30
 *					improf -p 1 30 30 image.im
 *				profile slice with z=20 in y direction (for a 3d image)
 *				averaging over	x=30 to 40:
 *					improf -d 0 20 20 -p 2 30 40 image.im
 *				profile in z direction for x=10 to 20 averaging
 *				y over 50 to 60:
 *					improf -d 2 10 20 -p 1 50 60 image.im
 *
 * Procedure:  Generates a profile through a 2d and 3d image
 *		and outputs to stdout. This can be piped into xgraph or graph.
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <mip/image.h>
//#ifndef WIN32
//#include "buildinfo.h"
//#endif

#define SWAP(a,b,t) t=a,a=b,b=t
int   verbose=0; /* print out more detailed information */
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
void perpendicularProfile(int startsum, int endsum, int sumdim, int profdim, int
  *dimv, int pixformat, char *image, double *pValues);
int arbitraryProfile(int x1, int y1, int x0, int y0, int pixformat, int xdim,
  int ydim, char *ppix, double *distances, double *values);
int main(int argc, char **argv);
void usageterm(void);
void errorterm(void);

void myMain(IMAGE *pImage, USEROPTS *pUserOpts, FILE *fpout)
{
	double x;
	double sum,max,normfac;
	double avgfac; /* factor for computing average */
	double *pDistances, *pValues;
	int	profdim; /*dimension for profiling*/
  int   slice;
	int   i, itmp, numpixels;
	int xdir, ydir, xdim,ydim, nvals;
	int x0, y0, x1, y1, profx0, profx1, profy0, profy1;
	int dimc, dimv[nDIMV];
	int endpts[nDIMV][2], coarseness[nDIMV];
	int pixformat, pixsize, maxmin[2], pixcnt;
	char *image;
	REALTYPE *rimage;

	imheader(pImage,&pixformat,&pixsize,&pixcnt,&dimc,dimv,maxmin);
	/* set up endpoints, etc. */
	if (pUserOpts->arb_prof){
		if (verbose) fprintf(stderr,"arbitrary profile direction\n");
		/* (x0,y0) and (x1,y1) are the upper right and lower left corners of the region to be profiled */
		x0 = pUserOpts->x0;
		y0 = pUserOpts->y0;
		x1 = pUserOpts->x1;
		y1 = pUserOpts->y1;
		/* make sure the endpoints are ur and ll instead of lr and ul */
		if (x0 > x1)
			SWAP(x0,x1,itmp);
		if (y0 > y1)
			SWAP(y0,y1,itmp);
		/* xdir and ydir are the indices into dimv for the directions
       in which the profiling is to occur. note that xdir must always be
       greater than ydir */
		xdim = x1 - x0+1;
		ydim = y1 - y0+1;
		/* the profiling coordinates are relative to the slice read in
       from the file which has a dift origin */
		profx0 = pUserOpts->x0 - x0;
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
			pixsize, xdim, ydim, NULL, NULL, NULL);
		if (verbose) fprintf(stderr, "%d points in profile\n",nvals);
		pValues = (double *)malloc(sizeof(double) * nvals);
		pDistances = (double *)malloc(sizeof(double) * nvals);
		if (pValues == NULL || pDistances == NULL || image == NULL){
			if (verbose) fprintf(stderr, "allocation error\n");
			exit(1);
		}
	}else{ /*set up for perpendicular profiling*/
		if (verbose) fprintf(stderr,"perpendiular profiling\n");
		/* note that slicedim, avgdim and profdim must add up to dimc*/
		if (dimc == 3)
			profdim=dimc-pUserOpts->slicedim-pUserOpts->avgdim;
		else /*dimc=2*/
			profdim = 1-pUserOpts->avgdim;
		/* set up endpts array*/
		endpts[pUserOpts->avgdim][0]=pUserOpts->startavg;
		endpts[pUserOpts->avgdim][1]=pUserOpts->endavg;
		endpts[profdim][0]=0;
		endpts[profdim][1]=dimv[profdim]-1;
		if (verbose){
			fprintf(stderr,"profdim=%d, avgdim=%d, slicedim=%d\n",
				profdim, pUserOpts->avgdim, pUserOpts->slicedim);
			fprintf(stderr,"endpts[profdim]=(%d,%d)\n",
        endpts[profdim][0],endpts[profdim][1]);
			fprintf(stderr,"endpts[avgdim]=(%d,%d)\n",
        endpts[pUserOpts->avgdim][0],endpts[pUserOpts->avgdim][1]);
			fprintf(stderr,"endpts[slicedim]=(%d,%d)\n",
        endpts[pUserOpts->slicedim][0],endpts[pUserOpts->slicedim][1]);
		}
		numpixels = (pUserOpts->endavg - pUserOpts->startavg + 1) *
      (dimv[profdim]);
		/* allocate memory for pixels */
		image = (char *)malloc(pixsize*numpixels);
		/* allocate memory for averaged pixels */
		pValues = (double *)malloc(sizeof(double) * dimv[profdim]);
		pDistances = (double *)malloc(sizeof(double) * dimv[profdim]);
		if (pValues == NULL || pDistances == NULL || image == NULL) {
			fprintf(stderr, "allocation error\n");
			exit(1);
		}
		nvals=dimv[profdim];
		for(i=0, x = pUserOpts->start;
				i < nvals;
				++i, x += pUserOpts->increment)
			pDistances[i] = x;
	}

	for (i = dimc - 1; i >= 0; --i)
		coarseness[i] = 1;

	if (pUserOpts->AllSlices && dimc == 3)
		pUserOpts->endslice = dimv[pUserOpts->slicedim]-1;

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
				pixsize, xdim, ydim, image, pDistances, pValues);
			for(i=1; i<nvals; ++i)
				pDistances[i] = pUserOpts->start +
          pDistances[i]*pUserOpts->increment;
			avgfac=1.0;
		}else{ /* sum pixels for perpendicular profiling */
      /* compute averages. if we are only extracting one line, this is
         a special case that can be handled simply by moving pixels */
			perpendicularProfile(pUserOpts->startavg, pUserOpts->endavg,
        pUserOpts->avgdim, profdim, dimv, pixformat, image, pValues);
			if (pUserOpts->do_average)
				avgfac = 1.0 / (pUserOpts->endavg - pUserOpts->startavg + 1);
			else
				avgfac = 1.0;
			if (verbose)fprintf(stderr,"avgfac=%.4g\n",avgfac);
		}
		/* now do any normalization */
		if (pUserOpts->sum_only || pUserOpts->normsum != 0.0){
			/* normalize to sum of profiles */
			/* so trap integration and direct sum of perpendicular
         profiles give same result, add half of 1st and last values */
			sum =0.5*(pValues[0]+pValues[nvals-1]);
			for(i=0; i<nvals-1; ++i){
				sum += 0.5*(pValues[i]+pValues[i+1])*
					(pDistances[i+1]-pDistances[i]);
			}
			sum = sum / pUserOpts->increment;
			normfac = sum != 0.0 ? pUserOpts->normsum/sum : 1.0;
		}else if (pUserOpts->normheight != 0.0){
      /* normalize by height (maximum value) */
			max = pValues[0];
			for(i=1; i<nvals; ++i)
				max = pValues[i] > max ? pValues[i] : max;
			normfac = max != 0.0 ? pUserOpts->normheight/max : 1.0;
		}else{
			/* scale values by fixed number */
			normfac = pUserOpts->scalefac;
		}
		normfac = normfac*avgfac;
		/* now print out the profile */
    if (verbose) fprintf(stderr,"normfac=%.4g\n",normfac);
		if (pUserOpts->sum_only)
			fprintf(fpout,"%s:%d\t%.8g\n",pUserOpts->name,slice,sum);
		else{
			if (pUserOpts->bWithHeader)
				printf("\"%s:slice %d\n",pUserOpts->name,slice);
			for(i=0; i < nvals; ++i)
				fprintf(fpout,"%.5lg\t%.5g\n",pDistances[i],pValues[i]*normfac);
			fputc('\n',fpout);
		}
	}
	free(image);
	free(pValues);
	free(pDistances);
}

void perpendicularProfile(int startsum, int endsum, int sumdim, int profdim, int *dimv, int pixformat, char *image, double *pValues)
     /* compute perpendicular profile given the direction to profile and sum in
      * (profdim and avgdim, respectively). The resulting values are summed into the
      * double precision array pValues[].
      */



{
	REALTYPE *pReal, *pR;
	GREYTYPE *pGrey, *pG;
	double *psum, sum;
	int i,j, rowinc, colinc;

	if (startsum == endsum){
		if (pixformat == GREY){
			pGrey=(GREYTYPE *)image;
			psum = pValues;
			for(i=dimv[profdim]; i > 0; --i)
				*psum++ = (double)*pGrey++;
		}else{/*real*/
			pReal=(REALTYPE *)image;
			psum = pValues;
			for(i=dimv[profdim]; i > 0; --i)
				*psum++ = (double)*pReal++;
		}
	}else{/* must do averaging. if sumdim > profdim then the pixels
           to be summed are contiguous. If not they are seperated
           by dimv[profdim] */
		if (sumdim > profdim){
			colinc = endsum - startsum + 1;
			rowinc = 1;
		}else{
			rowinc = dimv[profdim];
			colinc = 1;
		}
		if (verbose)fprintf(stderr,"colinc=%d, rowinc=%d\n",rowinc, colinc);
		if (pixformat == GREY){
			pGrey = (GREYTYPE *)image;
			psum = pValues;
			for(i=dimv[profdim]; i > 0; --i){
				pG = pGrey;
				*psum = 0.0;
				for(j=endsum - startsum + 1; j > 0; --j){
					*psum += (double)*pG;
					pG += rowinc;
				}
				pGrey += colinc;
				psum++;
			}
		}else{
			pReal = (REALTYPE *)image;
			psum = pValues;
			for(i=dimv[profdim]; i > 0; --i){
				pR = pReal;
				*psum = 0.0;
				for(j=endsum - startsum + 1; j > 0; --j){
					*psum += (double)*pR;
					pR += rowinc;
				}
				pReal += colinc;
				psum++;
			}
		}
	}
	if (verbose){
		for(i=0,sum=0; i < dimv[profdim]; ++i)
			sum += pValues[i];
		fprintf(stderr,"sum=%.3g\n",sum);
	}
}


int arbitraryProfile(int x1, int y1, int x0, int y0, int pixformat, int xdim, int ydim, char *ppix, double *distances, double *values)
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
	int	ipix;
	REALTYPE *pRpix=(REALTYPE *)ppix;
	GREYTYPE *pGpix=(GREYTYPE *)ppix;
	BYTETYPE *pBpix=(BYTETYPE *)ppix;

	int	x_coord;
	int	y_coord;


	delta_x = abs(x0 - x1);
	delta_y = abs(y0 - y1);

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

	/*initialize the error term to compensate for a nonzero intercept*/
	epsilon = 2 * delta_y - delta_x;

	if (ppix == NULL) return (delta_x+1);
	for (i = 0; i <= delta_x; i++) {
		x_coord = x;
		y_coord = y;

		while (epsilon >= 0) {
			if (interchange)
				x = x + s1;
			else
				y = y + s2;

			epsilon -= (2 * delta_x);
		}
		if (interchange)
			y = y + s2;
		else
			x = x + s1;
		epsilon += (2 * delta_y);

		distances[i] = sqrt ((double)((x1 - x_coord) * (x1 - x_coord) +
                           (y1 - y_coord) * (y1 - y_coord)));

		ipix = xdim*y_coord + x_coord;

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
	}
	return (delta_x+1);
}

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

/*#ifndef WIN32
  extern BuildInfo improf_buildinfo;
  extern BuildInfo libim_buildinfo;

  if (CheckForVersionSwitch(argc, argv))
  {
    fprintf(stderr, "%s\n%s",
      GetBuildSummary(&improf_buildinfo),
      GetBuildSummary(&libim_buildinfo));
    exit(0);
  }
#endif */
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

/*#ifndef WIN32
		if (verbose)
			fprintf(stderr, "%s\n", GetBuildString(&improf_buildinfo));
#endif*/
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
