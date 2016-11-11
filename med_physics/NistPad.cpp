////////////////////////////////////////////////////////////////////////////////
//                                                                            //
// NistPad.cpp                                                                //
// NIST Photon Attenuation Data (NISTPAD) Manager Class                       //
// Version 1.0                                                                //
//                                                                            //
// Steven Dolly                                                               //
// October 9, 2015                                                            //
//                                                                            //
// This is the main file for the class which loads and stores photon          //
// attenuation data from NIST. Data from any point on the table is accessed   //
// using logarithmic interpolation.                                           //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////

// Class header (make sure file path is correct!)
#include "NistPad.hpp"

// Standard C++ headers
#include <iostream>
#include <fstream>
#include <sstream>

// Custom headers (make sure file path is correct!)
#include "DataInterpolation.hpp"

// Default constructor
NistPad::NistPad(){

}

// Default destructor
NistPad::~NistPad(){

}

// Constructor tht automatically loads data file 
NistPad::NistPad(std::string file_name){
  Load(file_name);
}

// Data loading function
bool NistPad::Load(std::string file_name){
  std::ifstream fin;
  std::string line, str;
  bool reading_elements = true;
  size_t pos;
  unsigned int z, counter;
  double input;
  
  fin.open(file_name.c_str());
  
  // Read in material information from header
  for(int n = 0; n < 5; n++) std::getline(fin, line);
  name = line;
  
  for(int n = 0; n < 3; n++) std::getline(fin, line);
  std::stringstream(line) >> z_to_a_ratio;
  
  for(int n = 0; n < 3; n++) std::getline(fin, line);
  std::stringstream(line) >> mean_exitation_energy;
  
  for(int n = 0; n < 3; n++) std::getline(fin, line);
  line[5] = 'e';
  std::stringstream(line) >> density;
  
  for(int n = 0; n < 2; n++) std::getline(fin, line);
  while(reading_elements){
    std::getline(fin, line);
    if(line.empty()){
      reading_elements = false;
    }
    else {
      pos = line.find(':');
      std::stringstream(line.substr(0, pos)) >> z;
      atomic_number.push_back(z);
      std::stringstream(line.substr(pos+1)) >> input;
      weight_fraction.push_back(input);
    }
  }
  num_elements = atomic_number.size();
  if(num_elements == 1) is_element = true;
  else is_element = false;
  
  // Read in attenuation data
  counter = 0;
  for(int n = 0; n < 3; n++) std::getline(fin, line);
  while(std::getline(fin, line)){
    if(line[1] != '.') absorption_edges.push_back(counter);
    
    pos = line.find('.'); pos--;
    line[(pos+7)] = line[(pos+18)] = line[(pos+29)] = 'e';
    
    str = line.substr(pos, 12);
    std::stringstream(str) >> input;
    energies.push_back(input);
    
    str = line.substr((pos+12), 11);
    std::stringstream(str) >> input;
    mass_attenuation.push_back(input);
    
    str = line.substr(pos+23);
    std::stringstream(str) >> input;
    mass_energy_absorption.push_back(input);
    
    counter++;
  }
  
  fin.close();
  
  return true;
}

// Get values from data using log interpolation
double NistPad::MassAttenuation(double energy){
  return (LogInterpolation1D(energies, mass_attenuation, energy));
}
double NistPad::LinearAttenuation(double energy){
  return (density*LogInterpolation1D(energies, mass_attenuation, energy));
}
double NistPad::MassAbsorption(double energy){
  return (LogInterpolation1D(energies, mass_energy_absorption, energy));
}
double NistPad::LinearAbsorption(double energy){
  return (density*LogInterpolation1D(energies, mass_energy_absorption, energy));
}

// Print data to terminal screen
void NistPad::PrintData(){
  std::cout << name << '\n';
  
  if(is_element) std::cout << "This is an element.\n\n";
  else  std::cout << "This is not an element.\n\n";
  
  std::cout << "Z/A = " << z_to_a_ratio << '\n';
  std::cout << "I (eV) = " << mean_exitation_energy << '\n';
  std::cout << "Density (g/cm^3) = " << density << "\n\n";
  
  std::cout << "Elements by Weight\n";
  std::cout << "------------------\n";
  for(int n = 0; n < num_elements; n++){
    std::cout << atomic_number[n] << " : " << weight_fraction[n] << '\n';
  }
  std::cout << '\n';
  
  std::cout << "Attenuation Data\n";
  std::cout << "----------------\n";
  for(int n = 0; n < energies.size(); n++){
    std::cout << energies[n] << '\t' << mass_attenuation[n] << '\t' <<
        mass_energy_absorption[n] << '\n';
  }
  std::cout << '\n';
  
  std::cout << "Absorption Edges\n";
  std::cout << "----------------\n";
  for(int n = 0; n < absorption_edges.size(); n++){
    std::cout << energies[(absorption_edges[n])] << '\t' <<
        mass_attenuation[(absorption_edges[n])] << '\t' <<
        mass_energy_absorption[(absorption_edges[n])] << '\n';
  }
}
