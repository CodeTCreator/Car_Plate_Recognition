# API к системе учета ТС

### Данное API является составляющей системы учета ТС и является продолжением системы управления базами данных (Coursework_DB_API). Оно представляет собой Телеграм-бота, на вход которому подается изобржание автомобиля, а на выходе информация о данном авто, елси такова имеется

## Структура API:
- ### Система распознавания автомобильного номера на изображении:
  - ### Python (OpenCV с использованием Haar Cascade) для обнаружения номера и обработки фото 
  - ### Tesseract OCR для распознавания символов
  - ### Лингвистическая обработка результата (для повышения точности)
- ### Бэкэнд бота, описание работы взаимодействия с пользователем и с БД

## Описание работы API:
### Пользователь взаимодействует с ботом. После его активации можно боту отправлять изображения авто. Отправленное фото временно сохраняется в систему для обработки и распознавания. На изображении система пытается обнаружить автомобильный номер, в случае успеха оно предобрабатывается и переходит к этапу распознавания. Tesseract OSR распознает символы на фото. Следующим этапом является лингвистический анализ для повышения точности распознавания. А заключительным является запрос к БД на получение информации об авто и выдача ее ботом.
#### Пример ответа:
![изображение](https://github.com/user-attachments/assets/7b19f95f-eb07-4703-80d6-833452c23c49)
#### Система подразумевает возможность объявить авто в розыск, тогда будет выдаваться дополнительная информация (полное название, цвет, отличительные черты)*
