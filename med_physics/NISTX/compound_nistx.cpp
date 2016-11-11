// This program creates my custom ".nistx" data files using an input list and
// the info from the NIST website.
// This is for compounds only.

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
  std::vector<std::string> all_names;
  bool underscore, reading_mu;
  size_t pos;
  unsigned int Z;
  
  std::string nist_dir = "http://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/";
  
  // Load compound list
  std::vector<std::string> compound_list, compound_webpage;
  std::vector< std::vector<std::string> > compound_elements;
  fin.open("nist_compounds.txt");
  std::getline(fin, input);
  for(int n = 0; n < 48; n++){
    compound_list.push_back(input);
    std::getline(fin, input);
    compound_webpage.push_back(input);
    
    std::vector<std::string> materials;
    std::getline(fin, input);
    while(input.find(':') != std::string::npos){
      materials.push_back(input);
      std::getline(fin, input);
    }
    compound_elements.push_back(materials);
  }
  fin.close();
  
  for(int n = 0; n < compound_list.size(); n++){
    // Write first part of file using compound data
    input = compound_list[n];
    pos = input.find('\t');
    name = input.substr(0, pos-1); pos++;
    all_names.push_back(name);
    file_name = compound_webpage[n].substr(0, compound_webpage[n].length()-5) + ".nistx";
    fout.open(file_name.c_str());
    fout << "# " << file_name << "\n";
    fout << "# Attenuation data for (" << name << ") obtained directly from ";
    fout << "the NIST website\n\n";
    fout << "# Material Name\n" << name << "\n\n";
    //pos = input.find('\t', pos+1); pos++;
    fout << "# Z/A\n";
    fout << input.substr(pos, (input.find(' ', pos)-pos)) << "\n\n";
    pos = input.find('\t', pos+1); pos++;
    fout << "# Mean exitation energy (eV)\n";
    fout << input.substr(pos, (input.find(' ', pos)-pos)) << "\n\n";
    pos = input.find('\t', pos+1); pos++;
    fout << "# Density\n";
    fout << input.substr(pos) << "\n\n";
    fout << "# Material composition (Z: weight fraction)\n";
    
    for(int m = 0; m < compound_elements[n].size(); m++){
      fout << compound_elements[n][m] << '\n';
    }
    
    fout << "\n# Attenuation data\n";
    fout << "# Each row includes a photon energy, a mass attenuation ";
    fout << "coefficient, and a mass\n";
    fout << "# energy absorption coefficient\n";

    // Write attenuation coefficients from downloaded web page
    get_file_cmd = "wget -O mu.txt " + nist_dir + compound_webpage[n];
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
    mv_cmd = "mv " + file_name + " Compounds/";
    system(mv_cmd.c_str());
  }
  
  fout.open("CompoundList.txt");
  for(int n = 0; n < compound_list.size(); n++){
    file_name = compound_webpage[n].substr(0, compound_webpage[n].length()-5) + ".nistx";
    fout << all_names[n] << '\t' << file_name << '\n';
  }
  fout.close();
  
  return 0;
}
