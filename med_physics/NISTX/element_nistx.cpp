// This program takes an input file and creates my custom ".nistx" data file.
// This is for elements only

#include <cstdlib>

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

int main(){
  std::ifstream fin;
  std::ofstream fout;
  std::string input, output, file_name, name, get_file_cmd, mv_cmd;
  bool underscore, reading_mu;
  size_t pos;
  unsigned int Z;
  
  std::string nist_dir = "http://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/";
  
  // Load element list
  std::vector<std::string> element_list;
  fin.open("nist_elements.txt");
  while(std::getline(fin, input)){
    element_list.push_back(input);
  }
  fin.close();
  
  for(int n = 0; n < element_list.size(); n++){
    // Write first part of file using element data
    input = element_list[n];
    pos = input.find('\t');
    file_num = input.substr(0, pos-1);
    std::stringstream(file_num) >> Z;
    while(file_num.length() < 2) file_num = '0' + file_num;
    for(int n = 0; n < 1; n++){ pos = input.find('\t', pos+1); } pos++;
    name = input.substr(pos, (input.find(' ', pos)-pos));
    file_name = file_num + '-' + name + ".nistx";
    fout.open(file_name.c_str());
    fout << "# " << file_name << "\n";
    fout << "# Attenuation data for (" << name << ") obtained directly from ";
    fout << "the NIST website\n\n";
    fout << "# Material Name\n" << name << "\n\n";
    for(int n = 0; n < 1; n++){ pos = input.find('\t', pos+1); } pos++;
    fout << "# Z/A\n";
    fout << input.substr(pos, (input.find(' ', pos)-pos)) << "\n\n";
    for(int n = 0; n < 1; n++){ pos = input.find('\t', pos+1); } pos++;
    fout << "# Mean excitation energy (eV)\n";
    fout << input.substr(pos, (input.find(' ', pos)-pos)) << "\n\n";
    for(int n = 0; n < 1; n++){ pos = input.find('\t', pos+1); } pos++;
    fout << "# Density\n";
    fout << input.substr(pos) << "\n\n";
    fout << "# Material composition (Z: weight fraction)\n";
    fout << Z << ": 1.0\n\n";
    fout << "# Attenuation data\n";
    fout << "# Each row includes a photon energy, a mass attenuation ";
    fout << "coefficient, and a mass\n";
    fout << "# energy absorption coefficient\n";

    // Write attenuation coefficients from downloaded web page
    get_file_cmd = "wget -O mu.txt " + nist_dir + 'z' + file_num + ".html";
    system(get_file_cmd.c_str());
    fin.open("mu.txt");
    reading_mu = false;
    underscore = false;
    while(std::getline(fin, input)) {
      if(input.find("_____________") != std::string::npos){
        if(!underscore) underscore = true;
        else {
          reading_mu = true;
          std::getline(fin,input);
          continue;
        }
      }
      if(input == "</PRE></TD>" && reading_mu) reading_mu = false;
      if(reading_mu){
        while(*input.begin() == ' ') input.erase(input.begin());
        fout << input << '\n';
      }
    }
    fin.close();
    fout.close();
    
    // Move file to elements directory
    mv_cmd = "mv " + file_name + " Elements/";
    system(mv_cmd.c_str());
  }

  return 0;
}
