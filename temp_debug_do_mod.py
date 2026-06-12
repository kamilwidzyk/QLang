import sys
import os
sys.path.insert(0, os.getcwd())
from int.operations.operators import do_operation_mod
from int.expression import Expression, TYPE_STRING, TYPE_INT, TYPE_NUM
from int.variable import Variable
from int.num import Num

x = Variable('x', TYPE_NUM, [0])
x.set(Expression(TYPE_INT, 2), allow_const_init=True)
print('x.type', x.type, 'data', type(x.data).__name__, 'is_list', x.is_list)
left = Expression(TYPE_STRING, '%d')
for right in [2, Expression(TYPE_INT, 2), Expression(TYPE_NUM, Num(2)), x, x.get(), x.get_value()]:
    try:
        res = do_operation_mod(left, right)
        print('right', type(right).__name__, '=>', res.value)
    except Exception as e:
        print('ERROR right', type(right).__name__, type(e).__name__, str(e))
