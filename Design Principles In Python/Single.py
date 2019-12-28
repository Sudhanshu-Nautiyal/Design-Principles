#1. Solid Principles

#Class and functions definitions

class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f'{self.count}: {text}')

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return '\n'.join(self.entries)

j = Journal()
j.add_entry('This is Solid Principles code' )
j.add_entry('I bought it from Udemy')
print(f'Journal Entries: \n{j}')

#2. Open Closed Principles

#OCP

from enum import Enum

class Color(Enum):
   RED = 1
   GREEN = 2
   BLUE = 3

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size  = size

class ProductFilter:
     def filter_by_color(self, products, color):
         for p in products:
             if p.color == color:
                yield p

     def filter_by_size(self, products, size):
         for p in products:
             if p.size == size:
                yield p

     def filter_by_size_and_color (self, products, size, color):
         for p in products:
             if p.color == color and p.size  == size:
                 yield p

# Enterprice Patterns : Specification

class Specification:
     def is_satisfied(self, item):
         pass

class Filter:
    def filter (self, items, spec):
         pass;

class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        #super().is_satisfied(self, item)
        return item.color == self.color

class SizeSpecifiation(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        #super().is_satisfied(self, item)
        return item.size == self.size

class AndSpecification(Specification):
    def __init__(self, spec1, spec2):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied(self, item):
        #super().is_satisfied(self, item)
        return self.spec1.is_satisfied(item) and \
               self.spec2.is_satisfied(item)


class BetterFilter(Filter):
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item;


# Code Execution

apple = Product('Apple', Color.GREEN, Size.SMALL )
tree = Product('Tree', Color.GREEN, Size.LARGE )
house = Product('House', Color.BLUE, Size.LARGE )

products = [apple, tree, house]
#
# pf = ProductFilter()
# print('Green Products:(Old)')
# for p in pf.filter_by_color(products, Color.GREEN):
#     print(f'{p.name} is Green')

bf = BetterFilter()

print('Green Products:(New)')
green = ColorSpecification(Color.GREEN)
for p in bf.filter(products, green):
    print(f'- {p.name} is green')


print('Large Product:(New)')
large  = SizeSpecifiation(Size.LARGE)
for p in bf.filter(products, large):
    print(f'- {p.name} is large')


print('Large and Blue Item')
large_blue =  large and ColorSpecification(Color.BLUE)
for p in bf.filter(products, large_blue):
    print(f'- {p.name} is large and blue')

# 3. Lishkov Principles

class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def area(self):
        return self._width * self._height

    def __str__(self):
        return f'Width: {self.width}, height: {self.height}'

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value


class Square(Rectangle):
    def __init__(self, size):
        Rectangle.__init__(self, size, size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value


def use_it(rc):
    w = rc.width
    rc.height = 10
    expected = int(w*10)
    print(f'Expected an area of {expected}, got{rc.area}')

rc = Rectangle(2,3)
use_it(rc)

sq = Square(5)
use_it(sq)


# 4. Interface Segregation Principle

from abc import abstractmethod


class Machine:
    def print(self, document):
        raise NotImplementedError()

    def fax(self, document):
        raise NotImplementedError()

    def scan(self, document):
        raise NotImplementedError()


# ok if you need a multifunction device
class MultifunctionPrinter(Machine):
    def print(self, document):
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        pass

class OldFashionedPrinter(Machine):
    def print(self, document):
        # ok
        pass

    def fax(self, document):
        pass # noop

    def scan(self, document):
        """Not supported!"""
        raise NotImplementedError('Printer cannot scan!')


class Printer:
    @abstractmethod
    def print(self, document):
        pass

class Scanner:
    @abstractmethod
    def print(self, document):
        pass

class MyPrinter(Printer):
    def print(self, document):
        pass


class PhotoCopier(Printer, Scanner):
    def print(self, document):
        print(document)

    def scan(self, document):
        pass # something meaningful

class MultiFunctionDevice(Printer, Scanner):
    @abstractmethod
    def print(self, document):
       pass

    @abstractmethod
    def scan(self, document):
        pass


class MultiFunctionMachine(MultiFunctionDevice):
    def __init__(self, printer, scanner):
        self.printer = printer
        self.scanner = scanner

    def print(self, document):
        self.printer.print(document)

    def scan(self, document):
        self.scanner.scan(document)


printer = OldFashionedPrinter()
printer.fax(123)  # nothing happens
printer.scan(123)  # oops!



# 5. Dependency Inversion Principle

from abc import abstractmethod
from enum import Enum


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2


class Person:
    def __init__(self, name):
        self.name = name


class RelationshipBrowser:
    @abstractmethod
    def find_all_children_of(self, name): pass


class Relationships(RelationshipBrowser):  # low-level
    relations = []

    def add_parent_and_child(self, parent, child):
        self.relations.append((parent, Relationship.PARENT, child))
        self.relations.append((child, Relationship.PARENT, parent))

    def find_all_children_of(self, name):
        for r in self.relations:
            if r[0].name == name and r[1] == Relationship.PARENT:
                yield r[2].name


class Research:
    # dependency on a low-level module directly
    # bad because strongly dependent on e.g. storage type

    # def __init__(self, relationships):
    #     # high-level: find all of john's children
    #     relations = relationships.relations
    #     for r in relations:
    #         if r[0].name == 'John' and r[1] == Relationship.PARENT:
    #             print(f'John has a child called {r[2].name}.')

    def __init__(self, browser):
        for p in browser.find_all_children_of("John"):
            print(f'John has a child called {p}')


parent = Person('John')
child1 = Person('Chris')
child2 = Person('Matt')

# low-level module
relationships = Relationships()
relationships.add_parent_and_child(parent, child1)
relationships.add_parent_and_child(parent, child2)

Research(relationships)