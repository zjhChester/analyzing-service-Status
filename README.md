### 适配项目：
- spring管理的java项目
- 使用lombok管理getter的项目


---
### 支持的分析类目：
- 集合 `done`
- 全局变量 `refactoring` `not very accurate`
- 缓存 `todo`
- 配置 `todo`


---
### 使用：

- 在`Executer.py`内,修改`dirPath`的路径
- 执行main函数, 如果最终`CollectionsAnalysis.py/ObjectsAnalysis.py`里的`absoluteHasStatusVariables`有值， 则为有状态服务 