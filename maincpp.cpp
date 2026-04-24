#include <iostream>
#include <string>
#include "modules.h"

using namespace std;

struct Node {
    int data;
    Node* next;
    Node* prev;
};

struct LinkedList {
    Node* head;
    Node* tail;
    int count;
};

bool EmptyList(LinkedList* L) {
    return L->head == nullptr;
}

void InitializeLinkedList(LinkedList* L) {
    L->head = nullptr;
    L->tail = nullptr;
    L->count = 0;
}

void ClearLinkedList(LinkedList* L) {
    if (EmptyList(L)) {
        cout << "Список пуст" << endl;
        return;
    }

    while (L->head != nullptr) {
        Node* n = L->head;
        L->head = n->next;
        delete n;
    }

    L->tail = nullptr;
    L->count = 0;
}

void DeleteNode(LinkedList* L, int idx) {
    if (EmptyList(L)) {
        cout << "Список пуст" << endl;
        return;
    }

    if (idx < 0 || idx >= L->count) {
        cout << "Некорректный индекс" << endl;
        return;
    }

    if (idx == 0) {
        Node* n = L->head;
        L->head = n->next;

        if (L->head != nullptr)
            L->head->prev = nullptr;
        else
            L->tail = nullptr;

        delete n;
        L->count--;
        return;
    }

    if (idx == L->count - 1) {
        Node* n = L->tail;
        L->tail = n->prev;

        if (L->tail != nullptr)
            L->tail->next = nullptr;
        else
            L->head = nullptr;

        delete n;
        L->count--;
        return;
    }

    Node* n = L->head;
    for (int i = 0; i < idx; i++)
        n = n->next;

    n->prev->next = n->next;
    n->next->prev = n->prev;

    delete n;
    L->count--;
}

void InsertNode(LinkedList* L, int k, int idx) {
    if (idx < 0 || idx > L->count) {
        cout << "Некорректный индекс" << endl;
        return;
    }

    Node* n = new Node;
    n->data = k;
    n->next = nullptr;
    n->prev = nullptr;

    if (L->count == 0) {
        L->head = n;
        L->tail = n;
        L->count = 1;
        return;
    }

    if (idx == 0) {
        n->next = L->head;
        L->head->prev = n;
        L->head = n;
        L->count++;
        return;
    }

    if (idx == L->count) {
        n->prev = L->tail;
        L->tail->next = n;
        L->tail = n;
        L->count++;
        return;
    }

    Node* m = L->head;
    for (int i = 0; i < idx; i++)
        m = m->next;

    n->next = m;
    n->prev = m->prev;
    m->prev->next = n;
    m->prev = n;
    L->count++;
}

const char* ReadAllElements(LinkedList* L) {
    static std::string res;
    res.clear();

    if (EmptyList(L)) {
        cout << "Список пуст, читать нечего" << endl;
        res = "Список пуст, читать нечего";
        return res.c_str();
    }

    Node* n = L->head;
    while (n != nullptr) {
        res += to_string(n->data) + " ";
        n = n->next;
    }

    res = res + "Количество элементов: " + to_string(L->count);
    return res.c_str();
}

int ReadOneElement(LinkedList* L, int TargetIndex) {
    if (EmptyList(L) || TargetIndex < 0 || TargetIndex >= L->count) {
        cout << "Список пуст или индекс некорректен" << endl;
        return 0;
    }

    Node* n = L->head;
    int count = 0;
    while (count < TargetIndex) {
        n = n->next;
        count++;
    }

    return n->data;
}

void ReverseList(LinkedList* L) {
    if (EmptyList(L) || L->count == 1) {
        cout << "Список пуст или содержит один элемент" << endl;
        return;
    }

    LinkedList tw;
    InitializeLinkedList(&tw);

    while (L->count != 0) {
        int k = ReadOneElement(L, L->count - 1);
        DeleteNode(L, L->count - 1);
        InsertNode(&tw, k, tw.count);
    }

    *L = tw;
}
