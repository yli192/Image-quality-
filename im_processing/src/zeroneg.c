/*---------------------------------------------------------------------------*/
/*                                                                           */
/* Program:  zeroneg							     */
/*                                                                           */
/* Purpose:  sets all pixels with value less than zero to zero   */
/*                                                                           */
/* Inputs:   An input image file.					     */
/*                                                                           */
/* Outputs:  An output image file.					     */
/*                                                                           */
/* Contains: MyMain							     */
/*           main							     */
/*                                                                           */
/* Author:   Eric Frey							     */
/*                                                                           */
/* Date:     13 June 1990						     */
/*                                                                           */
/* Usage:    zeroneg [options] infile outfile				     */
/*                                                                           */
/* Options:  [-D]          Print debugging information.			     */
/*	     [-i]          Copy information fields.			     */
/*	     [-t "title"]  Specify output image title			     */
/*                                                                           */
/*---------------------------------------------------------------------------*/
/*page*/
/*---------------------------------------------------------------------------*/
/*                                                                           */
/* Globals:  The following global constants and variables are used to        */
/*           store the image being processed and lookup tables.              */
/*                                                                           */
/*---------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <mip/image.h>
#include <math.h>
#ifdef WIN32
#include <float.h>
#define isnan _isnan
#endif
#ifndef WIN32
#include "buildinfo.h"
#endif

/* Image file and variables */
IMAGE  *image1;
IMAGE  *image2;
GREYTYPE       *pixel1;
GREYTYPE       *pixel2;
int	pixformat;
int	pixsize;
int	pixcnt;
int	dimc;
int	dimv[nDIMV];
int	maxmin[nMAXMIN];
int	histo[nHISTOGRAM];
int	xdim;
int	ydim;

/* Program variables */
int	Debug = FALSE;
int	Normalize = FALSE; /* true to renormalize to same total counts */
int	ZeroNan=FALSE; /* zero not-a-numbers */


/*page*/
/*---------------------------------------------------------------------------*/
/*                                                                           */
/* Purpose:  These MACROs are used to read and write image intensity values. */
/* 	     It should be realized that they will slow the program down.     */
/* 	     Note also that they treat the pixel array modularly.  For	     */
/* 	     many applications, this may not be the thing to do.	     */
/*                                                                           */
/*---------------------------------------------------------------------------*/
#define Read_I1(i,x,y) \
   if ((0<=(y)) && ((y)<ydim) && (0<=(x)) && ((x)<xdim))\
      i = pixel1[(y)*xdim + (x)];\
   else\
      i = pixel1[(((y)+ydim)%ydim)*xdim + (((x)+xdim)%xdim)];

#define Write_I1(i,x,y) \
   if ((0<=(y)) && ((y)<ydim) && (0<=(x)) && ((x)<xdim))\
      pixel1[(y)*xdim + (x)] = i;\
   else\
      pixel1[(((y)+ydim)%ydim)*xdim + (((x)+xdim)%xdim)] = i;

#define Read_I2(i,x,y) \
   if ((0<=(y)) && ((y)<ydim) && (0<=(x)) && ((x)<xdim))\
      i = pixel2[(y)*xdim + (x)];\
   else\
      i = pixel2[(((y)+ydim)%ydim)*xdim + (((x)+xdim)%xdim)];

#define Write_I2(i,x,y) \
   if ((0<=(y)) && ((y)<ydim) && (0<=(x)) && ((x)<xdim))\
      pixel2[(y)*xdim + (x)] = i;\
   else\
      pixel2[(((y)+ydim)%ydim)*xdim + (((x)+xdim)%xdim)] = i;



/*---------------------------------------------------------------------------*/
/*                                                                           */
/* Purpose:  This MACRO is used to print an error message and abort program. */
/*                                                                           */
/*---------------------------------------------------------------------------*/
#define Abort(Mesg)\
   {\
   fprintf(stderr, "%s\n", Mesg);\
	fprintf(stderr,"image: %s\n", imerror());\
   exit(1);\
   }



/*page*/
MyMainReal(pixels,pixcnt)
int pixcnt;
REALTYPE *pixels;
{
	int i;
	REALTYPE *ppix;
	double beforesum, aftersum, normfac;

	/* set all negative pixels to zero*/
	if (ZeroNan){
		for(i=0; i< pixcnt; ++i){
			if (isnan(pixels[i]))
				pixels[i] = 0.0;
		}
	}
	beforesum = aftersum = 0.0;
	ppix = pixels;
	for(i=pixcnt; i > 0; --i, ppix++){
		beforesum += *ppix;
		if (*ppix < 0.0) *ppix = 0.0;
		aftersum += *ppix;
	}
	if (Normalize && aftersum != 0.0){
		normfac = beforesum/aftersum;
		fprintf(stderr,"normfac=%.4g\n",normfac);
		for(i=pixcnt, ppix = pixels; i > 0; --i, ppix++)
			*ppix *= normfac;
	}
}

MyMainGrey(pixels,pixcnt)
int pixcnt;
GREYTYPE *pixels;
{
	int i;
	GREYTYPE *ppix;
	double beforesum, aftersum, normfac;


	/* set all negative pixels to zero*/
	ppix = pixels;
	beforesum = aftersum = 0.0;
	for(i=pixcnt; i > 0; --i, ppix++){
		beforesum += *ppix;
		if (*ppix < 0.0) *ppix = 0;
		aftersum += *ppix;
	}
	if (Normalize && aftersum != 0.0){
		normfac = beforesum/aftersum;
		for(i=pixcnt, ppix = pixels; i > 0; --i, ppix++)
			*ppix *= normfac;
	}
}



/*page*/
/*---------------------------------------------------------------------------*/
/*                                                                           */
/* Purpose:  This is a basic image processing program.  It calls "MyMain"    */
/*           to handle the needs of the application.                         */
/*                                                                           */
/*---------------------------------------------------------------------------*/
main(argc, argv)
int	argc;
char	*argv[];
{
	char	*name1, *name2;
	char	newtitle[nTITLE];
	int	titleflag = FALSE;
	int	infoflag = FALSE;
/*
#ifndef WIN32
	HANDLE_BUILDINFO(zeroneg_buildinfo)
#endif
*/
	/* Interpret options */
	while (--argc > 0 && (*++argv)[0] == '-') {
		char	*s;
		for (s = argv[0] + 1; *s; s++)
			switch (*s) {
			case 'D':
				Debug = TRUE;
				break;
			case 'i':
				infoflag = TRUE;
				break;
			case 't':
				if (!*++argv || sscanf(*argv,"%s",newtitle)==0)
					Abort("Can not get title");
				titleflag = TRUE;
				argc--;
				break;
			case 'f':
				ZeroNan = TRUE;
				break;
			case 'n':
				Normalize = TRUE;
				break;
			default:
				fprintf (stderr, "Unknown option: -%c\n", *s);
				Abort ("");
				break;
			}
	}

	/* Print program title and version number */
	if (Debug) printf("zeroneg - Version 1.0\n\n");

	/* Check number of arguments */
	if (argc < 2) {
		fprintf(stderr,
		    "Usage: zeroneg [options] infile outfile\n\n");
		fprintf(stderr,
		    "       [-D]          Print debugging information\n");
		fprintf(stderr,
		    "       [-i]          Copy information fields\n");
		fprintf(stderr,
		    "       [-n ]  normalize image so sum before and after is same\n");
		fprintf(stderr,
		    "       [-t \"title\"]  Specify output image title\n");
		exit(1);
	}

	/* Get image file names from argument list */
	name1 = *argv;
	name2 = *++argv;
	if (name1 == NULL || name2 == NULL)
		 Abort("Error getting filenames");

	/* Open image file */
	if ((image1 = imopen(name1, READ)) == NULL)
		Abort("Can not open input image");
	if (imheader(image1, &pixformat, &pixsize, &pixcnt, &dimc, dimv,
	     maxmin) == INVALID)
		Abort("Can not get image information");

	/* Check pixel format */
	if (pixformat != GREY && pixformat != REAL)
		Abort("Image not of GREY or REAL type");

	/* Read in old image */
	pixel1 = (GREYTYPE *)malloc((unsigned)pixsize * pixcnt);
	if (pixel1 == NULL)
		Abort("Can not allocate pixels for input image");
	if (imread(image1, 0, pixcnt - 1, pixel1) == INVALID)
		Abort("Can not read pixels from input image");

	/* Create new image file */
	if ((image2 = imcreat(name2, DEFAULT, pixformat, dimc, dimv)) == INVALID)
		Abort("Can not create output image");

	/* Do application work */
	if (pixformat == GREY)
		MyMainGrey(pixel1, pixcnt);
	else
		MyMainReal(pixel1, pixcnt);

	/* Write out new image file */
	if (imwrite(image2, 0, pixcnt - 1, pixel1) == INVALID)
		Abort("Can not write pixels to output image\n");

	/* Update the values of minmax and histo for new image */
	if (pixformat == GREY){
		if (imgetdesc(image2, MINMAX, maxmin) == INVALID)
			Abort("Can not update maxmin field");
		if (imgetdesc(image2, HISTO, histo) == INVALID)
			Abort("Can not update histo field");
	}

	/* Copy info fields and title to new image */
	if (infoflag)
		if (imcopyinfo(image1, image2) == INVALID)
			Abort("Can not copy info fields");
	if (titleflag)
		if (imputtitle(image2, newtitle) == INVALID)
			Abort("Can not write title to new image");

	/* Close image files */
	imclose(image1);
	imclose(image2);
	exit(0);
}
