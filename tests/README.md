## ✅ Test Results & Coverage
```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\Zak\source\repos\LahmanBaseballLib
plugins: cov-6.2.1
collected 29 items

tests\test_allstar_appearances.py ........                               [ 27%]
tests\test_allstar_appearances_api.py ...                                [ 37%]
tests\test_base_table.py .                                               [ 41%]
tests\test_people.py .....                                               [ 58%]
tests\test_query_builder.py ............                                 [100%]

=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.13.5-final-0 _______________

Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
src\api\allstars_api.py                 14      0   100%
src\db\connector.py                      7      0   100%
src\db\models\AllstarApperances.py      14      0   100%
src\db\models\People.py                 36      0   100%
src\db\models\base_table.py             26      0   100%
src\db\models\query_builder.py         161      3    98%   336-338
------------------------------------------------------------------
TOTAL                                  258      3    99%
============================= 29 passed in 0.43s ==============================
```
