#include <pybind11/pybind11.h>
#include <list>
#include <string>
#include <iterator>

namespace py = pybind11;
using namespace std;

struct LinkedList {
    list<int> data;

    int count() const {
        return static_cast<int>(data.size());
    }
};

bool EmptyList(const LinkedList& L) {
    return L.data.empty();
}

LinkedList InitializeLinkedList() {
    return LinkedList();
}

void ClearLinkedList(LinkedList& L) {
    L.data.clear();
}

void InsertNode(LinkedList& L, int value, int idx) {
    if (idx < 0 || idx > static_cast<int>(L.data.size())) {
        return;
    }

    auto it = L.data.begin();
    advance(it, idx);
    L.data.insert(it, value);
}

void DeleteNode(LinkedList& L, int idx) {
    if (L.data.empty()) {
        return;
    }

    if (idx < 0 || idx >= static_cast<int>(L.data.size())) {
        return;
    }

    auto it = L.data.begin();
    advance(it, idx);
    L.data.erase(it);
}

string ReadAllElements(const LinkedList& L) {
    if (L.data.empty()) {
        return "Список пуст, читать нечего";
    }

    string res;

    for (int x : L.data) {
        res += to_string(x) + " ";
    }

    res += "Количество элементов: " + to_string(L.data.size());
    return res;
}

int ReadOneElement(const LinkedList& L, int idx) {
    if (L.data.empty() || idx < 0 || idx >= static_cast<int>(L.data.size())) {
        throw py::value_error("Список пуст или индекс не корректен");
    }

    auto it = L.data.begin();
    advance(it, idx);
    return *it;
}

void ReverseList(LinkedList& L) {
    if (L.data.size() <= 1) {
        return;
    }

    L.data.reverse();
}

PYBIND11_MODULE(stlmodule, m) {
    m.doc() = "STL linked lis";

    py::class_<LinkedList>(m, "LinkedList")
        .def(py::init<>())
        .def_property_readonly("count", &LinkedList::count);

    m.def("EmptyList", &EmptyList);
    m.def("InitializeLinkedList", &InitializeLinkedList);
    m.def("ClearLinkedList", &ClearLinkedList);
    m.def("DeleteNode", &DeleteNode);
    m.def("InsertNode", &InsertNode);
    m.def("ReadAllElements", &ReadAllElements);
    m.def("ReadOneElement", &ReadOneElement);
    m.def("ReverseList", &ReverseList);
}
