////////////////////////////////////////////////////////////////////////////////
//                                                                            //
// DataInterpolation.hpp                                                      //
// Data interpolation math header file                                        //
// Version 1.0                                                                //
//                                                                            //
// Steven Dolly                                                               //
// January 31, 2016                                                           //
//                                                                            //
// This is the header file for the template functions that assist in data     //
// interpolation for tabular values.                                          //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////

// Header guard
#ifndef DATAINTERPOLATION_HPP
#define DATAINTERPOLATION_HPP

// Standard C header
#include <cmath>

// Stardard C++ headers
#include <string>
#include <vector>

template <class T>
T LinearInterpolation1D(std::vector<T> data_x, std::vector<T> data_y,
    T value_x){
  unsigned int index = 0;
  
  while((data_x[index] <= value_x) && (index < data_x.size())) index++;
  index--;
  
  double f = (value_x - data_x[index]) /
      (data_x[(index+1)] - data_x[index]);
  T value_y = f*data_y[(index+1)] + (1-f)*data_y[index];
  
  return value_y;
}

template <class T>
T LogInterpolation1D(std::vector<T> data_x, std::vector<T> data_y, T value_x){
  unsigned int index = 0;
  
  while((data_x[index] <= value_x) && (index < data_x.size())) index++;
  index--;
  
  double f = (log10(value_x) - log10(data_x[index])) /
      (log10(data_x[(index+1)]) - log10(data_x[index]));
  T value_y = (pow(data_y[(index+1)], f) * pow(data_y[index],(1-f)));
  
  return value_y;
}
      
#endif
