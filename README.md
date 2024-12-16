### Ферма веселого МакДоналда
#### Требования
- python 3.8+
- postgresql
- GUI (приложение является графическим)
#### Функционал
- Разделение пользователей на администратор/пользователь
- Учет типов животных
- Учет животных
#### Сборка пакета из исходных файлов
```
python -m venv venv
source venv/bin/activate
python install -r requirements.txt
```
обновите учетные данные в файле app.py
```
make build
```
исполняемый файл будет расположен в ./dist
