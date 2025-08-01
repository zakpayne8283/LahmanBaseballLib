## ✅ Test Results & Coverage
```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\Zak\source\repos\LahmanBaseballLib
plugins: cov-6.2.1
collected 25 items

tests\test_allstar_appearances.py .........                              [ 36%]
tests\test_base_table.py .                                               [ 40%]
tests\test_people.py ......                                              [ 64%]
tests\test_query_builder.py .........                                    [100%]

=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.13.5-final-0 _______________

Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
src\db\connector.py                      7      0   100%
src\db\models\AllstarApperances.py      19      0   100%
src\db\models\People.py                 45      0   100%
src\db\models\base_table.py             26      0   100%
src\db\models\query_builder.py          96      3    97%   202-204
------------------------------------------------------------------
TOTAL                                  193      3    98%
============================= 25 passed in 0.42s ==============================
```
