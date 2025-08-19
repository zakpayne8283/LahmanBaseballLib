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

Name                                             Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------
src\Lahman\api\allstars_api.py                      20      5    75%   73-96
src\Lahman\db\models\AllstarApperances.py           14      0   100%
src\Lahman\db\models\People.py                      35      0   100%
src\Lahman\db\models\lahman_table.py                 3      0   100%
src\Retrosheet\data\build_database.py               47     47     0%   1-104
src\Retrosheet\data\config.py                       11     11     0%   2-20
src\Retrosheet\data\download_data.py                56     56     0%   1-120
src\Retrosheet\data\load_data.py                     3      3     0%   1-4
src\Retrosheet\data\models\Game.py                  14     14     0%   1-29
src\Retrosheet\data\models\retrosheet_table.py       7      7     0%   1-11
src\Retrosheet\setup.py                              6      6     0%   1-10
src\utils\db\base_table.py                          26      0   100%
src\utils\db\connector.py                            6      0   100%
src\utils\db\query_builder.py                      163      3    98%   339-341
------------------------------------------------------------------------------
TOTAL                                              411    152    63%
============================= 29 passed in 0.49s ==============================
```
