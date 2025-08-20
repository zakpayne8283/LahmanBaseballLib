## ✅ Test Results & Coverage
```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
rootdir: C:\Users\Zak\source\repos\MyBaseballLib
plugins: cov-6.2.1
collected 30 items

tests\Lahman\test_allstar_appearances.py ........                        [ 26%]
tests\Lahman\test_allstar_appearances_api.py ....                        [ 40%]
tests\Lahman\test_base_table.py .                                        [ 43%]
tests\Lahman\test_people.py .....                                        [ 60%]
tests\Lahman\test_query_builder.py ............                          [100%]

=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.13.5-final-0 _______________

Name                                             Stmts   Miss  Cover   Missing
------------------------------------------------------------------------------
src\Lahman\api\allstars_api.py                      20      0   100%
src\Lahman\db\models\AllstarApperances.py           14      0   100%
src\Lahman\db\models\People.py                      35      0   100%
src\Lahman\db\models\lahman_table.py                 3      0   100%
src\Retrosheet\data\build_database.py               48     48     0%   1-107
src\Retrosheet\data\config.py                       11     11     0%   2-20
src\Retrosheet\data\download_data.py                56     56     0%   1-120
src\Retrosheet\data\models\Game.py                  10     10     0%   1-21
src\Retrosheet\data\models\retrosheet_table.py      25     25     0%   1-73
src\Retrosheet\setup.py                              6      6     0%   1-10
src\utils\db\base_table.py                          26      0   100%
src\utils\db\connector.py                            6      0   100%
src\utils\db\query_builder.py                      163      3    98%   339-341
------------------------------------------------------------------------------
TOTAL                                              423    159    62%
============================= 30 passed in 0.47s ==============================
```
