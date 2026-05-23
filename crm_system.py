import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from datetime import datetime


class Person(ABC):
    """
    Абстрактный базовый класс, представляющий человека в системе.
    
    Служит основой для классов сотрудников и покупателей.
    Обеспечивает инкапсуляцию базовых данных (ID и имя).
    """
    
    def __init__(self, person_id: int, name: str):
        """
        Инициализирует базовые атрибуты человека.
        
        Args:
            person_id (int): Уникальный идентификатор.
            name (str): Имя и фамилия.
        """
        self._id = person_id
        self._name = name

    @property
    def id(self) -> int:
        """int: Возвращает идентификатор человека."""
        return self._id

    @property
    def name(self) -> str:
        """str: Возвращает имя человека."""
        return self._name

    @abstractmethod
    def get_role(self) -> str:
        """
        Возвращает текстовое описание роли человека.
        
        Returns:
            str: Роль в системе (например, "Покупатель" или "Сотрудник").
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует объект в словарь для последующего сохранения в JSON.
        
        Returns:
            Dict[str, Any]: Словарь с данными объекта.
        """
        return {"id": self._id, "name": self._name}


class Location(ABC):
    """
    Абстрактный базовый класс для физических локаций компании.
    
    Объединяет общие свойства складов и пунктов продаж (адрес, инвентарь, руководитель).
    """
    
    def __init__(self, loc_id: int, address: str, manager_id: Optional[int] = None):
        """
        Инициализирует базовые атрибуты локации.
        
        Args:
            loc_id (int): Уникальный идентификатор локации.
            address (str): Физический адрес.
            manager_id (Optional[int]): ID сотрудника, назначенного руководителем.
        """
        self._id = loc_id
        self._address = address
        self._manager_id = manager_id
        self._inventory: Dict[int, int] = {}  

    @property
    def id(self) -> int:
        """int: Возвращает идентификатор локации."""
        return self._id
    
    @property
    def address(self) -> str:
        """str: Возвращает адрес локации."""
        return self._address

    @property
    def manager_id(self) -> Optional[int]:
        """Optional[int]: Возвращает ID руководителя локации."""
        return self._manager_id

    def set_manager(self, manager_id: int):
        """
        Назначает нового руководителя локации.
        
        Args:
            manager_id (int): Уникальный идентификатор сотрудника.
        """
        self._manager_id = manager_id

    @abstractmethod
    def get_info(self) -> str:
        """
        Возвращает краткую информацию о локации.
        
        Returns:
            str: Форматированная строка с данными.
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Сериализует объект локации в словарь.
        
        Returns:
            Dict[str, Any]: Словарь с данными локации и ее инвентарем.
        """
        return {
            "id": self._id, 
            "address": self._address, 
            "manager_id": self._manager_id,
            "inventory": self._inventory
        }


class Product:
    """Класс, описывающий товарную позицию в каталоге системы."""
    
    def __init__(self, prod_id: int, name: str, purchase_price: float, sell_price: float):
        """
        Инициализирует карточку товара.
        
        Args:
            prod_id (int): Уникальный артикул/ID товара.
            name (str): Название товара.
            purchase_price (float): Цена закупки у поставщика.
            sell_price (float): Розничная цена продажи.
        """
        self.id = prod_id
        self.name = name
        self.purchase_price = purchase_price
        self.sell_price = sell_price

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует данные товара в словарь для сериализации."""
        return {
            "id": self.id, 
            "name": self.name, 
            "purchase_price": self.purchase_price, 
            "sell_price": self.sell_price
        }


class Employee(Person):
    """Класс сотрудника компании. Наследует базовые атрибуты от Person."""
    
    def __init__(self, person_id: int, name: str, position: str):
        """
        Инициализирует профиль сотрудника.
        
        Args:
            person_id (int): ID сотрудника.
            name (str): Имя сотрудника.
            position (str): Занимаемая должность.
        """
        super().__init__(person_id, name)
        self.position = position

    def get_role(self) -> str:
        """Возвращает строку с указанием должности сотрудника."""
        return f"Сотрудник ({self.position})"
        
    def to_dict(self) -> Dict[str, Any]:
        """Добавляет поле должности к базовому словарю сериализации Person."""
        data = super().to_dict()
        data["position"] = self.position
        return data


class Customer(Person):
    """Класс покупателя (клиента). Наследует базовые атрибуты от Person."""
    
    def __init__(self, person_id: int, name: str):
        """
        Инициализирует профиль клиента.
        
        Args:
            person_id (int): ID клиента.
            name (str): Имя клиента.
        """
        super().__init__(person_id, name)
        self.purchase_history: List[int] = []

    def get_role(self) -> str:
        """Возвращает фиксированную роль 'Покупатель'."""
        return "Покупатель"


class WarehouseCell:
    """Класс, представляющий отдельную ячейку хранения на складе."""
    
    def __init__(self, cell_id: str, capacity: int):
        """
        Инициализирует ячейку.
        
        Args:
            cell_id (str): Внутренний номер ячейки (например, 'A-12').
            capacity (int): Максимальная вместимость ячейки в единицах.
        """
        self.cell_id = cell_id
        self.capacity = capacity
        self.product_id: Optional[int] = None
        self.quantity: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Сериализует состояние ячейки в словарь."""
        return {
            "cell_id": self.cell_id, 
            "capacity": self.capacity, 
            "product_id": self.product_id, 
            "quantity": self.quantity
        }


class Warehouse(Location):
    """Класс центрального склада. Наследует функционал локации."""
    
    def __init__(self, loc_id: int, address: str, manager_id: Optional[int] = None):
        """Инициализирует склад и пустой список ячеек хранения."""
        super().__init__(loc_id, address, manager_id)
        self.cells: List[WarehouseCell] = []

    def get_info(self) -> str:
        """Возвращает сводную строку с ID, адресом и количеством ячеек склада."""
        return f"[Склад ID: {self.id}] Адрес: {self.address}, Ячеек: {len(self.cells)}"

    def to_dict(self) -> Dict[str, Any]:
        """Сериализует склад и все его ячейки в словарь."""
        data = super().to_dict()
        data["cells"] = [cell.to_dict() for cell in self.cells]
        return data


class PointOfSale(Location):
    """Класс розничного пункта продаж (магазина). Наследует функционал локации."""
    
    def __init__(self, loc_id: int, address: str, manager_id: Optional[int] = None):
        """Инициализирует пункт продаж и обнуляет финансовые показатели."""
        super().__init__(loc_id, address, manager_id)
        self.revenue: float = 0.0
        self.expenses: float = 0.0

    def get_info(self) -> str:
        """Возвращает сводную строку с финансовыми показателями точки."""
        return f"[Пункт продаж ID: {self.id}] Адрес: {self.address}, Доход: {self.revenue}, Расход: {self.expenses}"

    def to_dict(self) -> Dict[str, Any]:
        """Добавляет финансовые показатели к базовой сериализации локации."""
        data = super().to_dict()
        data.update({"revenue": self.revenue, "expenses": self.expenses})
        return data


class Order:
    """Класс заказа (транзакции), фиксирующий факт продажи."""
    
    def __init__(self, order_id: int, customer_id: int, pos_id: int, product_id: int, quantity: int, total: float):
        """
        Инициализирует запись о заказе.
        
        Args:
            order_id (int): Уникальный номер чека/заказа.
            customer_id (int): ID покупателя.
            pos_id (int): ID пункта продаж, где совершена операция.
            product_id (int): ID проданного товара.
            quantity (int): Количество проданного товара.
            total (float): Итоговая сумма заказа.
        """
        self.order_id = order_id
        self.customer_id = customer_id
        self.pos_id = pos_id
        self.product_id = product_id
        self.quantity = quantity
        self.total = total
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует заказ в словарь, включая автоматически сгенерированную дату."""
        return vars(self)


class CRMSystem:
    """
    Главный управляющий класс.
    Хранит все бизнес-объекты, управляет балансом компании и обрабатывает команды пользователя.
    """
    
    def __init__(self, data_file: str = "crm_data.json"):
        """
        Инициализирует пустые реестры и загружает данные из файла, если он существует.
        
        Args:
            data_file (str): Путь к JSON-файлу базы данных.
        """
        self.data_file = data_file
        self.products: Dict[int, Product] = {}
        self.employees: Dict[int, Employee] = {}
        self.customers: Dict[int, Customer] = {}
        self.warehouses: Dict[int, Warehouse] = {}
        self.points_of_sale: Dict[int, PointOfSale] = {}
        self.orders: Dict[int, Order] = {}
        
        self.company_balance: float = 100000.0 
        
        self.load_data()

    def save_data(self):
        """
        Агрегирует данные всех реестров и сохраняет их в указанный JSON-файл.
        """
        data = {
            "balance": self.company_balance,
            "products": {k: v.to_dict() for k, v in self.products.items()},
            "employees": {k: v.to_dict() for k, v in self.employees.items()},
            "warehouses": {k: v.to_dict() for k, v in self.warehouses.items()},
            "points_of_sale": {k: v.to_dict() for k, v in self.points_of_sale.items()},
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Данные успешно сохранены.")

    def load_data(self):
        """
        Читает JSON-файл базы данных и восстанавливает все объекты системы в памяти.
        Если файл отсутствует, оставляет систему с начальными пустыми параметрами.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.company_balance = data.get("balance", 100000.0)
            
            for pid, pdata in data.get("products", {}).items():
                self.products[int(pid)] = Product(**pdata)
                
            for eid, edata in data.get("employees", {}).items():
                self.employees[int(eid)] = Employee(
                    person_id=edata['id'], 
                    name=edata['name'], 
                    position=edata['position']
                )
                
            for loc_id, loc_data in data.get("points_of_sale", {}).items():
                pos = PointOfSale(loc_data['id'], loc_data['address'], loc_data.get('manager_id'))
                pos.revenue = loc_data.get('revenue', 0.0)
                pos.expenses = loc_data.get('expenses', 0.0)
                
                raw_inventory = loc_data.get('inventory', {})
                pos._inventory = {int(k): v for k, v in raw_inventory.items()}
                
                self.points_of_sale[int(loc_id)] = pos
        else:
            print("Файл данных не найден. Создана новая пустая база.")

    def hire_employee(self):
        """Интерактивный метод найма сотрудника с запросом данных через консоль."""
        eid = len(self.employees) + 1
        name = input("Имя сотрудника: ")
        pos = input("Должность: ")
        self.employees[eid] = Employee(eid, name, pos)
        print(f"Сотрудник {name} нанят! (ID: {eid})")

    def fire_employee(self):
        """Интерактивный метод увольнения (удаления из реестра) сотрудника по ID."""
        eid = int(input("Введите ID сотрудника для увольнения: "))
        if eid in self.employees:
            name = self.employees.pop(eid).name
            print(f"Сотрудник {name} уволен.")
        else:
            print("Сотрудник не найден.")

    def open_point_of_sale(self):
        """Создает новый филиал (пункт продаж) и добавляет его в реестр."""
        loc_id = len(self.points_of_sale) + 1
        address = input("Введите адрес нового пункта продаж: ")
        self.points_of_sale[loc_id] = PointOfSale(loc_id, address)
        print(f"Пункт продаж открыт! (ID: {loc_id})")

    def add_product_catalog(self):
        """Создает новую номенклатурную карточку товара и добавляет ее в глобальный каталог."""
        pid = len(self.products) + 1
        name = input("Название товара: ")
        buy_price = float(input("Закупочная цена: "))
        sell_price = float(input("Цена продажи: "))
        self.products[pid] = Product(pid, name, buy_price, sell_price)
        print(f"Товар добавлен в каталог. (ID: {pid})")

    def purchase_inventory(self):
        """
        Обрабатывает бизнес-логику закупки товара.
        Уменьшает баланс компании, увеличивает расходы пункта продаж 
        и добавляет указанное количество товара в его инвентарь.
        """
        print("Доступные товары для закупки:")
        for p in self.products.values():
            print(f"ID: {p.id} | {p.name} | Закупка: {p.purchase_price}")
        
        pid = int(input("ID товара для закупки: "))
        
        if pid in self.products:
            qty = int(input("Количество: "))
            pos_id = int(input("ID пункта продаж для поставки: "))
            
            if pos_id in self.points_of_sale:
                cost = self.products[pid].purchase_price * qty
                if self.company_balance >= cost:
                    self.company_balance -= cost
                    self.points_of_sale[pos_id].expenses += cost
                    
                    inv = self.points_of_sale[pos_id]._inventory
                    inv[pid] = inv.get(pid, 0) + qty
                    
                    print(f"Успешно закуплено {qty} ед. {self.products[pid].name}.")
                else:
                    print("Недостаточно средств на балансе компании!")
            else:
                print("Пункт продаж не найден.")
        else:
            print("Товар не найден!")

    def sell_product(self):
        """
        Обрабатывает бизнес-логику розничной продажи.
        Проверяет наличие товара на точке, списывает остатки, 
        увеличивает выручку точки и пополняет общий баланс компании.
        """
        pos_id = int(input("ID пункта продаж: "))
        
        if pos_id in self.points_of_sale:
            pos = self.points_of_sale[pos_id]
            print("Наличие в этом пункте:")
            for pid, qty in pos._inventory.items():
                print(f"ID Товара: {pid} | Кол-во: {qty} шт.")
                
            prod_id = int(input("ID продаваемого товара: "))
            qty = int(input("Количество для продажи: "))
            
            if pos._inventory.get(prod_id, 0) >= qty:
                product = self.products[prod_id]
                revenue = product.sell_price * qty
                
                pos._inventory[prod_id] -= qty
                pos.revenue += revenue
                self.company_balance += revenue
                
                print(f"Продано! Выручка: {revenue}")
            else:
                print("Недостаточно товара на точке.")
        else:
            print("Пункт продаж не найден.")

    def show_profitability(self):
        """Выводит в консоль финансовый отчет по компании в целом и по каждому пункту продаж."""
        print(f"\n--- ФИНАНСЫ ПРЕДПРИЯТИЯ ---")
        print(f"Баланс компании: {self.company_balance}")
        print("Доходность по пунктам продаж:")
        for pos in self.points_of_sale.values():
            profit = pos.revenue - pos.expenses
            print(f"ID: {pos.id} | Адрес: {pos.address} | Выручка: {pos.revenue} | Расходы: {pos.expenses} | ПРИБЫЛЬ: {profit}")
        print("---------------------------")


def main_menu():
    """
    Запускает бесконечный цикл консольного меню.
    Перехватывает исключения ввода и маршрутизирует команды 
    к соответствующим методам объекта CRMSystem.
    """
    app = CRMSystem()
    
    while True:
        print("\n" + "="*30)
        print(" CRM СИСТЕМА УПРАВЛЕНИЯ ")
        print("="*30)
        print("1. Найм сотрудника")
        print("2. Увольнение сотрудника")
        print("3. Открытие пункта продаж")
        print("4. Добавить товар в каталог (Создать карточку)")
        print("5. Закупка товара (Поставка на точку)")
        print("6. Продажа товара (Списание с точки)")
        print("7. Информация о доходности")
        print("8. Показать список сотрудников")
        print("0. Выход и Сохранение")
        
        choice = input("Выберите действие: ")
        
        try:
            match choice:
                case '1': 
                    app.hire_employee()
                case '2': 
                    app.fire_employee()
                case '3': 
                    app.open_point_of_sale()
                case '4': 
                    app.add_product_catalog()
                case '5': 
                    app.purchase_inventory()
                case '6': 
                    app.sell_product()
                case '7': 
                    app.show_profitability()
                case '8': 
                    for e in app.employees.values(): 
                        print(f"ID: {e.id} | Имя: {e.name} | Должность: {e.position}")
                case '0':
                    app.save_data()
                    print("Завершение работы программы...")
                    break
                case _:
                    print("Неверная команда, попробуйте снова.")
        except ValueError:
            print("Ошибка: ожидался ввод числа!")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main_menu()
