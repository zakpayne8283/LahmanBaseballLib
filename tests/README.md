## ✅ Test Results & Coverage
```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\Zak\source\repos\MyBaseballLib
plugins: cov-6.2.1
collected 29 items

tests\Lahman\test_allstar_appearances.py ........                        [ 27%]
tests\Lahman\test_allstar_appearances_api.py ...                         [ 37%]
tests\Lahman\test_base_table.py .                                        [ 41%]
tests\Lahman\test_people.py .....                                        [ 58%]
tests\Lahman\test_query_builder.py ............                          [100%]

=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.13.5-final-0 _______________

Name                                        Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------
src\Lahman\api\allstars_api.py                 20      5    75%   73-96
src\Lahman\db\connector.py                      7      0   100%
src\Lahman\db\models\AllstarApperances.py      14      0   100%
src\Lahman\db\models\People.py                 35      0   100%
src\Lahman\db\models\base_table.py             26      0   100%
src\Lahman\db\models\query_builder.py         161      3    98%   336-338
-------------------------------------------------------------------------
TOTAL                                         263      8    97%
============================= 29 passed in 0.48s ==============================
```
