#pragma once
extern "C" {
    typedef struct LinkedList LinkedList;
    __declspec(dllexport) bool EmptyList(LinkedList* L);
    __declspec(dllexport) void InitializeLinkedList(LinkedList* L);
    __declspec(dllexport) void ClearLinkedList(LinkedList* L);
    __declspec(dllexport) void DeleteNode(LinkedList* L, int idx);
    __declspec(dllexport) void InsertNode(LinkedList* L, int k, int idx);
    __declspec(dllexport) const char* ReadAllElements(LinkedList* L);
    __declspec(dllexport) int ReadOneElement(LinkedList* L, int TargetIndex);
    __declspec(dllexport) void ReverseList(LinkedList* L);
}
