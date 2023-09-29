#include <glm/glm.hpp>
#include <rapidxml.hpp>
#include <vector>
#include <map>
#include <string>
using namespace rapidxml;

struct entry {
    std::string type;
    size_t id;
    unsigned long long begin, end;
};

class TimeDoc {
public:
    std::map<std::string, glm::vec3> types;
    std::map<std::string, size_t> type_layers;
    std::vector<entry> entries;
    std::map<std::string, unsigned long long> current;
    TimeDoc();

private:
    xml_document<> doc;
    xml_node<> * root_node = nullptr, 
                *types_node = nullptr, 
                *entries_node = nullptr, 
                *current_node = nullptr;
};