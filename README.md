# Leight项目重构用分支

本次重构旨在将代码内容规范化，增加可读性，梳理好项目结构。  
目标：  
1. 降低程序的资源开销，增加设备稳定性
2. 全面优化按键逻辑的实现代码
3. 减少定时器Timer的使用，全面改用_thread库，用线程优化设备的使用流畅度
