from ctypes import *
import os
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import module as py_module

try:
    import stlmodule as stl_module
except ImportError:
    stl_module = None


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CPP_DLL_PATH = os.path.join(BASE_DIR, "mylib.dll")


class CppNode(Structure):
    pass


CppNode._fields_ = [
    ("data", c_int),
    ("next", POINTER(CppNode)),
    ("prev", POINTER(CppNode)),
]


class CppLinkedList(Structure):
    _fields_ = [
        ("head", POINTER(CppNode)),
        ("tail", POINTER(CppNode)),
        ("count", c_int),
    ]


class Python:
    name = "Python"

    def __init__(self):
        self.linked_list = py_module.InitializeLinkedList()

    @property
    def count(self):
        return self.linked_list.count

    def EmptyList(self):
        return py_module.EmptyList(self.linked_list)

    def InitializeLinkedList(self):
        self.linked_list = py_module.InitializeLinkedList()

    def ClearLinkedList(self):
        py_module.ClearLinkedList(self.linked_list)

    def DeleteNode(self, idx):
        py_module.DeleteNode(self.linked_list, idx)

    def InsertNode(self, value, idx):
        py_module.InsertNode(self.linked_list, value, idx)

    def ReadAllElements(self):
        return py_module.ReadAllElements(self.linked_list)

    def ReadOneElement(self, idx):
        return py_module.ReadOneElement(self.linked_list, idx)

    def ReverseList(self):
        py_module.ReverseList(self.linked_list)


class Cpp:
    name = "C++"

    def __init__(self, dll_path):
        self.lib = CDLL(dll_path)
        self._configure()
        self.linked_list = CppLinkedList()
        self.InitializeLinkedList()

    def _configure(self):
        self.lib.EmptyList.argtypes = [POINTER(CppLinkedList)]
        self.lib.EmptyList.restype = c_bool

        self.lib.InitializeLinkedList.argtypes = [POINTER(CppLinkedList)]
        self.lib.InitializeLinkedList.restype = None

        self.lib.ClearLinkedList.argtypes = [POINTER(CppLinkedList)]
        self.lib.ClearLinkedList.restype = None

        self.lib.DeleteNode.argtypes = [POINTER(CppLinkedList), c_int]
        self.lib.DeleteNode.restype = None

        self.lib.InsertNode.argtypes = [POINTER(CppLinkedList), c_int, c_int]
        self.lib.InsertNode.restype = None

        self.lib.ReadAllElements.argtypes = [POINTER(CppLinkedList)]
        self.lib.ReadAllElements.restype = c_char_p

        self.lib.ReadOneElement.argtypes = [POINTER(CppLinkedList), c_int]
        self.lib.ReadOneElement.restype = c_int

        self.lib.ReverseList.argtypes = [POINTER(CppLinkedList)]
        self.lib.ReverseList.restype = None

    @property
    def count(self):
        return self.linked_list.count

    def EmptyList(self):
        return self.lib.EmptyList(byref(self.linked_list))

    def InitializeLinkedList(self):
        self.lib.InitializeLinkedList(byref(self.linked_list))

    def ClearLinkedList(self):
        self.lib.ClearLinkedList(byref(self.linked_list))

    def DeleteNode(self, idx):
        self.lib.DeleteNode(byref(self.linked_list), idx)

    def InsertNode(self, value, idx):
        self.lib.InsertNode(byref(self.linked_list), value, idx)

    def ReadAllElements(self):
        return self.lib.ReadAllElements(byref(self.linked_list)).decode("utf-8")

    def ReadOneElement(self, idx):
        if self.EmptyList() or idx < 0 or idx >= self.count:
            raise ValueError("Список пуст или индекс не корректен")
        return self.lib.ReadOneElement(byref(self.linked_list), idx)

    def ReverseList(self):
        self.lib.ReverseList(byref(self.linked_list))


class Stl:
    name = "STL"

    def __init__(self):
        if stl_module is None:
            raise ImportError("pybind11-модуль stlmodule не найден")
        self.module = stl_module
        self.linked_list = self.module.InitializeLinkedList()

    @property
    def count(self):
        return getattr(self.linked_list, "count", 0)

    def EmptyList(self):
        return self.module.EmptyList(self.linked_list)

    def InitializeLinkedList(self):
        self.linked_list = self.module.InitializeLinkedList()

    def ClearLinkedList(self):
        self.module.ClearLinkedList(self.linked_list)

    def DeleteNode(self, idx):
        self.module.DeleteNode(self.linked_list, idx)

    def InsertNode(self, value, idx):
        self.module.InsertNode(self.linked_list, value, idx)

    def ReadAllElements(self):
        return self.module.ReadAllElements(self.linked_list)

    def ReadOneElement(self, idx):
        if self.EmptyList() or idx < 0 or idx >= self.count:
            raise ValueError("Список пуст или индекс не корректен")
        return self.module.ReadOneElement(self.linked_list, idx)

    def ReverseList(self):
        self.module.ReverseList(self.linked_list)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Двусвязный список")
        self.root.geometry("900x620")

        self.modules = {"Python": Python()}
        self.missing = []

        try:
            self.modules["C++"] = Cpp(CPP_DLL_PATH)
        except Exception as e:
            self.missing.append(f"C++ (нет mylib.dll или библиотека не загрузилась: {e})")

        try:
            self.modules["STL"] = Stl()
        except Exception as e:
            self.missing.append(f"STL (pybind11-модуль не загрузился: {e})")

        self.name = tk.StringVar(value=list(self.modules.keys())[0])
        self._build_ui()
        self.log("Программа запущена")
        if self.missing:
            for item in self.missing:
                self.log(item)

    def _build_ui(self):
        tk.Label(self.root, text="Выберите библиотеку", font=("Arial", 11)).pack(pady=(12, 2))

        self.combo = ttk.Combobox(
            self.root,
            textvariable=self.name,
            values=list(self.modules.keys()),
            state="readonly",
            width=20,
        )
        self.combo.pack()
        self.combo.bind("<<ComboboxSelected>>", self.on_module_change)

        tk.Label(self.root, text="Введите значение", font=("Arial", 11)).pack(pady=(12, 2))
        self.entry_value = tk.Entry(self.root, width=30)
        self.entry_value.pack()

        tk.Label(self.root, text="Введите индекс", font=("Arial", 11)).pack(pady=(10, 2))
        self.entry_index = tk.Entry(self.root, width=30)
        self.entry_index.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=18)

        buttons = [
            ("InitializeLinkedList", self.initialize_list),
            ("EmptyList", self.empty_list),
            ("InsertNode", self.insert_node),
            ("DeleteNode", self.delete_node),
            ("ReadAllElements", self.read_all),
            ("ReadOneElement", self.read_one),
            ("ReverseList", self.reverse_list),
            ("ClearLinkedList", self.clear_list),
        ]

        for idx, (text, command) in enumerate(buttons):
            row = idx // 4
            col = idx % 4
            tk.Button(button_frame, text=text, width=18, command=command).grid(
                row=row, column=col, padx=8, pady=8
            )

        self.output = ScrolledText(self.root, width=100, height=20)
        self.output.pack(padx=20, pady=10)

    def get_module(self):
        return self.modules[self.name.get()]

    def on_module_change(self, _event=None):
        self.log(f"Выбрана библиотека: {self.name.get()}")

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def get_index_value(self, default=None):
        raw = self.entry_index.get().strip()
        
        if raw == "":
            if default is None:
                raise ValueError("Индекс не введен")
            return default
        return int(raw)

    def get_node_value(self):
        raw = self.entry_value.get().strip()
        if raw == "":
            raise ValueError("Значение не введено")
        return int(raw)

    def clear_entries(self):
        self.entry_value.delete(0, tk.END)
        self.entry_index.delete(0, tk.END)

    def initialize_list(self):
        module = self.get_module()
        module.InitializeLinkedList()
        self.log(f"[{module.name}] InitializeLinkedList выполнена")

    def empty_list(self):
        module = self.get_module()
        result = module.EmptyList()
        self.log(f"[{module.name}] EmptyList -> {result}")

    def insert_node(self):
        module = self.get_module()
        try:
            value = self.get_node_value()
            index = self.get_index_value(default=module.count)
            module.InsertNode(value, index)
            self.log(f"[{module.name}] InsertNode({value}, {index}) выполнена")
            #self.clear_entries()
        except Exception as e:
            self.log(f"Ошибка: {e}")

    def delete_node(self):
        module = self.get_module()
        try:
            index = self.get_index_value(default=module.count - 1)
            module.DeleteNode(index)
            self.log(f"[{module.name}] DeleteNode({index}) выполнена")
            self.entry_index.delete(0, tk.END)
        except Exception as e:
            self.log(f"Ошибка: {e}")

    def read_all(self):
        module = self.get_module()
        try:
            result = module.ReadAllElements()
            self.log(f"[{module.name}] {result}")
        except Exception as e:
            self.log(f"Ошибка: {e}")

    def read_one(self):
        module = self.get_module()
        try:
            index = self.get_index_value()
            result = module.ReadOneElement(index)
            self.log(f"[{module.name}] Элемент по индексу {index}: {result}")
        except Exception as e:
            self.log(f"Ошибка: {e}")

    def reverse_list(self):
        module = self.get_module()
        try:
            module.ReverseList()
            self.log(f"[{module.name}] ReverseList выполнена")
        except Exception as e:
            self.log(f"Ошибка: {e}")

    def clear_list(self):
        module = self.get_module()
        try:
            module.ClearLinkedList()
            self.log(f"[{module.name}] ClearLinkedList выполнена")
        except Exception as e:
            self.log(f"Ошибка: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()