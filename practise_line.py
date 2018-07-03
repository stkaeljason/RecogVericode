import tensorflow as tf

import pandas as pd
import numpy as np
a=pd.Series(['kk','aa','cc'])
b=pd.Series([23,98,100])
person = pd.DataFrame({'name': a, 'value': b})

print(b.apply(lambda x:x > 24))
person['sex'] = pd.Series(['male', 'female', 'male'])
person['work_year'] = pd.Series([3, 40, 50])
person['xxx'] = person['value'] / person['work_year']
print(person)

print(np.log(b))
