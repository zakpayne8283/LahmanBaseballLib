## ✅ Test Results & Coverage
```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\Zak\source\repos\LahmanBaseballLib
plugins: cov-6.2.1
collected 26 items

tests\test_allstar_appearances.py .........                              [ 34%]
tests\test_base_table.py .                                               [ 38%]
tests\test_people.py ......                                              [ 61%]
tests\test_query_builder.py ..........                                   [100%]

=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.13.5-final-0 _______________

Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
src\db\connector.py                      7      0   100%
src\db\models\AllstarApperances.py      19      0   100%
src\db\models\People.py                 45      0   100%
src\db\models\base_table.py             26      0   100%
src\db\models\query_builder.py         123      3    98%   259-261
------------------------------------------------------------------
TOTAL                                  220      3    99%
============================= 26 passed in 0.46s ==============================
```
