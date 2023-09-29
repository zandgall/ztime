#include "TimeDoc.h"
#include <fstream>
#include <iostream>

#ifdef WIN32
#define DOC_PATH "time.xml"
#else
#define DOC_PATH "/home/zandgall/time.xml"
#endif

TimeDoc::TimeDoc() {    
    std::ifstream input(DOC_PATH);
    if(!input.good()) {
        input.close();
        std::ofstream creation(DOC_PATH);
        creation << "<data><types></types><entries next_id=\"0\"></entries><current></current></data>";
        creation.close();
        input = std::ifstream(DOC_PATH);
    }
    std::vector<char> buffer((std::istreambuf_iterator<char>(input)), std::istreambuf_iterator<char>());
    buffer.push_back('\0');
    doc.parse<0>(&buffer[0]);
    root_node = doc.first_node();
    types_node = root_node->first_node("types");
    entries_node = root_node->first_node("entries");
    current_node = root_node->first_node("current");
    
    std::map<char, int> conv = {{'0', 0}, {'1',1}, {'2',2}, {'3',3},{'4',4}, {'5',5}, {'6',6},{'7',7}, {'8',8}, {'9',9},{'a',10},{'b',11},{'c',12},{'d',13},{'e',14},{'f',15}};
    int layer = 0;
    for (xml_node<>* type = types_node->first_node(); type; type = type->next_sibling()) {
        std::string str_color(type->first_attribute()->value());
        int r = conv[str_color[1]]*16 + conv[str_color[2]];
        int g = conv[str_color[3]]*16 + conv[str_color[4]];
        int b = conv[str_color[5]]*16 + conv[str_color[6]];
        types[std::string(type->name())] = glm::vec3(r / 255.f, g / 255.f, b / 255.f);
        type_layers[std::string(type->name())] = layer;
        layer++;
    }
    
    for (xml_node<>* entry = entries_node->first_node(); entry; entry = entry->next_sibling())
        entries.push_back(
            {
                entry->name(), 
                std::strtoul(entry->first_attribute("id")->value(), nullptr, 10),
                std::strtoull(entry->first_attribute("begin")->value(), nullptr, 10),
                std::strtoull(entry->first_attribute("end")->value(), nullptr, 10)
            }
        );
    
    for (xml_node<>* cur = current_node->first_node(); cur; cur = cur->next_sibling())
        current[cur->name()] = std::strtoull(cur->first_attribute("begin")->value(), nullptr, 10);
}