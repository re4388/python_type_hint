

# mypy 靜態型別檢查

# -----------------------
# 1. 適用時機。
# 大型專案用型別會清楚很多
# 如果是快速建立一個可以跑起來的原型，那用型別可能會降低速度。


# 壞處？你要寫的code變多了、多安裝mypy、需要去執行mypy xxx.py去進行型別檢查
# 好處？ 你不用跑下去才知道對錯，你看下面這兩行，你就知道第二個函數有問題。大型的code base不用跑就可以抓到型別的錯很省時間。
# 另外大型code base進行重構或是寫程式時，多了型別，讓我們寫程式可以更清楚，直接避免了型別錯誤。
# 好處應該是遠大於壞處的

# def str_len(s: str) -> int:
#     return len(s)
#
# def invalid_inc(n: int) -> str:
#     return n + 1


# -----------------------
# 2. 要小心的地方：
# 型別檢查只有在函數層級，因此類似下面這種只有加上部分型別的情況，就算寫錯，mypy不會跳錯。

# this is cuz it is expensive to ask mypy to inference acorss func, consider we
# could have multiple branch and multi-level recusive function calls
# and based on PEP484, Python is set its role on dynamic typed languge, so its type hint
# will always be partial and graudal, so keep in mind that Python allow incomplete type hint
# will result in this kind of danger.
# 不要認為型別檢查過了就沒有型別錯誤的問題，因為本身Python的型別檢查就只有在函數層級。

# example

# no return type hint here
# def expects_string(a: str):
#     return a
#
# def expects_int(a: int) -> int:
#     return a + 1
#
# runtime error, but mypy will no detect it!
# def main():
#     untyped = expects_string('a')
#     expects_int(untyped)




# -----------------------
# 如果要用！那下面就開始型別的介紹

# -----------------------
# 1. Primitive types

# 類似，bool, int, str, float
# 加在 type arguments 和 return types:

# example
# def str_len(s: str) -> int:
#     return len(s)

# def get_product_name(pd_id :int) -> str:
#     return get_from_db(pd_id)


# -----------------------
# 2. Composed types

# from typing import List, Dict, Tuple
#
# def gen_list() -> List[int]:
#     return [1,2,3]
#
# def gen_dict() -> Dict[str, int]:
#     return {'a': 1, 'b':2}
#
# def gen_tuple() -> Tuple[int, str]:
#     return (1, 'apple')

# -----------------------
# 3. 如果函數不應該返回值，用None
# def my_print(s: str) -> None:
#     print('>' + s)


# -----------------------
# 4. 如果函數不應該返回值，但可以允許raise, 用NoReturn
# from typing import NoReturn
# def not_ready(s: str) -> NoReturn:
#     print('not implemented')
#     raise # ok: always throws

# -----------------------
# 5. 你也可以對於變數建立的時候去給定型別
# b: bool = False
# i: int = 1
# s: str = 'abc'
# f: float = 1.0


# -----------------------
# 6. 如果你會返回 None 或 返回某種型別，可以用 Optional[T]
# from typing import Optional
#
# def get_first_product(product_code: List[int]) -> Optional[int]:
#     if len(product_code) == 0:
#         return None
#     else:
#         return product_code[0]

# -----------------------
# 7. 或用 Union[Type_1, Type_2]
# from typing import Union
# import random
#
# def int_or_str() -> Union[str, int]:
#     if random.randint(0, 1) == 0:
#         return 0
#     else:
#         return 'do not hit zero'

# 原文作者建議使用Union會謹慎，返回多個型別，反而讓code flow更不清楚。
# 一般建議用在繼承時的基類。


# -----------------------
# 8. Any vs. object

# any type 是所有型別，如同沒有增加型別檢查
# object 型別是所有型別的基類，類似所有型別的Union
# 如果你定義了object型別，你還需要定義更細的型別才能被其他型別使用。請看下面的 “Refining types”

# def dummy(x: object) -> object:
#     return x
#
# def inc(x: int) -> int:
#     return x + 1
#
# dummy(Square()) # ok
# inc(dummy(1))   # error - dummy(1) returns object

# -----------------------
# 9. Classes
# 幾個注意的地方。
# class裡面的變數一樣可以加上type
# 我們不會去給self加上type
# 參數和方法的返回值都可以加上型別

# class C:
#
#     _n: int
#
#     def __init__(self, n: int) -> None:
#         self._n = n
#
#     def inc(self) -> None:
#         self._n += 1

# -----------------------
# 10. Callables

# 通常是所謂的高階函數，表示函數的參數裡面放入函數。
# 下面的 f 就是所謂的 Callable
# Callable[[int], int]), 第一個 int 是這個函數吃的參數，第二的int是這個函數的返回值。也都可以加入型別

# def typed_map(xs: List[int], f: Callable[[int], int]) -> List[int]:
#     return [f(x) for x in xs]
#
# print(typed_map([1, 2, 3], lambda x: x*2))

# 這個例子的 Callable 就吃兩個字串參數，返回一個字串參數。
# def typed_reduce(xs: List[str], f: Callable[[str, str], str], x0: str) -> str:
#     r = x0
#     for x in xs:
#         r = f(r, x)
#     return r
#
# print(typed_reduce(['a', 'b', 'c'], lambda x, y: x + y, ''))


# -----------------------
# 11. Generics: Type Variables
# 型別本身也可以被定義為一個變數，然後在不同地方使用。
# 比如，下面的T就是一個型別變數。first 函數的參數和返回的值，裡面的T都需要是同一個型別。

# from typing import TypeVar
# T = TypeVar('T')
#
# def first(xs: List[T]) -> Optional[T]:
#     if (len(xs) == 0):
#         return None
#     return xs[0]


# 這邊要注意的是，TypeVar裡面的'T1'必須跟你定義的變數名稱T1一樣
# 作者認為這可能是mypy受限於Python解釋器所造成的限制語法。

# 下面演示了建立兩個型別變數
# T1 = TypeVar('T1')
# T2 = TypeVar('T2')
#
# def tuplify(a: T1, b: T2) -> Tuple[T1, T2]:
#     return (a, b)


# 型別變數也可以定義這個型別的必須是那種刑
# 下面這種寫法是說，Tmix可以是 int or str
#
# 需要留意，這個意思和 Union[int, str] 不同。
# TypeVar('Tmix', int, str) 是說，int 或 str, 2擇一，你用了一個，就不可以是另一個。
# Union[int, str] 是說，結果只要是兩種之一，都可以


# Tmix = TypeVar('Tmix', int, str)
#
# def fmix(a: Tmix, b: Tmix) -> Tmix:
#     if(random.randint(0, 1) == 0):
#         return a
#     return b
#
# fmix('a', 'b') # ok
# fmix(1, 2) # ok
# fmix('a', 1) # error

# -----------------------
# 12. Parametrized Classes

# 我們同樣可以把型別變數用在類上
# 使用上需要導入Generic基類

# from typing import Generic
# class Parametrized(Generic[T]):
#     value: T
#
#     def __init__(self, value: T) -> None:
#         self.value = value
#
#     def getValue(self) -> T:
#         return self.value


# -----------------------
# 13. Ignoring type hints

# 加上 `# type: ignore` 在那一行程式碼，那一行就不會去檢查型別。
# 如果放在第一行，這個py檔就不會去檢查型別。

# pseudo_int: int = 'a'  # type: ignore




# -----------------------
# 14. Refining types: isinstance() and cast()

# 一種情況是，如果你的型別是 object, 這樣不清不處，型別檢查器會跳錯。
# 一個方法是在呼叫函數前，先用 isinstance 去檢查。這樣檢查器就可以自動推論到了。

# def inc(x: int) -> int:
#     return x + 1
#
#
# def delegate(x: object) -> object:
#     if (isinstance(x, int)):
#         return inc(x)


# cast([type], x)的用法不是很清楚，先跳過。

# -----------------------
# 15. Arbitrary argument lists

# 也可以給 *args 和 **kwargs 加上型別
# def foo(*args: str, **kwargs: int):
#     pass





if __name__ == '__main__':
    str_1 = 'apple'
    # print(str_len(str_1))

    # print(invalid_inc(1))   # no error popup?

    user_input = 10
    fee = 10
    value = convert_currency(user_input) - fee


