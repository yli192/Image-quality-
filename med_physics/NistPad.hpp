////////////////////////////////////////////////////////////////////////////////
//                                                                            //
// NistPad.hpp                                                                //
// NIST Photon Attenuation Data (NISTPAD) Manager Class                       //
// Version 1.0                                                                //
//                                                                            //
// Steven Dolly                                                               //
// October 9, 2015                                                            //
//                                                                            //
// This file contains the header for the class which loads and stores photon  //
// attenuation data from NIST. Data from any point on the table is accessed   //
// using logarithmic interpolation.                                           //
//                                                                            //
////////////////////////////////////////////////////////////////////////////////

#ifndef NISTPAD_HPP
#define NISTPAD_HPP

#include <string>
#include <vector>

class NistPad {
  public:
    // Default constructor and destructor
    NistPad();
    ~NistPad();
    // Constructor that automatically loads data if file name is given
    NistPad(std::string file_name);
    // Get and set functions
    std::string get_name(){ return name;}
    // File loading function (returns true if successful)
    bool Load(std::string file_name);
    // Get values from data using log interpolation
    double MassAttenuation(double energy);
    double LinearAttenuation(double energy);
    double MassAbsorption(double energy);
    double LinearAbsorption(double energy);
    // Prints all data to screen
    void PrintData();
  private:
    std::string name;
    unsigned int num_elements;
    bool is_element;
    std::vector<unsigned int> atomic_number;
    std::vector<double> weight_fraction;
    double z_to_a_ratio;
    double mean_exitation_energy;
    double density;
    
    std::vector<double> energies;
    std::vector<double> mass_attenuation;
    std::vector<double> mass_energy_absorption;
    
    std::vector<unsigned int> absorption_edges;
};

#endif
